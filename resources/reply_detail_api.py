# -*- coding:utf-8 -*-

from flask.ext.restful import Resource, marshal_with
from flask.globals import request

from common.fields import reply_field
from common.models import Reply
from common.service_configs import REPLY_ROW
from utils import get_page_offset
__author__ = "Philgyu,Seong"
__email__ = "philgyu.seong@gluvi.co"

KEY_ROW = "row"
KEY_PAGE = "page"

LOCATION_FORM = "form"


class ReplyDetailApi(Resource):

    @marshal_with(reply_field, "replies")
    def get(self, id, parent_id):
        post_id = id
        row = int(request.args.get(KEY_ROW, default=REPLY_ROW))
        page = int(request.args.get(KEY_PAGE, default=1))

        replies = Reply.query.filter(Reply.post_id == post_id).filter(Reply.parent_id == parent_id).order_by(Reply.id.desc()).offset(get_page_offset(page, row)).limit(row).all()

        return replies
