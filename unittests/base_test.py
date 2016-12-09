# -*- coding:utf-8 -*-
import json
import os

from flask.app import Flask
from flask.ext.testing.utils import TestCase
import requests

from common.config_keys import KEY_API_URL, KEY_S3_BUCKET, KEY_CDN_URL, KEY_AWS_ACCESS_KEY_ID, KEY_AWS_ACCESS_SECRET, \
    KEY_LOCAL_URL
from common.mods import db
from common.regex import REGEX_URL

__author__ = "Philgyu, Seong"
__email__ = "phil@treasureisle.co"


class BaseTestCase(TestCase):
    headers = {"content-type": "application/json"}

    def create_app(self):
        app = Flask(__name__)
        app.config.from_pyfile("../configs.py")
        app.config.from_envvar("TREASUREISLE_CONFIGS")
        app.config["TESTING"] = True
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

        self.api_url = app.config[KEY_API_URL]
        self.app = app
        self.assert_configs()

        self.test_user = None

        return app

    def setUp(self):
        db.init_app(self.app)

    def assert201(self, response, message=None):
        self.assertStatus(response, 201, message)

    def assert204(self, response, message=None):
        self.assertStatus(response, 204, message)

    def assert406(self, response, message=None):
        self.assertStatus(response, 406, message)

    def assert409(self, response, message=None):
        self.assertStatus(response, 409, message)

    def assertIsNotNoneAndNotNullString(self, obj, message=None):
        self.assertTrue(expr=obj is not None and object != "null", msg=message)

    def assertBool(self, obj, message=None):
        self.assertEqual(type(obj), bool, msg=message)

    def assertInt(self, obj):
        self.assertEqual(type(obj), int)

    def assertUrl(self, url):
        """
        url 이 유효한지 확인
        :param url:
        """
        self.assertRegexpMatches(url, REGEX_URL)

    def assert_configs(self):
        config = self.app.config

        self.assertIn(KEY_API_URL, config)
        self.assertUrl(config[KEY_API_URL])

        self.assertIn(KEY_S3_BUCKET, config)
        self.assertNotEqual(config[KEY_S3_BUCKET], "S3_BUCKET")

        self.assertIn(KEY_CDN_URL, config)
        self.assertUrl(config[KEY_CDN_URL])

        self.assertIn(KEY_AWS_ACCESS_KEY_ID, config)
        self.assertNotEqual(config[KEY_AWS_ACCESS_KEY_ID], "AWS_ACCESS_KEY")

        self.assertIn(KEY_AWS_ACCESS_SECRET, config)
        self.assertNotEqual(config[KEY_AWS_ACCESS_SECRET], "AWS_ACCESS_SECRET")

        self.assertIn(KEY_LOCAL_URL, config)
        self.assertUrl(config[KEY_LOCAL_URL])

    def get_api_url(self, sub_url):
        return "%s%s" % (self.app.config[KEY_API_URL], sub_url)

    def get_localhost_url(self, sub_url):
        return "%s%s" % (self.app.config[KEY_LOCAL_URL], sub_url)

    def get_json_headers(self, login=True):
        header = {"content-type": "application/json"}
        if login:
            if self.test_user_session is not None:
                header["Authorization"] = "%s:%s" % (self.test_user_session.id, self.test_user_session.access_token)

        return header

    def json_post(self, sub_url, data=None, headers=None):
        if data:
            data = json.dumps(data)
        _headers = headers if headers else self.get_json_headers()
        return requests.post(url=self.get_api_url(sub_url), data=data, headers=_headers)

    def json_get(self, sub_url, data=None, headers=None):
        if data:
            data = json.dumps(data)
        _headers = headers if headers else self.get_json_headers()
        return requests.get(url=self.get_api_url(sub_url), data=data, headers=_headers)

    def json_delete(self, sub_url, headers=None):
        _headers = headers if headers else self.get_json_headers()
        return requests.delete(url=self.get_api_url(sub_url), headers=_headers)

    def get_full_asset_filename(self, filename):
        return os.path.join(os.getcwd(), "unittests", "asset", filename)
