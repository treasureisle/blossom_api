# -*- coding:utf-8 -*-

from flask.ext.restful import Resource, reqparse

from common.mods import db
from common.models import HashtagScore, Category
from common.api_errors import InternalServerError

__author__ = "Philgyu,Seong"
__email__ = "philgyu.seong@gluvi.co"

KEY_CATEGORY_ID = "category_id"

LOCATION_FORM = "form"


class HashtagScoreApi(Resource):
    def __init__(self):
        self.post_parser = reqparse.RequestParser()
        self.post_parser.add_argument(KEY_CATEGORY_ID, location=LOCATION_FORM)

    def post(self, hashtag_id):
        args = self.post_parser.parse_args()
        category_id = args[KEY_CATEGORY_ID]

        self.recognize_score(hashtag_id, category_id)

        return

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

        return


