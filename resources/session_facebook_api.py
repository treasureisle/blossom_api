# -*- coding:utf-8 -*-

from flask.ext.restful import Resource, marshal_with, reqparse
from flask.globals import current_app
import requests

from common.api_errors import NotValidFbAccessToken, UserNotFound
from common.config_keys import KEY_CDN_URL
from common.fields import session_fields
from common.models import User, Session
from common.mods import bcrypt, db
from utils import upload_fb_thumb, generate_client_access_token

__author__ = "Philgyu,Seong"
__email__ = "philgyu.seong@gluvi.co"


KEY_EMAIL = "email"
KEY_FB_ID = "fb_id"
KEY_FB_ACCESS_TOKEN = "fb_access_token"


class SessionFacebookApi(Resource):
    @marshal_with(session_fields, envelope="session")
    def post(self):
        post_parser = reqparse.RequestParser()
        post_parser.add_argument(KEY_EMAIL, type=str)
        post_parser.add_argument(KEY_FB_ID, type=str, required=True)
        post_parser.add_argument(KEY_FB_ACCESS_TOKEN, type=str, required=True)

        args = post_parser.parse_args()
        email = args[KEY_EMAIL]
        fb_id = args[KEY_FB_ID]
        fb_access_token = args[KEY_FB_ACCESS_TOKEN]

        # 인증 확인
        fb_validate_r = requests.get("https://graph.facebook.com/me?access_token=%s" % fb_access_token)
        if fb_validate_r.status_code != 200:
            raise NotValidFbAccessToken

        exist_user = User.query.filter(User.fb_id == fb_id).first()

        if exist_user is None:
            if email is not None:
                exist_user = User.query.filter(User.email == email).first()

                if exist_user is None:
                    raise UserNotFound
            else:
                raise UserNotFound

        user_access_token = generate_client_access_token(exist_user.id)
        access_token = bcrypt.generate_password_hash(user_access_token)

        exist_user.fb_id = fb_id
        exist_user.fb_access_token = fb_access_token
        exist_user.access_token = access_token
        exist_user.is_activated = 1

        if exist_user.profile_thumb_url is None:
            profile_keyname = upload_fb_thumb(current_app, exist_user.id, fb_id)
            exist_user.profile_thumb_url = current_app.config[KEY_CDN_URL] + "/" + profile_keyname

        db.session.merge(exist_user)
        db.session.commit()

        session = Session(exist_user.id, user_access_token, exist_user.username)

        return session
