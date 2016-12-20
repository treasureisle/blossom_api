# -*- coding:utf-8 -*-

from flask.ext.restful import Resource, marshal_with, reqparse
from flask.ext.login import current_user
from flask.globals import request

from common.mods import db
from common.fields import reply_field
from common.api_errors import PostNotFound
from common.models import Post, Reply
from common.service_configs import REPLY_ROW
from utils import get_page_offset, api_login_required, get_now_mysql_datetime

__author__ = "Philgyu,Seong"
__email__ = "philgyu.seong@gluvi.co"

KEY_ROW = "row"
KEY_PAGE = "page"

KEY_TEXT = "text"

LOCATION_FORM = "form"


class ReplyApi(Resource):
    def __init__(self):
        self.post_parser = reqparse.RequestParser()
        self.post_parser.add_argument(KEY_TEXT, location=LOCATION_FORM)

    @marshal_with(reply_field, "replies")
    def get(self, post_id):
        row = int(request.args.get(KEY_ROW, default=REPLY_ROW))
        page = int(request.args.get(KEY_PAGE, default=1))

        replys = Reply.query.filter(Reply.post_id == post_id).offset(get_page_offset(page, row)).limit(row).all()

        return replys

    @api_login_required
    def post(self, post_id):
        args = self.post_parser.parse_args()

        post = Post.query.filter(Post.id == post_id).first()

        if post is None:
            raise PostNotFound

        text = args[KEY_TEXT]

        new_reply = Reply(user_id=current_user.id, post_id=post_id, text=text, created_at=get_now_mysql_datetime)

        db.session.add(new_reply)
        db.session.commint()

        return