# -*- coding:utf-8 -*-
from flask.ext.restful import Resource, marshal_with, reqparse

from common.api_errors import UserNotFound, WrongPassword
from common.fields import session_fields
from common.models import User, Session
from common.mods import bcrypt, db
from utils import generate_client_access_token

__author__ = "Philgyu,Seong"
__email__ = "philgyu.seong@gluvi.co"

KEY_EMAIL = "email"
KEY_PASSWORD = "password"


class SessionEmailApi(Resource):
    @marshal_with(session_fields, envelope="session")
    def post(self):
        post_parser = reqparse.RequestParser()
        post_parser.add_argument(KEY_EMAIL, type=str, required=True)
        post_parser.add_argument(KEY_PASSWORD, type=str, required=True)

        args = post_parser.parse_args()

        email = args[KEY_EMAIL]
        password = args[KEY_PASSWORD]

        user = User.query.filter(User.email == email).first()

        if user is None:
            raise UserNotFound

        if user.password is None or not bcrypt.check_password_hash(pw_hash=user.password, password=password):
            raise WrongPassword

        user_access_token = generate_client_access_token(id=user.id)
        user.access_token = bcrypt.generate_password_hash(user_access_token)

        db.session.merge(user)
        db.session.commit()

        session = Session(user.id, user_access_token, user.username)

        return session
