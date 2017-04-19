# -*- coding:utf-8 -*-

from flask.ext.restful import Resource, marshal_with, reqparse
from flask.ext.login import current_user
from flask.globals import request

from common.mods import db
from common.fields import message_field
from common.models import User, Notification
from common.api_errors import UserNotFound
from utils import get_page_offset, api_login_required, get_now_mysql_datetime

__author__ = "Philgyu,Seong"
__email__ = "philgyu.seong@gluvi.co"


KEY_CODE = "code"
KEY_MESSAGE = "message"

LOCATION_FORM = "form"


class NotificationApi(Resource):
    def __init__(self):
        self.post_parser = reqparse.RequestParser()
        self.post_parser.add_argument(KEY_MESSAGE, location=LOCATION_FORM)

    @api_login_required
    @marshal_with(message_field, "notification")
    def get(self):

        notifications = Notification.query.filter(Notification.user_id == current_user.id).\
            filter(Notification.is_read is False).all()

        return notifications
