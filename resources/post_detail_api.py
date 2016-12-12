# -*- coding:utf-8 -*-

from flask.ext.restful import Resource, marshal_with

from common.models import Post
from common.fields import post_detail_field

__author__ = "Philgyu,Seong"
__email__ = "phil@treasureisle.co"


class PostDetailApi(Resource):
    def __init__(self):
        return

    @marshal_with(post_detail_field, envelope="post")
    def get(self, post_id):

        post = Post.query.filter(Post.id == post_id).first()

        return post
