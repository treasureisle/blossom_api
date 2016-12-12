# -*- coding:utf-8 -*-
from copy import deepcopy

from common.models import User
from common.mods import db
from resources.users_api import KEY_REG_TYPE, REG_TYPE_EMAIL, KEY_EMAIL, KEY_PASSWORD, KEY_USERNAME
from unittests.api_test import ApiTestCase

__author__ = "Philgyu,Seong"
__email__ = "phil@treasureisle.co"


class UsersApiTestCase(ApiTestCase):
    DUMMY_EMAIL = "guerrilla86@naver.com"  # 이메일 가입 전용 테스트 이메일
    DUMMY_PASSWORD = "qwer1234"
    DUMMY_FB_ID = "1377733419184639"
    DUMMY_FB_EMAIL = "test.register@treasureisle.co"  # 페이스북 가입 전용 테스트 이메일
    DUMMY_USERNAME = "testusername"
    DUMMY_DUP_USERNAME = "testuser"
    DUMMY_FAKE_USERNAME = "fakeusername"
    DUMMY_DUP_EMAIL = "pigrabbit86@gmail.com"
    DUMMY_FAKE_EMAIL = "fake@treasureisle.co"
    DUMMY_WRONG_EMAIL = "bademail.com"
    DUMMY_WRONG_SIGN_USERNAME = "bad#$#$"
    DUMMY_WRONG_SHORT_USERNAME = "sh"
    DUMMY_WRONG_LONG_USERNAME = "tooooooooooooooooooooolong"
    DUMMY_WRONG_KOREAN_USERNAME = "한글좋아요"
    DUMMY_GOOGLE_EMAIL = "philm@treasureisle.co"

    def test_post(self):
        def post_users(data):
            return self.json_post("/users", data=data)

        def post_and_assert200(data):
            r = post_users(data=data)

            self.assert200(r, message="%s status:code:%d" % (r.text, r.status_code))

            r_json = r.json()
            self.assert_valid_session(r_json["session"])

        def post_and_assert400(data):
            r = post_users(data=data)
            self.assert400(r, message="%s status:code:%d" % (r.text, r.status_code))

        def post_and_assert409(data):
            r = post_users(data=data)
            self.assert409(r, message="%s status:code:%d" % (r.text, r.status_code))

        def set_none_data(data, key):
            tmp = deepcopy(data)
            tmp[key] = None
            return tmp

        def assert_delete_test_user(f):
            exist_user = User.query.filter(f).first()

            self.assertIsNotNone(exist_user)

            db.session.delete(exist_user)
            db.session.commit()

        def assert_delete_email_test_user():
            assert_delete_test_user(User.email == self.DUMMY_EMAIL)

        def set_none_and_post_assert400(data, *keys):
            if not keys:
                return

            data_temp = data
            for key in keys:
                data_temp = set_none_data(data=data_temp, key=key)

            post_and_assert400(data_temp)

        # 이메일 가입 테스트
        good_dummy = {
            KEY_REG_TYPE: REG_TYPE_EMAIL,
            KEY_EMAIL: self.DUMMY_EMAIL,
            KEY_PASSWORD: self.DUMMY_PASSWORD,
            KEY_USERNAME: self.DUMMY_USERNAME
        }

        dummy_user = User.query.filter(User.email == self.DUMMY_EMAIL).first()

        if dummy_user is not None:
            db.session.delete(dummy_user)
            db.session.commit()

        post_and_assert200(good_dummy)

        db.session.commit()

        # 이메일로 가입했을 경우 is_activated 가 0인가?
        exist_email_user = User.query.filter(User.email == self.DUMMY_EMAIL).first()
        self.assertEqual(exist_email_user.is_activated, 0)

        assert_delete_email_test_user()
        db.session.commit()

        # 중복 이메일 테스트
        dup_email_dummy = deepcopy(good_dummy)
        dup_email_dummy[KEY_EMAIL] = self.DUMMY_DUP_EMAIL
        dup_email_dummy[KEY_USERNAME] = "duptest"

        dub_email_user = User.query.filter(User.email == self.DUMMY_DUP_EMAIL).first()
        if dub_email_user is not None:
            db.session.delete(dub_email_user)
            db.session.commit()

        post_and_assert200(dup_email_dummy)

        db.session.commit()

        dup_email_dummy_2 = deepcopy(dup_email_dummy)
        dup_email_dummy_2[KEY_USERNAME] = "duptest2"

        post_and_assert409(dup_email_dummy_2)

        # 중복 유저네임 테스트
        dup_username_dummy = deepcopy(dup_email_dummy)
        dup_username_dummy[KEY_EMAIL] = "noexist@email.test"

        post_and_assert409(dup_username_dummy)

        assert_delete_test_user(User.email == self.DUMMY_DUP_EMAIL)

        db.session.commit()

        # 키가 없을 경우들 테스트
        set_none_and_post_assert400(good_dummy, KEY_REG_TYPE)
        if KEY_REG_TYPE == REG_TYPE_EMAIL:
            set_none_and_post_assert400(good_dummy, KEY_EMAIL)
            set_none_and_post_assert400(good_dummy, KEY_USERNAME)
            set_none_and_post_assert400(good_dummy, KEY_PASSWORD)

        # username 을 이상하게 적을 경우 가입이 안되는가?
        def set_wrong_username_and_post_assert400(wrong_username):
            temp = deepcopy(good_dummy)
            temp[KEY_USERNAME] = wrong_username

            post_and_assert400(temp)

        # 한글일 경우
        set_wrong_username_and_post_assert400(self.DUMMY_WRONG_KOREAN_USERNAME)
        # 특수기호가 있을 경우
        set_wrong_username_and_post_assert400(self.DUMMY_WRONG_SIGN_USERNAME)
        # 짧을 경우
        set_wrong_username_and_post_assert400(self.DUMMY_WRONG_SHORT_USERNAME)
        # 너무 길 경우
        set_wrong_username_and_post_assert400(self.DUMMY_WRONG_LONG_USERNAME)

        # facebook, twitter 가입은 각 api test에서