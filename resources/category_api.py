# -*- coding:utf-8 -*-

__author__ = "Philgyu,Seong"
__email__ = "philgyu.seong@gluvi.co"


from flask.ext.restful import Resource, marshal_with

from common.models import Category
from common.fields import category_field

class CategoryApi(Resource):

    @marshal_with(category_field, envelope="categories")
    def get(self ):
        categories = Category.query.all()

        return categories