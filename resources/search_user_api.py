# -*- coding:utf-8 -*-

from flask.ext.restful import Resource, marshal_with, reqparse

from common.fields import user_fields
from common.api_errors import UserNotFound
from common.models import User

__author__ = "Philgyu,Seong"
__email__ = "philgyu.seong@gluvi.co"

KEY_KEYWORD = "keyword"

KEY_SEARCH_TYPE_TITLE = "title"
KEY_SEARCH_TYPE_HASHTAG = "hashtag"

LOCATION_FORM = "form"


class SearchUserApi(Resource):
    def __init__(self):
        self.post_parser = reqparse.RequestParser()
        self.post_parser.add_argument(KEY_KEYWORD, location=LOCATION_FORM)

    @marshal_with(user_fields, envelope="users")
    def post(self):
        args = self.post_parser.parse_args()

        keyword = args[KEY_KEYWORD]

        result = User.query.filter(User.username.like('%'+keyword+'%')).all()

        if result is None:
            raise UserNotFound

        return result
