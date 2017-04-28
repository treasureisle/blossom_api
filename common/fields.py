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
    "is_me": fields.Boolean
}

user_message_fields = {
    "id": fields.Integer,
    "username": fields.String,
    "profile_thumb_url": fields.String,
    "introduce": fields.String,
    "is_me": fields.Boolean,
    "last_message": fields.String,
    "last_message_created_at": fields.DateTime,
    "is_read": fields.Boolean
}

user_detail_fields = {
    "id": fields.Integer,
    "username": fields.String,
    "email": fields.String,
    "name": fields.String,
    "zipcode": fields.Integer,
    "address1": fields.String,
    "address2": fields.String,
    "recent_name": fields.String,
    "recent_zipcode": fields.String,
    "recent_add1": fields.String,
    "recent_add2": fields.String,
    "recent_phone": fields.String,
    "phone": fields.String,
    "level": fields.Integer,
    "point": fields.Integer,
    "region": fields.String,
    "seller_level": fields.Integer,
    "bank_account": fields.String,
    "biz_num": fields.String,
    "biz_name": fields.String,
    "recommender_id": fields.Integer,
    "profile_thumb_url": fields.String,
    "last_logged_at": fields.DateTime,
    "introduce": fields.String,
    "created_at": fields.DateTime,
    "is_me": fields.Boolean
}

post_field = {
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
    "product_name": fields.String,
    "origin_price": fields.Integer,
    "purchase_price": fields.Integer,
    "fee": fields.Integer,
    "region": fields.String,
    "hashtag": fields.String,
    "text": fields.String,
    "replies": fields.Integer,
    "likes": fields.Integer,
    "is_liked": fields.Boolean
}

reply_field = {
    "id": fields.Integer,
    "user": fields.Nested(user_fields),
    "post": fields.Nested(post_field),
    "parent_id": fields.Integer,
    "depth": fields.Integer,
    "text": fields.String,
    "likes": fields.Integer,
    "replies": fields.Integer,
    "created_at": fields.DateTime,
    "is_liked": fields.Boolean
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
    "number": fields.Integer,
    "hidden": fields.Integer
}

purchase_field = {
    "id": fields.Integer,
    "post": fields.Nested(post_field),
    "seller": fields.Nested(user_fields),
    "buyer": fields.Nested(user_fields),
    "color_size": fields.Nested(color_size_field),
    "amount": fields.Integer,
    "price": fields.Integer,
    "payment": fields.Integer,
    "name": fields.String,
    "zipcode": fields.Integer,
    "address1": fields.String,
    "address2": fields.String,
    "phone": fields.String,
    "comment": fields.String,
    "delivery_code": fields.Integer,
    "delivery_number": fields.String,
    "is_paid": fields.Integer,
    "created_at": fields.DateTime
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

message_field = {
    "id": fields.Integer,
    "sender": fields.Nested(user_fields),
    "reciever": fields.Nested(user_fields),
    "message": fields.String,
    "is_read": fields.Boolean,
    "created_at": fields.DateTime
}

category_field = {
    "id": fields.Integer,
    "name": fields.String,
    "parent_id": fields.Integer,
    "depth": fields.Integer
}

store_field = {
    "id": fields.Integer,
    "num_events": fields.Integer,
    "event1_hashtag_id": fields.Integer,
    "event1_img_url": fields.String,
    "event1_title": fields.String,
    "event2_hashtag_id": fields.Integer,
    "event2_img_url": fields.String,
    "event2_title": fields.String,
    "event3_hashtag_id": fields.Integer,
    "event3_img_url": fields.String,
    "event3_title": fields.String,
    "event4_hashtag_id": fields.Integer,
    "event4_img_url": fields.String,
    "event4_title": fields.String,
    "event5_hashtag_id": fields.Integer,
    "event5_img_url": fields.String,
    "event5_title": fields.String,
    "seller_id": fields.Integer,
    "today_seller_title": fields.String,
    "editors_pick_hashtag_id": fields.Integer,
    "editors_pick_title": fields.String
}

notification_field = {
    "id": fields.Integer,
    "user": fields.Nested(user_fields),
    "sender": fields.Nested(user_fields),
    "code": fields.Integer,
    "message": fields.String,
    "is_read": fields.Boolean,
    "created_at": fields.DateTime
}

message_timestamp_field = {
    "id": fields.Integer,
    "user_id": fields.Integer,
    "timestamp": fields.DateTime
}

firebase_field = {
    "id": fields.Integer,
    "user_id": fields.Integer,
    "device_token": fields.String
}