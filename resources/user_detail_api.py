# -*- coding:utf-8 -*-

import re, hashlib, tempfile
from flask.ext.restful import Resource, reqparse, marshal_with
from flask.ext.login import current_user
from flask.globals import current_app
from PIL import Image

from common.mods import db
from common.api_errors import UserNotFound, Forbidden
from common.models import User
from common.fields import user_detail_fields
from common.service_configs import USER_PROFILE_WIDTH_NORMAL, USER_PROFILE_HEIGHT_NORMAL
from utils import api_login_required, rotate_image_with_exif, upload_profile_image, make_thumbnail
from werkzeug.datastructures import FileStorage

__author__ = "Philgyu,Seong"
__email__ = "phil@treasureisle.co"

KEY_PROFILE_THUMB = "profile_thumb"
KEY_INTRODUCE = "introduce"
KEY_NAME = "name"
KEY_ZIPCODE = "zipcode"
KEY_ADDRESS1 = "address1"
KEY_ADDRESS2 = "address2"
KEY_PHONE = "phone"
KEY_BANK_ACCOUNT = "bank_account"
KEY_BIZ_NUM = "biz_num"

LOCATION_FORM = "form"
LOCATION_FILES = "files"


class UserDetailApi(Resource):
    def __init__(self):
        self.post_parser = reqparse.RequestParser()
        self.post_parser.add_argument(KEY_INTRODUCE, location=LOCATION_FORM)
        self.post_parser.add_argument(KEY_NAME, location=LOCATION_FORM)
        self.post_parser.add_argument(KEY_ZIPCODE, location=LOCATION_FORM)
        self.post_parser.add_argument(KEY_ADDRESS1, location=LOCATION_FORM)
        self.post_parser.add_argument(KEY_ADDRESS2, location=LOCATION_FORM)
        self.post_parser.add_argument(KEY_PHONE, location=LOCATION_FORM)
        self.post_parser.add_argument(KEY_BANK_ACCOUNT, location=LOCATION_FORM)
        self.post_parser.add_argument(KEY_BIZ_NUM, location=LOCATION_FORM)

        self.post_parser.add_argument(KEY_PROFILE_THUMB, type=FileStorage, location=LOCATION_FILES)


    @api_login_required
    @marshal_with(user_detail_fields, envelope="user_detail")
    def get(self, user_id):
        user = User.query.filter(User.id == user_id).first()

        if user is None:
            raise UserNotFound

        return user

    @api_login_required
    @marshal_with(user_detail_fields, envelope="user_detail")
    def post(self, user_id):

        if current_user.id != user_id:
            raise Forbidden

        user = User.query.filter(User.id == user_id).first()

        if user is None:
            raise UserNotFound

        args = self.post_parser.parse_args()

        profile_thumb = args[KEY_PROFILE_THUMB]
        introduce = args[KEY_INTRODUCE]
        name = args[KEY_NAME]
        zipcode = args[KEY_ZIPCODE]
        address1 = args[KEY_ADDRESS1]
        address2 = args[KEY_ADDRESS2]
        phone = args[KEY_PHONE]
        bank_account = args[KEY_BANK_ACCOUNT]
        biz_num =args[KEY_BIZ_NUM]

        if profile_thumb is not None:
            stream = args[KEY_PROFILE_THUMB].stream
            image = Image.open(stream)
            image = rotate_image_with_exif(image)

            tf = tempfile.NamedTemporaryFile()
            thumbnail = make_thumbnail(image, (USER_PROFILE_WIDTH_NORMAL, USER_PROFILE_HEIGHT_NORMAL))
            thumbnail.save(tf, format="JPEG")

            s3_url = upload_profile_image(current_app, tf.name, user.id)

            user.profile_thumb_url = s3_url

        if introduce is not None:
            user.introduce = introduce

        if name is not None:
            user.name = name

        if zipcode is not None:
            user.zipcode = int(zipcode)

        if address1 is not None:
            user.address1 = address1

        if address2 is not None:
            user.address1 = address1

        if phone is not None:
            user.recent_address1 = phone

        if bank_account is not None:
            user.recent_address1 = bank_account

        if biz_num is not None:
            user.biz_num = biz_num

        db.session.merge(user)
        db.session.commit()

        return user

