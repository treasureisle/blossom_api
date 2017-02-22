# -*- coding:utf-8 -*-

import sys

from flask import Flask
from common.mods import db
from common.api_errors import errors
from common.models import User

from resources.users_api import UsersApi
from resources.session_api import SessionApi
from resources.session_email_api import SessionEmailApi
from resources.posts_api import PostsApi
from resources.post_detail_api import PostDetailApi
from resources.color_size_api import ColorSizeApi
from resources.hashtag_api import HashtagApi
from resources.follow_api import FollowApi
from resources.liked_post_api import LikedPostApi
from resources.following_stores_api import FollowingStoresApi
from resources.like_api import LikeApi
from resources.user_posts_api import UserPostsApi
from resources.is_following_api import IsFollowingApi
from resources.feeds_api import FeedsApi
from resources.search_post_api import SearchPostApi
from resources.search_user_api import SearchUserApi
from resources.reply_api import ReplyApi
from resources.reply_like_api import ReplyLikeApi
from resources.basket_api import BasketApi
from resources.purchase_api import PurchaseApi
from resources.message_api import MessageApi
from resources.user_detail_api import UserDetailApi
from resources.category_api import CategoryApi
from resources.hashtag_score_api import HashtagScoreApi

from common.mods import api, bcrypt, login_manager

__author__ = "Philgyu, Seong"
__email__ = "phil@treasureisle.co"


def register_apis():
    api.add_resource(UsersApi, "/users", "/users/<int:user_id>")
    api.add_resource(SessionApi, "/session")
    api.add_resource(SessionEmailApi, "/session/email")
    api.add_resource(PostsApi, "/posts")
    api.add_resource(PostDetailApi, "/post/<int:post_id>")
    api.add_resource(ColorSizeApi, "/color_sizes/<int:post_id>")
    api.add_resource(HashtagApi, "/hashtags/<int:post_id>")
    api.add_resource(FollowApi, "/follow", "/follow/<int:id>")
    api.add_resource(LikedPostApi, "/liked_posts/<int:user_id>")
    api.add_resource(FollowingStoresApi, "/following_stores/<int:user_id>")
    api.add_resource(LikeApi, "/like/<int:id>")
    api.add_resource(UserPostsApi, "/user_posts/<int:user_id>")
    api.add_resource(IsFollowingApi, "/is_following/<int:user_id>")
    api.add_resource(FeedsApi, "/feeds")
    api.add_resource(SearchPostApi, "/search_post")
    api.add_resource(SearchUserApi, "/search_user")
    api.add_resource(ReplyApi, "/reply/<int:id>")
    api.add_resource(ReplyLikeApi, "/reply_like/<int:id>")
    api.add_resource(BasketApi, "/basket", "/basket/<int:id>")
    api.add_resource(PurchaseApi, "/purchase", "/purchase/<int:id>")
    api.add_resource(MessageApi, "/message/<int:user_id>")
    api.add_resource(UserDetailApi, "/user_detail/<int:user_id>")
    api.add_resource(CategoryApi, "/category")
    api.add_resource(HashtagScoreApi, "/hashtag_score/<int:hashtag_id>")


# noinspection PyUnusedLocal
def init_login():
    # noinspection PyUnusedLocal
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.filter(User.id == user_id).first()

    # noinspection PyUnusedLocal
    @login_manager.header_loader
    def load_user_from_header(header_val):
        splits = header_val.split(":")
        id = splits[0]
        access_token = splits[1]

        user = load_user(id)
        if user is not None and bcrypt.check_password_hash(user.access_token, access_token):
            return user
        return None

reload(sys)
sys.setdefaultencoding('utf-8')

app = Flask(__name__)
app.config.from_pyfile("configs.py")
app.config.from_envvar("TREASUREISLE_CONFIGS")

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

register_apis()

db.init_app(app)
api.init_app(app)
api.errors = errors

login_manager.init_app(app)

init_login()

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
