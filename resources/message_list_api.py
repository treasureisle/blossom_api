# -*- coding:utf-8 -*-

from flask.ext.restful import Resource, marshal_with, marshal
from flask.ext.login import current_user

from common.fields import user_message_fields
from common.models import User, Message
from utils import api_login_required

__author__ = "Philgyu,Seong"
__email__ = "philgyu.seong@gluvi.co"

KEY_ROW = "row"
KEY_PAGE = "page"

LOCATION_FORM = "form"


class MessageListApi(Resource):
    @api_login_required
    @marshal_with(user_message_fields, "user_messages")
    def get(self):

        messages = Message.query.filter("('(sender_id=:id1) or (reciever_id=:id2)')").\
            params(id1=current_user.id, id2=current_user.id).all()

        user_ids = []

        for message in messages:
            if message.sender_id != current_user.id:
                if message.sender_id not in user_ids:
                    user_ids.append(message.sender_id)
            else:
                if message.reciever_id not in user_ids:
                    user_ids.append(message.reciever_id)

        users = User.query.filter(User.id.in_(user_ids)).all()

        for user in users:
            message = Message.query.\
                filter("('(sender_id=:id1 and reciever_id=:id2) or (sender_id=:id3 and reciever_id=:id4)')").\
                params(id1=current_user.id, id2=user.id, id3=user.id, id4=current_user.id).first()
            user.last_message = message.message
            user.last_message_created_at = message.created_at
            user.is_read = message.is_read

        return users

