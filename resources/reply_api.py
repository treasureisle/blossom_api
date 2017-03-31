# -*- coding:utf-8 -*-

from flask.ext.restful import Resource, marshal_with, reqparse
from flask.ext.login import current_user
from flask.globals import request

from common.mods import db
from common.fields import reply_field
from common.api_errors import PostNotFound, ReplyNotFound, Forbidden
from common.models import Post, Reply
from common.service_configs import REPLY_ROW
from utils import get_page_offset, api_login_required, get_now_mysql_datetime

__author__ = "Philgyu,Seong"
__email__ = "philgyu.seong@gluvi.co"

KEY_ROW = "row"
KEY_PAGE = "page"

KEY_TEXT = "text"
KEY_PARENT_ID = "parent_id"

LOCATION_FORM = "form"


class ReplyApi(Resource):
    def __init__(self):
        self.post_parser = reqparse.RequestParser()
        self.post_parser.add_argument(KEY_TEXT, location=LOCATION_FORM)
        self.post_parser.add_argument(KEY_PARENT_ID, location=LOCATION_FORM)

    @marshal_with(reply_field, "replies")
    def get(self, id):
        post_id = id
        row = int(request.args.get(KEY_ROW, default=REPLY_ROW))
        page = int(request.args.get(KEY_PAGE, default=1))

        replies = Reply.query.filter(Reply.post_id == post_id).order_by(Reply.id.desc()).offset(get_page_offset(page, row)).limit(row).all()

        return replies

    @api_login_required
    def post(self, id):
        post_id = id

        args = self.post_parser.parse_args()

        post = Post.query.filter(Post.id == post_id).first()

        if post is None:
            raise PostNotFound

        text = args[KEY_TEXT]
        parent_id = args[KEY_PARENT_ID]

        if parent_id is None:
            parent_id = 0
            depth = 0
        else:
            parent = Reply.query.filter(Reply.id == parent_id).first()
            if parent is None:
                raise ReplyNotFound
            depth = parent.depth + 1

        print "userId: %d, postId: %d, text: %s, parent_id: %d, depth: %d" % (current_user.id, post_id, text, parent_id,
                                                                              depth)

        new_reply = Reply(user_id=current_user.id, post_id=post_id, text=text, created_at=get_now_mysql_datetime(),
                          parent_id=parent_id, depth=depth)

        db.session.add(new_reply)

        replies = Reply.query.filter(Reply.post_id == post_id).count()

        post.replies = replies

        db.session.merge(post)
        db.session.commit()

        return ""

    @api_login_required
    def delete(self, id):
        reply_id = id
        reply = Reply.query.filter(Reply.id == reply_id).first()
        if reply is None:
            raise ReplyNotFound
        if reply.user_id != current_user.id:
            raise Forbidden

        post = Post.query.filter(Post.id == reply.post_id).first()
        if post is None:
            raise PostNotFound
        post.replies -= 1

        db.session.delete(reply)
        db.session.merge(post)
        db.session.commit()

        return ""
