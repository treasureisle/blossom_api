# -*- coding:utf-8 -*-

from flask.ext.restful import Resource, marshal_with
from flask.ext.login import current_user

from common.api_errors import UserNotFound, FollowNotFound
from common.models import User, Follow
from common.fields import follower_field
from utils import api_login_required

__author__ = "Philgyu,Seong"
__email__ = "philgyu.seong@gluvi.co"

KEY_FOLLOWING = "following"


class IsFollowingApi(Resource):
    # @marshal_with(follower_field, envelope="follow")
    @api_login_required
    def get(self, user_id):
        user = User.query.filter(User.id == user_id).first()

        if user is None:
            raise UserNotFound

        follow = Follow.query.filter(Follow.follower_id == current_user.id).\
            filter(Follow.following_id == user_id).first()

        if follow is None:
            raise FollowNotFound

        return ""
