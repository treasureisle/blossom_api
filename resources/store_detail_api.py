# -*- coding:utf-8 -*-

from flask.ext.restful import Resource, reqparse, marshal_with
from flask.ext.login import current_user
from flask.globals import current_app, request
from PIL import Image

from common.mods import db
from common.api_errors import PostNotFound
from common.models import Post, HashtagPost
from common.fields import post_field
from common.service_configs import POST_ROW
from utils import get_page_offset

__author__ = "Philgyu,Seong"
__email__ = "philgyu.seong@gluvi.co"

KEY_ORDER = "order"
KEY_ROW = "row"
KEY_PAGE = "page"

ORDER_SCORE = "score"


class StoreDetailApi(Resource):
    @marshal_with(post_field, envelope="posts")
    def get(self, hashtag_id):

        row = int(request.args.get(KEY_ROW, default=POST_ROW))
        page = int(request.args.get(KEY_PAGE, default=1))
        # order = request.args.get(KEY_ORDER, default=ORDER_SCORE)

        post_type_code = 1

        hashtag_posts = HashtagPost.query.filter(HashtagPost.hashtag_id == hashtag_id).all()
        post_ids = [hashtag_post.post_id for hashtag_post in hashtag_posts]

        result = Post.query.filter(Post.id.in_(post_ids)).filter(Post.post_type == post_type_code).\
            order_by(Post.score.desc()).offset(get_page_offset(page, row)).limit(row).all()

        if result is None:
            raise PostNotFound

        return result
