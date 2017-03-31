# -*- coding:utf-8 -*-

from flask.ext.restful import Resource, reqparse, marshal_with
from flask.ext.login import current_user

from common.mods import db
from common.api_errors import PostNotFound, Forbidden
from common.models import Post, Hashtag, HashtagPost, HashtagScore, Category
from common.fields import hashtag_field
from utils import api_login_required, get_now_mysql_datetime

__author__ = "Philgyu,Seong"
__email__ = "phil@treasureisle.co"

KEY_COUNT = "count"
KEY_NAME = ["name1", "name2", "name3", "name4", "name5"]

LOCATION_FORM = "form"


class HashtagApi(Resource):
    def __init__(self):
        self.post_parser = reqparse.RequestParser()
        self.post_parser.add_argument(KEY_COUNT, location=LOCATION_FORM, required=True)
        self.post_parser.add_argument(KEY_NAME[0], location=LOCATION_FORM)
        self.post_parser.add_argument(KEY_NAME[1], location=LOCATION_FORM)
        self.post_parser.add_argument(KEY_NAME[2], location=LOCATION_FORM)
        self.post_parser.add_argument(KEY_NAME[3], location=LOCATION_FORM)
        self.post_parser.add_argument(KEY_NAME[4], location=LOCATION_FORM)

    @marshal_with(hashtag_field, envelope="hashtag")
    def get(self, post_id):

        post = Post.query.filter(Post.id == post_id).first()

        if post is None:
            raise PostNotFound

        hashtags = Hashtag.query.join(HashtagPost, HashtagPost.hashtag_id == Hashtag.id).\
            filter(HashtagPost.post_id == post_id).all()

        return hashtags

    @marshal_with(hashtag_field, envelope="hashtag")
    @api_login_required
    def post(self, post_id):
        args = self.post_parser.parse_args()

        print args

        post = Post.query.filter(Post.id == post_id).first()

        if post is None:
            raise PostNotFound

        if post.user_id != current_user.id:
            raise Forbidden

        count = int(args[KEY_COUNT])

        print count

        for num in range(0, count):
            name = args[KEY_NAME[num]]

            hashtag = Hashtag.query.filter(Hashtag.name==name).first()

            if hashtag is None:
                hashtag = Hashtag(name=name, created_at=get_now_mysql_datetime())
                db.session.add(hashtag)
                db.session.flush()
                db.session.refresh(hashtag)

                categories = Category.query.all()

                for category in categories:
                    hashtag_score = HashtagScore(hashtag.id, category.id)
                    db.session.add(hashtag_score)

            db.session.flush()
            db.session.refresh(hashtag)

            hashtag.number += 1

            hashtag_post = HashtagPost(hashtag_id=hashtag.id, post_id=post_id, created_at=get_now_mysql_datetime())
            db.session.add(hashtag_post)

        db.session.commit()

        return hashtag

