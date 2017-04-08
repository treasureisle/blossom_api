# -*- coding:utf-8 -*-

from flask.ext.restful import Resource, reqparse, marshal_with

from common.mods import db
from common.models import HashtagScore, Category, Hashtag
from common.api_errors import InternalServerError
from common.fields import hashtag_field

__author__ = "Philgyu,Seong"
__email__ = "philgyu.seong@gluvi.co"

KEY_CATEGORY_ID = "category_id"

LOCATION_FORM = "form"


class HashtagScoreApi(Resource):
    def __init__(self):
        self.post_parser = reqparse.RequestParser()
        self.post_parser.add_argument(KEY_CATEGORY_ID, location=LOCATION_FORM)

    @marshal_with(hashtag_field, envelope="hashtags")
    def get(self, id):
        category_id = id

        hashtag_scores = HashtagScore.query.filter(HashtagScore.category_id == category_id).\
            order_by(HashtagScore.score.desc()).limit(3).all()

        hashtag_ids = [hashtag_score.hashtag_id for hashtag_score in hashtag_scores]

        hashtags = Hashtag.query.filter(Hashtag.id.in_(hashtag_ids)).all()

        return hashtags

    def post(self, id):
        hashtag_id = id
        args = self.post_parser.parse_args()
        category_id = args[KEY_CATEGORY_ID]

        self.recognize_score(hashtag_id, category_id)

        return {}

    def recognize_score(self, hashtag_id, category_id):
        category = Category.query.filter(Category.id == category_id).first()

        if category is None:
            raise InternalServerError

        hashtag_score = HashtagScore.query.filter(HashtagScore.hashtag_id == hashtag_id).\
            filter(HashtagScore.category_id == category_id).first()

        if hashtag_score is None:
            raise InternalServerError

        hashtag_score.score += 1

        db.session.merge(hashtag_score)
        db.session.commit()

        if category.parent_id != 0:
            self.recognize_score(hashtag_id, category.parent_id)

        return {}


