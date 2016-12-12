# -*- coding:utf-8 -*-
from flask.ext.restful import fields

__author__ = "Philgyu, Seong"
__email__ = "phil@treasureisle.co"


session_type_fields = {
    "type": fields.String
}

session_fields = {
    "id": fields.Integer,
    "access_token": fields.String,
    "types": fields.Nested(session_type_fields)
}

user_fields = {
    "id": fields.Integer,
    "username": fields.String,
    "profile_thumb_url": fields.String,
    "introduce": fields.String,
    "is_me": fields.Boolean,
}

post_field = {
    "id": fields.Integer,
    "post_type": fields.Integer,
    "user": fields.Nested(user_fields),
    "img_url1": fields.String,
    "title": fields.String,
    "origin_price": fields.Integer,
    "purchase_price": fields.Integer,
    "fee": fields.Integer
}

post_detail_field = {
    "id": fields.Integer,
    "post_type": fields.Integer,
    "user": fields.Nested(user_fields),
    "img_url1": fields.String,
    "img_url2": fields.String,
    "img_url3": fields.String,
    "img_url4": fields.String,
    "img_url5": fields.String,
    "title": fields.String,
    "brand": fields.String,
    "origin_price": fields.Integer,
    "purchase_price": fields.Integer,
    "fee": fields.Integer,
    "region": fields.String,
    "hashtag": fields.String,
    "text": fields.String,
    "replys": fields.Integer,
    "likes": fields.Integer
}

reply_field = {
    "id": fields.Integer,
    "user": fields.Nested(user_fields),
    "post_id": fields.Integer,
    "parent_id": fields.Integer,
    "text": fields.String,
    "likes": fields.Integer,
    "replys": fields.Integer,
    "created_at": fields.datetime
}

color_size_field = {
    "id": fields.Integer,
    "post_id": fields.Integer,
    "name": fields.String,
    "available": fields.Integer
}

hashtag_field = {
    "id": fields.Integer,
    "name": fields.String,
    "number": fields.Integer
}

purchase_field = {
    "id": fields.Integer,
    "seller": fields.Nested(user_fields),
    "buyer": fields.Nested(user_fields),
    "color_size": fields.Nested(color_size_field),
    "amount": fields.Integer,
    "price": fields.Integer,
    "payment": fields.Integer,
    "zipcode": fields.Integer,
    "address1": fields.String,
    "address2": fields.String,
    "phone": fields.String,
    "comment": fields.String,
    "delivery_code": fields.Integer,
    "delivery_number": fields.String,
    "created_at": fields.datetime
}

basket_field = {
    "id": fields.Integer,
    "user": fields.Nested(user_fields),
    "post": fields.Nested(post_field),
    "color_size": fields.Nested(color_size_field),
    "amount": fields.Integer
}

wish_field = {
    "id": fields.Integer,
    "user": fields.Nested(user_fields),
    "post": fields.Nested(post_field)
}

follower_field = {
    "id": fields.Integer,
    "follower_id": fields.Integer,
    "following_id": fields.Integer,
}

follow_wrapper = {
    "followings": fields.List(fields.Nested(follower_field)),
    "followers": fields.List(fields.Nested(follower_field))
}
