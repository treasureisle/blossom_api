# -*- coding:utf-8 -*-

import re, hashlib, tempfile

from flask.ext.restful import Resource, reqparse, marshal_with
from flask.globals import current_app
from PIL import Image

from common.mods import bcrypt, db
from common.api_errors import UserNotFound, InternalServerError, NotValidUsername, UsernameTooShort, UsernameTooLong, \
    UserAlreadyExist, UsernameAlreadyTaken, NotValidEmail, EmailAlreadyTaken
from common.models import User, Session
from common.fields import session_fields, user_fields
from common.regex import REGEX_USERNAME, REGEX_EMAIL
from common.service_configs import MIN_USERNAME_LENGTH, MAX_USERNAME_LENGTH, USER_PROFILE_HEIGHT_NORMAL, \
    USER_PROFILE_WIDTH_NORMAL
from utils import json_post, json_delete, get_key_or_abort400, get_now_mysql_datetime, get_default_profile_thumb_url, \
    generate_client_access_token, rotate_image_with_exif, upload_profile_image, make_thumbnail
from werkzeug.datastructures import FileStorage

__author__ = "Philgyu, Seong"
__email__ = "phil@treasureisle.co"

KEY_REG_TYPE = "reg_type"
KEY_EMAIL = "email"
KEY_USERNAME = "username"
KEY_PASSWORD = "password"
KEY_PROFILE_THUMB = "profile_thumb"

LOCATION_FORM = "form"
LOCATION_FILES = "files"

REG_TYPE_EMAIL = "email"


class UsersApi(Resource):
    def __init__(self):
        self.post_parser = reqparse.RequestParser()
        self.post_parser.add_argument(KEY_REG_TYPE, required=True)
        self.post_parser.add_argument(KEY_EMAIL, location=LOCATION_FORM)
        self.post_parser.add_argument(KEY_PASSWORD, location=LOCATION_FORM)
        self.post_parser.add_argument(KEY_USERNAME, location=LOCATION_FORM)
        self.post_parser.add_argument(KEY_PROFILE_THUMB, type=FileStorage, location=LOCATION_FILES)

    @marshal_with(user_fields, envelope="user")
    def get(self, user_id):
        user = User.query.filter(User.id == user_id).first()

        if user is None:
            raise UserNotFound

        return user

    @marshal_with(session_fields, envelope="session")
    def post(self):
        def validate_username(username):
            if len(username) < MIN_USERNAME_LENGTH:
                raise UsernameTooShort

            if len(username) > MAX_USERNAME_LENGTH:
                raise UsernameTooLong

            if not re.match(REGEX_USERNAME, username):
                raise NotValidUsername

            if User.query.filter(User.username == username).first() is not None:
                raise UsernameAlreadyTaken

        def validate_email(email):
            if not re.match(REGEX_EMAIL, email):
                raise NotValidEmail

        def check_email_is_taken(email):
            if User.query.filter(User.email == email).first() is not None:
                raise EmailAlreadyTaken

        args = self.post_parser.parse_args()

        reg_type = get_key_or_abort400(args, KEY_REG_TYPE)
        username = get_key_or_abort400(args, KEY_USERNAME)
        profile_thumb = args[KEY_PROFILE_THUMB]

        validate_username(username)

        if reg_type == REG_TYPE_EMAIL:
            email = get_key_or_abort400(args, KEY_EMAIL)
            password = get_key_or_abort400(args, KEY_PASSWORD)

            validate_email(email)
            check_email_is_taken(email)

            hashed_password = bcrypt.generate_password_hash(password=password)

            new_user = User(username=username, created_at=get_now_mysql_datetime(),
                            last_logged_at=get_now_mysql_datetime(),
                            profile_thumb_url=get_default_profile_thumb_url(current_app), email=email,
                            password=hashed_password)

            db.session.add(new_user)
            db.session.flush()
            db.session.refresh(new_user)

            user_access_token = generate_client_access_token(new_user.id)

            access_token = bcrypt.generate_password_hash(user_access_token)
            new_user.access_token = access_token

            if profile_thumb is not None:
                stream = args[KEY_PROFILE_THUMB].stream
                image = Image.open(stream)
                image = rotate_image_with_exif(image)

                tf = tempfile.NamedTemporaryFile()
                thumbnail = make_thumbnail(image, (USER_PROFILE_WIDTH_NORMAL, USER_PROFILE_HEIGHT_NORMAL))
                thumbnail.save(tf, format="JPEG")

                s3_url = upload_profile_image(current_app, tf.name, new_user.id)

                new_user.profile_thumb_url = s3_url

            db.session.merge(new_user)
            db.session.commit()

            session = Session(new_user.id, user_access_token, new_user.username)

            return session

    def delete(self, user_id):

        user = User.query.filter(User.id == user_id).first()

        if user is None:
            raise UserNotFound

        sub_url = "/users/me"

        response = json_delete(sub_url=sub_url, user=user)

        if response.status_code != 200:
            raise InternalServerError

        return response.json()

    def make_image_filename(self, post_id, number):
        h = hashlib.md5()
        h.update(str(post_id))
        return "%s_%d.jpg" % (h.hexdigest(), number)

    def make_image_keyname(self, image_filename):
        return "profile_thumbs/%s" % image_filename
