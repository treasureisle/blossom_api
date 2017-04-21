# -*- coding:utf-8 -*-

from flask.ext.restful import Resource, marshal_with
from flask.ext.login import current_user

from common.fields import message_timestamp_field
from common.models import MessageTimestamp
__author__ = "Philgyu,Seong"
__email__ = "philgyu.seong@gluvi.co"


class MessageTimestampApi(Resource):

    @marshal_with(message_timestamp_field, "timestamp")
    def get(self):

        timestamp = MessageTimestamp.query.filter(MessageTimestamp.user_id == current_user.id).first()

        if timestamp is None:
            return {}

        return timestamp
