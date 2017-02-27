# -*- coding:utf-8 -*-

from flask.ext.restful import Resource, marshal_with
from common.models import Store
from common.fields import store_field

__author__ = "Philgyu,Seong"
__email__ = "philgyu.seong@gluvi.co"

KEY_ORDER = "order"
KEY_ROW = "row"
KEY_PAGE = "page"

ORDER_SCORE = "score"


class StoreApi(Resource):
    @marshal_with(store_field, envelope="store")
    def get(self):
        store = Store.query.first()

        return store
