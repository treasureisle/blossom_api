# -*- coding:utf-8 -*-
from resources.session_api import KEY_ID, KEY_ACCESS_TOKEN
from resources.session_email_api import KEY_EMAIL, KEY_PASSWORD
from unittests.api_test import ApiTestCase

__author__ = "Philgyu,Seong"
__email__ = "phil@treasureisle.co"


class SessionEmailApiTestCase(ApiTestCase):
    GOOD_EMAIL = "test@treasureisle.co"
    GOOD_PASSWORD = "qqqqqqqq"

    def test_post(self):
        def post_session_email(data):
            return self.json_post("/session/email", data=data)

        good_dummy = {
            KEY_EMAIL: self.GOOD_EMAIL,
            KEY_PASSWORD: self.GOOD_PASSWORD
        }

        r = post_session_email(data=good_dummy)

        self.assert200(r)

        session_json = r.json()["session"]

        self.assert_valid_session(session_json)

        # 로그인한 token 으로 /session 에 로그인이 되는가?
        token_data = {
            KEY_ID: session_json[KEY_ID],
            KEY_ACCESS_TOKEN: session_json[KEY_ACCESS_TOKEN]
        }

        r = self.json_post("/session", data=token_data)
        self.assert200(r)

        self.assert_valid_session(r.json()["session"])

        # 틀린 비밀번호일 경우 400 에러가 출력되는가?
        wrong_password = {
            KEY_EMAIL: self.GOOD_EMAIL,
            KEY_PASSWORD: "wrongpassword"
        }

        r = post_session_email(data=wrong_password)

        self.assert400(r)

        # 이메일이 존재하지 않으면 404 에러가 뜨는가?
        not_exist_email = {
            KEY_EMAIL: "notexist@email.com",
            KEY_PASSWORD: "notexist"
        }

        r = post_session_email(data=not_exist_email)

        self.assert404(r)
