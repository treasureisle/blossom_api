# -*- coding:utf-8 -*-

from flask.ext.restful import Resource, marshal_with, reqparse
from flask.ext.login import current_user

from common.mods import db
from common.fields import firebase_field
from common.models import Firebase
from utils import api_login_required

__author__ = "Philgyu,Seong"
__email__ = "philgyu.seong@gluvi.co"

KEY_DEVICE_TOKEN = "device_token"

LOCATION_FORM = "form"

class FirebaseApi(Resource):
    def __init__(self):
        self.post_parser = reqparse.RequestParser()
        self.post_parser.add_argument(KEY_DEVICE_TOKEN, location=LOCATION_FORM)

    @api_login_required
    @marshal_with(firebase_field, "firebase")
    def get(self):

        firebase = Firebase.query.filter(Firebase.user_id == current_user.id).first()

        return firebase

    @api_login_required
    def post(self):

        args = self.post_parser.parse_args()

        firebase = Firebase.query.filter(Firebase.user_id == current_user.id).first()

        device_token = args[KEY_DEVICE_TOKEN]

        if firebase is None:
            firebase = Firebase(current_user.id, device_token)
            db.session.add(firebase)
        else:
            firebase.device_token = device_token
            db.session.merge(firebase)

        db.session.commit()

        return {}
