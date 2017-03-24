# -*- coding:utf-8 -*-

import requests
from unittests.api_test import ApiTestCase

__author__ = "Philgyu,Seong"
__email__ = "philgyu.seong@gluvi.co"

KEY_POST_TYPE = "post_type"
KEY_IMG1 = "img1"
KEY_IMG2 = "img2"
KEY_IMG3 = "img3"
KEY_IMG4 = "img4"
KEY_IMG5 = "img5"
KEY_TITLE = "title"
KEY_BRAND = "brand"
KEY_PRODUCT_NAME = "product_name"
KEY_ORIGIN_PRICE = "origin_price"
KEY_PURCHASE_PRICE = "purchase_price"
KEY_FEE = "fee"
KEY_REGION = "region"
KEY_HASHTAG = "hashtag"
KEY_TEXT = "text"


class PostsApiTest(ApiTestCase):
    def test_post(self):
        test1_filename = self.get_full_asset_filename("sample1.jpg")
        test2_filename = self.get_full_asset_filename("sample2.jpg")
        test3_filename = self.get_full_asset_filename("sample3.jpg")
        test4_filename = self.get_full_asset_filename("sample4.jpg")
        test5_filename = self.get_full_asset_filename("sample5.jpg")

        headers = {"Authorization": "%s:%s" % (self.test_user.id, self.test_user_session.access_token)}

        dummy = {
            KEY_POST_TYPE: 0,
            KEY_TITLE: "test title",
            KEY_BRAND: "test brand",
            KEY_PRODUCT_NAME: "test product name",
            KEY_ORIGIN_PRICE: 1000000,
            KEY_PURCHASE_PRICE: 100000,
            KEY_FEE: 10000,
            KEY_REGION: "test gegion",
            KEY_HASHTAG: "test hashtag",
            KEY_TEXT: "test text"
        }

        files = {
            KEY_IMG1: open(test1_filename, "rb"),
            KEY_IMG2: open(test2_filename, "rb"),
            KEY_IMG3: open(test3_filename, "rb"),
            KEY_IMG4: open(test4_filename, "rb"),
            KEY_IMG5: open(test5_filename, "rb")
        }

        r = requests.post(self.get_api_url("/posts"), headers=headers, data=dummy, files=files)

        self.assert200(r)
