# -*- coding:utf-8 -*-

from flask.ext.restful import Resource, marshal_with, reqparse
from flask.ext.login import current_user

from common.api_errors import UserNotFound, FollowNotFound, Forbidden
from common.fields import follow_wrapper
from common.models import Follow, User
from common.mods import db
from utils import api_login_required, get_now_mysql_datetime

__author__ = "Philgyu,Seong"
__email__ = "philgyu.seong@gluvi.co"


class FollowApi(Resource):
    @marshal_with(follow_wrapper)
    def get(self, id):
        followings = Follow.query.filter(Follow.follower_id == id).all()
        followers = Follow.query.filter(Follow.following_id == id).all()

        follow_wrapper = {
            "followings": followings,
            "followers": followers
        }

        return follow_wrapper

    @api_login_required
    def post(self, id):
        following = User.query.filter(User.id == id).first()

        if following is None:
            raise UserNotFound

        follow = Follow(follower_id=current_user.id, following_id=id, created_at=get_now_mysql_datetime())
        db.session.add(follow)
        db.session.commit()

        return

    @api_login_required
    def delete(self, id):
        follow = Follow.query.filter(Follow.id == id).first()

        if follow is None:
            raise FollowNotFound

        if follow.follower_id != current_user.id:
            raise Forbidden

        db.session.delete(follow)
        db.session.commit()

        return
