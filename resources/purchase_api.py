# -*- coding:utf-8 -*-

from flask.ext.restful import Resource, marshal_with, reqparse
from flask.ext.login import current_user

from common.mods import db
from common.fields import purchase_field
from common.api_errors import PostNotFound, PurchaseNotFound, Forbidden
from common.models import Post, Purchase
from utils import api_login_required, get_now_mysql_datetime

__author__ = "Philgyu,Seong"
__email__ = "philgyu.seong@gluvi.co"

KEY_POST_ID = "post_id"
KEY_COLOR_SIZE_ID = "color_size_id"
KEY_AMOUNT = "amount"
KEY_PRICE = "price"
KEY_PAYMENT = "payment"
KEY_NAME = "name"
KEY_ZIPCODE = "zipcode"
KEY_ADDRESS1 = "address1"
KEY_ADDRESS2 = "address2"
KEY_PHONE = "phone"
KEY_COMMENT = "comment"

LOCATION_FORM = "form"


class PurchaseApi(Resource):
    def __init__(self):
        self.post_parser = reqparse.RequestParser()
        self.post_parser.add_argument(KEY_POST_ID, location=LOCATION_FORM)
        self.post_parser.add_argument(KEY_COLOR_SIZE_ID, location=LOCATION_FORM)
        self.post_parser.add_argument(KEY_AMOUNT, location=LOCATION_FORM)
        self.post_parser.add_argument(KEY_PRICE, location=LOCATION_FORM)
        self.post_parser.add_argument(KEY_PAYMENT, location=LOCATION_FORM)
        self.post_parser.add_argument(KEY_NAME, location=LOCATION_FORM)
        self.post_parser.add_argument(KEY_ZIPCODE, location=LOCATION_FORM)
        self.post_parser.add_argument(KEY_ADDRESS1, location=LOCATION_FORM)
        self.post_parser.add_argument(KEY_ADDRESS2, location=LOCATION_FORM)
        self.post_parser.add_argument(KEY_PHONE, location=LOCATION_FORM)
        self.post_parser.add_argument(KEY_COMMENT, location=LOCATION_FORM)

    @api_login_required
    @marshal_with(purchase_field, "purchase")
    def get(self):

        purchase = Purchase.query.filter(Purchase.buyer_id == current_user.id).all()

        return purchase

    @api_login_required
    def post(self, id):
        post_id = id
        args = self.post_parser.parse_args()

        post = Post.query.filter(Post.id == post_id).first()

        if post is None:
            raise PostNotFound

        seller_id = post.user_id
        buyer_id = current_user.id
        color_size_id = int(args[KEY_COLOR_SIZE_ID])
        amount = int(args[KEY_AMOUNT])
        price = int(args[KEY_PRICE])
        payment = int(args[KEY_PAYMENT])
        name = args[KEY_NAME]
        zipcode = args[KEY_ZIPCODE]
        address1 = args[KEY_ADDRESS1]
        address2 = args[KEY_ADDRESS2]
        phone = args[KEY_PHONE]
        comment = args[KEY_COMMENT]

        new_purchase = Purchase(post_id=post_id, seller_id=seller_id, buyer_id=buyer_id, color_size_id=color_size_id,
                                amount=amount, price=price, payment=payment, name=name, zipcode=zipcode,
                                address1=address1, address2=address2, phone=phone, comment=comment,
                                creaetd_at=get_now_mysql_datetime())

        db.session.add(new_purchase)
        db.session.commit()

        return {}

    @api_login_required
    def delete(self, id):
        purchase_id = id
        purchase = Purchase.query.filter(Purchase.id == purchase_id).first()
        if purchase is None:
            raise PurchaseNotFound
        if purchase.user_id != current_user.id:
            raise Forbidden

        db.session.delete(purchase)
        db.session.commit()

        return {}
