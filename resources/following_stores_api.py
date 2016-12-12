# -*- coding:utf-8 -*-

from flask.ext.restful import Resource, marshal_with
from flask.globals import request

from common.api_errors import UserNotFound
from common.models import Post, Like, User
from common.fields import post_field
from common.service_configs import POST_ROW
from utils import get_page_offset

__author__ = "Philgyu,Seong"
__email__ = "phil@treasureisle.co"

KEY_ROW = "row"
KEY_PAGE = "page"

ORDER_SCORE = "score"


class FollowingStoresApi(Resource):
    @marshal_with(post_field, envelope="posts")
    def get(self, user_id):
        # 정책 불확실, 추후 구현
        user = User.query.filter(User.id == user_id).first()

        if user is None:
            raise UserNotFound

        row = int(request.args.get(KEY_ROW, default=POST_ROW))
        page = int(request.args.get(KEY_PAGE, default=1))

        likes = Like.query.filter(Like.user_id == user_id).all()

        liked_post_ids = [like.post_id for like in likes]

        posts = Post.query.filter(Post.id.in_(liked_post_ids)).order_by(Post.score.desc()).\
                offset(get_page_offset(page, row)).limit(row).all()

        return posts
