# -*- coding:utf-8 -*-

from flask.ext.restful import Resource
from flask.ext.login import current_user

from common.api_errors import AlreadyVoted, MyVoteNotFound, Forbidden, PostNotFound
from common.models import ReplyLike, Reply
from common.mods import db
from utils import api_login_required, get_now_mysql_datetime

__author__ = "Philgyu,Seong"
__email__ = "phil@treasureisle.co"

KEY_POST_ID = "post_id"


class ReplyLikeApi(Resource):
    @api_login_required
    def post(self, id):

        like = ReplyLike.query.filter(ReplyLike.user_id == current_user.id).filter(ReplyLike.reply_id == id).first()
        reply = Reply.query.filter(Reply.id == id).first()

        if like is not None:
            raise AlreadyVoted

        if reply is None:
            raise PostNotFound

        like = ReplyLike(user_id=current_user.id, reply_id=id, created_at=get_now_mysql_datetime())
        reply.likes += 1

        db.session.add(like)
        db.session.merge(reply)
        db.session.commit()

        return

    @api_login_required
    def delete(self, id):
        reply = Reply.query.filter(Reply.id == id).first()

        if reply is None:
            raise PostNotFound

        like = ReplyLike.query.filter(ReplyLike.reply_id == reply.id).\
            filter(ReplyLike.user_id == current_user.id).first()

        if like is None:
            raise MyVoteNotFound

        reply.likes -= 1

        db.session.delete(like)
        db.session.merge(reply)
        db.session.commit()

        return
