# -*- coding:utf-8 -*-

from flask.ext.restful import Resource, marshal_with, reqparse
from flask.ext.login import current_user
from flask.globals import request

from common.mods import db
from common.fields import message_field
from common.models import User, Message
from common.service_configs import MESSAGE_ROW
from common.api_errors import UserNotFound
from utils import get_page_offset, api_login_required, get_now_mysql_datetime

__author__ = "Philgyu,Seong"
__email__ = "philgyu.seong@gluvi.co"

KEY_ROW = "row"
KEY_PAGE = "page"

KEY_MESSAGE = "message"

LOCATION_FORM = "form"


class MessageApi(Resource):
    def __init__(self):
        self.post_parser = reqparse.RequestParser()
        self.post_parser.add_argument(KEY_MESSAGE, location=LOCATION_FORM)

    @marshal_with(message_field, "messages")
    def get(self, user_id):
        row = int(request.args.get(KEY_ROW, default=MESSAGE_ROW))
        page = int(request.args.get(KEY_PAGE, default=1))

        id1 = current_user.id
        id2 = user_id

        messages = Message.query.\
            filter("(sender_id=:id1 and reciever_id=:id2) or (sender_id=:id3 and reciever_id=:id4)").\
            params(id1=id1, id2=id2, id3=id2, id4=id1).offset(get_page_offset(page, row)).limit(row).all()

        return messages

    @api_login_required
    def post(self, user_id):
        sender_id = current_user.id
        reciever_id = user_id

        args = self.post_parser.parse_args()

        user = User.query.filter(User.id == reciever_id).first()

        if user is None:
            raise UserNotFound

        message = args[KEY_MESSAGE]

        new_message = Message(sender_id=sender_id, reciever_id=reciever_id, message=message,
                              created_at=get_now_mysql_datetime())

        db.session.add(new_message)
        db.session.commit()

        return ""
