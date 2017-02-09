# -*- coding:utf-8 -*-

from flask.ext.restful import Resource, marshal_with, reqparse
from flask.ext.login import current_user

from common.mods import db
from common.fields import basket_field
from common.api_errors import PostNotFound, BasketNotFound, Forbidden
from common.models import Post, Basket
from utils import api_login_required, get_now_mysql_datetime

__author__ = "Philgyu,Seong"
__email__ = "philgyu.seong@gluvi.co"

KEY_COLOR_SIZE_ID = "color_size_id"
KEY_AMOUNT = "amount"


LOCATION_FORM = "form"


class BasketApi(Resource):
    def __init__(self):
        self.post_parser = reqparse.RequestParser()
        self.post_parser.add_argument(KEY_COLOR_SIZE_ID, location=LOCATION_FORM)
        self.post_parser.add_argument(KEY_AMOUNT, location=LOCATION_FORM)

    @api_login_required
    @marshal_with(basket_field, "basket")
    def get(self):

        basket = Basket.query.filter(Basket.user_id == current_user.id).all()

        return basket

    @api_login_required
    def post(self, id):
        post_id = id
        args = self.post_parser.parse_args()

        post = Post.query.filter(Post.id == post_id).first()

        if post is None:
            raise PostNotFound

        color_size_id = int(args[KEY_COLOR_SIZE_ID])
        amount = int(args[KEY_AMOUNT])

        new_basket = Basket(user_id=current_user.id, post_id=post_id, color_size_id=color_size_id, amount=amount,
                            created_at=get_now_mysql_datetime())

        db.session.add(new_basket)
        db.session.commit()

        return

    @api_login_required
    def delete(self, id):
        basket_id = id
        basket = Basket.query.filter(Basket.id == basket_id).first()
        if basket is None:
            raise BasketNotFound
        if basket.user_id != current_user.id:
            raise Forbidden

        db.session.delete(basket)
        db.session.commit()

        return
