# -*- coding:utf-8 -*-

from flask.ext.restful import Resource, marshal_with, reqparse
from flask.ext.login import current_user

from common.mods import db
from common.api_errors import PurchaseNotFound, Forbidden
from common.fields import purchase_field
from common.models import Purchase
from utils import api_login_required

__author__ = "Philgyu,Seong"
__email__ = "philgyu.seong@gluvi.co"

KEY_DELIVERY_CODE = "delivery_code"
KEY_DELIVERY_NUMBER = "delivery_number"

LOCATION_FORM = "form"

class SellApi(Resource):
    def __init__(self):
        self.post_parser = reqparse.RequestParser()
        self.post_parser.add_argument(KEY_DELIVERY_CODE, location=LOCATION_FORM)
        self.post_parser.add_argument(KEY_DELIVERY_NUMBER, location=LOCATION_FORM)

    @api_login_required
    @marshal_with(purchase_field, "purchase")
    def get(self):

        purchase = Purchase.query.filter(Purchase.seller_id == current_user.id).all()

        return purchase

    @api_login_required
    def post(self, purchase_id):

        args = self.post_parser.parse_args()

        purchase = Purchase.query.filter(Purchase.id == purchase_id).first()

        if purchase is None:
            raise PurchaseNotFound

        if purchase.seller_id != current_user.id:
            raise Forbidden

        delivery_code = args[KEY_DELIVERY_CODE]
        delivery_number = args[KEY_DELIVERY_NUMBER]

        purchase.delivery_code = delivery_code
        purchase.delivery_number = delivery_number

        db.session.merge(purchase)
        db.session.commit()

        return {}
