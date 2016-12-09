# -*- coding:utf-8 -*-
from functools import wraps

from flask.globals import request, current_app
from flask.ext.login import current_user
from flask.ext.restful import abort
from common.api_errors import Forbidden
from common.mods import db, bcrypt
from common.service_configs import CLIENT_ACCESS_TOKEN_SALT
from common.config_keys import KEY_CDN_URL, KEY_AWS_ACCESS_KEY_ID, KEY_AWS_ACCESS_SECRET, KEY_S3_BUCKET
from configs import API_URL
from boto3 import client
from boto3.s3.transfer import S3Transfer
from PIL import ImageOps, ExifTags, Image
import requests
import json
import time
import hashlib
import datetime
import arrow

__author__ = "Philgyu, Seong"
__email__ = "phil@treasureisle.co"


def check_ip(func):
    """
    white list 에 포함된 ip 인지를 확인 아니면 403을 리턴한다.
    :param func:
    :return:
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        if request.remote_addr not in current_app.config["WHITE_IPS"]:
            raise Forbidden

        return func(*args, **kwargs)

    return wrapper


def get_current_time_ms():
    return int(round(time.time() * 1000))


def generate_client_access_token(id):
    """
    유저에게 줄 access_token 생성
    """
    key = "%d%s%d" % (id, CLIENT_ACCESS_TOKEN_SALT, get_current_time_ms())
    return hashlib.sha256(key).hexdigest()


def get_user_access_token(user):
    user_access_token = generate_client_access_token(id=user.id)
    user.access_token = bcrypt.generate_password_hash(user_access_token)

    db.session.merge(user)
    db.session.commit()
    return user_access_token


def get_json_headers(user=None):
    header = {"content-type": "application/json"}
    if user is not None:
        access_token = get_user_access_token(user)
        header["Authorization"] = "%s:%s" % (user.id, access_token)

    return header


def get_api_url(sub_url):
    return "%s%s" % (API_URL, sub_url)


def json_post(sub_url, user=None, data=None, headers=None):
    if data:
        data = json.dumps(data)
    _headers = headers if headers else get_json_headers(user=user)
    return requests.post(url=get_api_url(sub_url), data=data, headers=_headers)


def json_get(sub_url, user=None, data=None, headers=None):
    if data:
        data = json.dumps(data)
    _headers = headers if headers else get_json_headers(user=user)
    return requests.get(url=get_api_url(sub_url), data=data, headers=_headers)


def json_delete(sub_url, user, headers=None):
    _headers = headers if headers else get_json_headers(user=user)
    return requests.delete(url=get_api_url(sub_url), headers=_headers)


def get_key_or_abort400(args, param):
    p = args[param]
    if p is None:
        abort(400, message="parameter %s is missing." % param)
    return p


def get_now_mysql_datetime():
    """
    now mysql datetime 형 반환

    :return:
    """

    return time.strftime('%Y-%m-%d %H:%M:%S')


def get_past_mysql_datetime(days):
    """
    mysql datetime 형 과거 날짜 반환
    :param days: 기간
    :return:
    """
    return (datetime.datetime.today() - datetime.timedelta(days=days)).strftime('%Y-%m-%d %H:%M:%S')


def python_time_to_mysql_datetime(python_time):
    return python_time.strftime('%Y-%m-%d %H:%M:%S')


def python_str_time_to_python_time(python_str_time):
    # Thu, 12 Mar 2015 15:19:10 -0000
    return arrow.get(python_str_time, "ddd, DD MMM YYYY HH:mm:ss Z")


def get_default_profile_thumb_url(app):
    return "%s/imgs/default_person.png" % app.config[KEY_CDN_URL]


def generate_client_access_token(id):
    """
    유저에게 줄 access_token 생성
    """
    key = "%d%s%d" % (id, CLIENT_ACCESS_TOKEN_SALT, get_current_time_ms())
    return hashlib.sha256(key).hexdigest()


def get_page_offset(page, limit):
    return (page - 1) * limit


def api_login_required(func):
    """
    login 이 필요한 api 에 씌어서 사용한다.
    login 이 안되어있다면 403 을 리턴한다.
    :param func:
    :return:
    """

    @wraps(func)
    def decorated_view(*args, **kwargs):
        if not current_user.is_authenticated:
            print "what?"
            raise Forbidden
        return func(*args, **kwargs)

    return decorated_view


def get_boto_client(app, service, region_name="ap-northeast-2"):
    return client(service, region_name=region_name,
                  aws_access_key_id=app.config[KEY_AWS_ACCESS_KEY_ID],
                  aws_secret_access_key=app.config[KEY_AWS_ACCESS_SECRET])


def make_s3_url(app, keyname):
    return "%s/%s" % (app.config[KEY_CDN_URL], keyname)


def upload_file_to_s3(app, filename, keyname, content_type="image/jpeg"):
    client = get_boto_client(app, "s3")
    transfer = S3Transfer(client)
    transfer.upload_file(filename, app.config[KEY_S3_BUCKET], keyname,
                         extra_args={'ACL': 'public-read', "ContentType": content_type})

    return make_s3_url(app, keyname)


def rotate_image_with_exif(image):
    if hasattr(image, '_getexif'):  # only present in JPEGs
        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation] == 'Orientation':
                break
        e = image._getexif()  # returns None if no EXIF data
        if e is not None:
            exif = dict(e.items())
            orientation = exif[orientation]

            if orientation == 3:
                image = image.transpose(Image.ROTATE_180)
            elif orientation == 6:
                image = image.transpose(Image.ROTATE_270)
            elif orientation == 8:
                image = image.transpose(Image.ROTATE_90)

    return image


def upload_profile_image(app, filename, user_id):
    return upload_file_to_s3(app, filename, make_profile_keyname(user_id))


def make_profile_keyname(user_id):
    return "profiles/%d_o_%s.jpg" % (user_id, base36encode(get_current_time_ms()))


def base36encode(number):
    if not isinstance(number, (int, long)):
        raise TypeError('number must be an integer')
    if number < 0:
        raise ValueError('number must be positive')

    alphabet = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'

    base36 = ''
    while number:
        number, i = divmod(number, 36)
        base36 += alphabet[i]

    return base36 or alphabet[0]


def make_thumbnail(image, size=(100, 100)):
    return ImageOps.fit(image, size, Image.ANTIALIAS,
                        centering=(0.5, 0.5))
