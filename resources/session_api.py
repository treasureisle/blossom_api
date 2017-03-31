# -*- coding:utf-8 -*-
from flask.ext.restful import Resource, reqparse, marshal_with

from common.api_errors import UserNotFound, NotValidAccessToken
from common.fields import session_fields
from common.models import User
from common.mods import bcrypt

__author__ = "Philgyu,Seong"
__email__ = "phil@treasureisle.co"

KEY_ID = "id"
KEY_ACCESS_TOKEN = "access_token"


class SessionApi(Resource):
    @marshal_with(session_fields, envelope="session")
    def post(self):
        post_parser = reqparse.RequestParser()
        post_parser.add_argument(KEY_ID, type=int, required=True)
        post_parser.add_argument(KEY_ACCESS_TOKEN, type=str, required=True)

        args = post_parser.parse_args()
        id = args[KEY_ID]
        access_token = args[KEY_ACCESS_TOKEN]

        user = User.query.filter(User.id == id).first()

        if user is None:
            raise UserNotFound

        if not bcrypt.check_password_hash(user.access_token, access_token):
            raise NotValidAccessToken

        return {}
