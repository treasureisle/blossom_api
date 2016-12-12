# -*- coding:utf-8 -*-

from flask.ext.restful import Resource, reqparse, marshal_with
from flask.ext.login import current_user

from common.mods import db
from common.api_errors import PostNotFound, Forbidden
from common.models import Post, ColorSize
from common.fields import color_size_field
from utils import api_login_required, get_now_mysql_datetime

__author__ = "Philgyu,Seong"
__email__ = "phil@treasureisle.co"

KEY_COUNT = "count"
KEY_NAME = []
KEY_AVAILABLE = []
KEY_NAME.append("name1")
KEY_AVAILABLE.append("available1")
KEY_NAME.append("name2")
KEY_AVAILABLE.append("available2")
KEY_NAME.append("name3")
KEY_AVAILABLE.append("available3")
KEY_NAME.append("name4")
KEY_AVAILABLE.append("available4")
KEY_NAME.append("name5")
KEY_AVAILABLE.append("available5")

LOCATION_FORM = "form"


class ColorSizeApi(Resource):
    def __init__(self):
        self.post_parser = reqparse.RequestParser()
        self.post_parser.add_argument(KEY_COUNT, location=LOCATION_FORM, required=True)
        self.post_parser.add_argument(KEY_NAME[0], location=LOCATION_FORM, required=True)
        self.post_parser.add_argument(KEY_AVAILABLE[0], location=LOCATION_FORM, required=True)
        self.post_parser.add_argument(KEY_NAME[1], location=LOCATION_FORM)
        self.post_parser.add_argument(KEY_AVAILABLE[1], location=LOCATION_FORM)
        self.post_parser.add_argument(KEY_NAME[2], location=LOCATION_FORM)
        self.post_parser.add_argument(KEY_AVAILABLE[2], location=LOCATION_FORM)
        self.post_parser.add_argument(KEY_NAME[3], location=LOCATION_FORM)
        self.post_parser.add_argument(KEY_AVAILABLE[3], location=LOCATION_FORM)
        self.post_parser.add_argument(KEY_NAME[4], location=LOCATION_FORM)
        self.post_parser.add_argument(KEY_AVAILABLE[4], location=LOCATION_FORM)

    @marshal_with(color_size_field, envelope="color_sizes")
    def get(self, post_id):
        post = Post.query.filter(Post.id == post_id).first()

        if post is None:
            raise PostNotFound

        color_sizes = ColorSize.query.filter(ColorSize.post_id == post_id).all()

        return color_sizes

    @api_login_required
    def post(self, post_id):

        args = self.post_parser.parse_args()

        post = Post.query.filter(Post.id == post_id).first()

        if post is None:
            raise PostNotFound

        if post.user_id != current_user.id:
            raise Forbidden

        print(args)
        print(args[KEY_COUNT])

        count = int(args[KEY_COUNT])

        for num in range(0, count):
            name = args[KEY_NAME[num]]
            available = int(args[KEY_AVAILABLE[num]])
            new_color_size = ColorSize(post_id=post_id, name=name, available=available,
                                       created_at=get_now_mysql_datetime())
            db.session.add(new_color_size)

        db.session.commit()

        return count

