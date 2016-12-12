# -*- coding:utf-8 -*-
from common.models import User
from utils import generate_client_access_token
from unittests.api_test import ApiTestCase

__author__ = "Philgyu,Seong"
__email__ = "phil@treasureisle.co"

KEY_ID = "id"
KEY_ACCESS_TOKEN = "access_token"


class SessionApiTestCase(ApiTestCase):
    def test_post(self):
        def post_session(data):
            return self.json_post("/session", data=data)

        def post_and_assert200(data):
            r = post_session(data=data)

            self.assert200(r)
            self.assert_valid_session(r.json()["session"])

        # 정상일 경우
        good_dummy = {
            KEY_ID: self.test_user_session.id,
            KEY_ACCESS_TOKEN: self.test_user_session.access_token
        }

        post_and_assert200(good_dummy)
