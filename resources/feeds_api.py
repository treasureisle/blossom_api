# -*- coding:utf-8 -*-

from flask.ext.restful import Resource, marshal_with
from flask.ext.login import current_user
from flask.globals import request

from common.models import Post, User, Follow
from common.fields import post_field
from common.service_configs import POST_ROW
from utils import get_page_offset, api_login_required

__author__ = "Philgyu,Seong"
__email__ = "phil@treasureisle.co"

KEY_POST_TYPE = "post_type"
KEY_ORDER = "order"
KEY_ROW = "row"
KEY_PAGE = "page"

ORDER_SCORE = "score"

POST_TYPE_SELL = "sell"
POST_TYPE_COMMON = "common"


class FeedsApi(Resource):
    @api_login_required
    @marshal_with(post_field, envelope="posts")
    def get(self):
        def get_following(user_id):
            following = User.query.filter(Follow.follower_id == user_id).filter(User.id == Follow.following_id).\
                order_by(Follow.id.desc()).all()

            return following

        following = get_following(current_user.id)

        following_ids = [following_user.id for following_user in following]
        following_ids.append(current_user.id)

        row = int(request.args.get(KEY_ROW, default=POST_ROW))
        page = int(request.args.get(KEY_PAGE, default=1))
        order = request.args.get(KEY_ORDER, default=ORDER_SCORE)
        post_type = request.args.get(KEY_POST_TYPE, default=POST_TYPE_SELL)

        if post_type == POST_TYPE_SELL:
            posts = Post.query.filter(Post.user_id.in_(following_ids)).filter(Post.post_type == 0).\
                order_by(Post.score.desc()).offset(get_page_offset(page, row)).limit(row).all()

            return posts

        posts = Post.query.filter(Post.user_id.in_(following_ids)).filter(Post.post_type != 0).\
            order_by(Post.score.desc()).offset(get_page_offset(page, row)).limit(row).all()

        return posts
