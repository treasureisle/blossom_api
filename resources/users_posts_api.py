# -*- coding:utf-8 -*-

from flask.ext.restful import Resource, marshal_with
from flask.globals import request

from common.api_errors import NotAllowedOrderType
from common.models import Post, User
from common.fields import post_field
from common.service_configs import POST_ROW
from utils import get_page_offset

__author__ = "Philgyu,Seong"
__email__ = "philgyu.seong@gluvi.co"

KEY_POST_TYPE = "post_type"
KEY_ORDER = "order"
KEY_ROW = "row"
KEY_PAGE = "page"

ORDER_SCORE = "score"

POST_TYPE_SELL = "sell"
POST_TYPE_BUY = "buy"
POST_TYPE_REVIEW = "review"
POST_TYPE_STORE = "store"


class UsersPostsApi(Resource):
    @marshal_with(post_field, envelope="posts")
    def get(self, user_id):

        post_type = request.args.get(KEY_POST_TYPE, default=POST_TYPE_SELL)
        row = int(request.args.get(KEY_ROW, default=POST_ROW))
        page = int(request.args.get(KEY_PAGE, default=1))
        order = request.args.get(KEY_ORDER, default=ORDER_SCORE)

        post_type_code = 0

        if post_type == POST_TYPE_BUY:
            post_type_code = 1
        elif post_type == POST_TYPE_REVIEW:
            post_type_code = 2
        elif post_type == POST_TYPE_STORE:
            post_type_code = 3

        if post_type == 0:
            posts = Post.query.filter(Post.user_id == user_id).order_by(Post.score.desc()).\
                offset(get_page_offset(page, row)).limit(row).all()

            return posts

        if order == ORDER_SCORE:
            posts = Post.query.filter(Post.user_id == user_id).filter(Post.post_type == post_type_code).\
                order_by(Post.score.desc()).offset(get_page_offset(page, row)).limit(row).all()

            return posts
        else:
            raise NotAllowedOrderType
