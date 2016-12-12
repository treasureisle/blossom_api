# -*- coding:utf-8 -*-

from flask.ext.restful import Resource
from flask.ext.login import current_user

from common.api_errors import AlreadyVoted, MyVoteNotFound, Forbidden, PostNotFound
from common.models import Like, Post
from common.mods import db
from utils import api_login_required, get_now_mysql_datetime

__author__ = "Philgyu,Seong"
__email__ = "phil@treasureisle.co"

KEY_POST_ID = "post_id"


class LikeApi(Resource):
    @api_login_required
    def post(self, id):

        like = Like.query.filter(Like.user_id==current_user.id).filter(Like.post_id == id).first()
        post = Post.query.filter(Post.id == id).first()

        if like is not None:
            raise AlreadyVoted

        if post is None:
            raise PostNotFound

        like = Like(user_id=current_user.id, post_id=id, created_at=get_now_mysql_datetime())
        post.likes += 1

        db.session.add(like)
        db.session.merge(post)
        db.session.commit()

        return

    @api_login_required
    def delete(self, id):
        like = Like.query.filter(Like.id == id).first()

        if like is None:
            raise MyVoteNotFound

        post = Post.query.filter(Post.id == like.post_id).first()

        if post is None:
            raise PostNotFound

        if like.user_id != current_user.id:
            raise Forbidden

        post.likes -= 1

        db.session.delete(like)
        db.session.merge(post)
        db.session.commit()

        return
