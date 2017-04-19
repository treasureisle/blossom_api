# -*- coding:utf-8 -*-

from flask.ext.restful import Resource, marshal_with
from flask.ext.login import current_user

from common.fields import user_fields
from common.models import User, Message
from utils import api_login_required

__author__ = "Philgyu,Seong"
__email__ = "philgyu.seong@gluvi.co"

KEY_ROW = "row"
KEY_PAGE = "page"

LOCATION_FORM = "form"


class MessageListApi(Resource):
    @api_login_required
    @marshal_with(user_fields, "users")
    def get(self):

        messages = Message.query.filter("(sender_id=:id1) or (reciever_id=:id2)").\
            params(id1=current_user.id, id2=current_user.id).all()

        user_ids = []

        for message in messages:
            if message.sender_id != current_user.id:
                if message.sender_id not in user_ids:
                    user_ids.append(message.sender_id)
            else:
                if message.reciever_id not in user_ids:
                    user_ids.append(message.reciever_id)

        users = User.query.filter(User.user_id.in_(user_ids)).all()

        return users

