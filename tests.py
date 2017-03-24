# -*- coding:utf-8 -*-

from test import test_support

from unittests.users_api_test import UsersApiTestCase
from unittests.session_api_test import SessionApiTestCase
from unittests.session_email_api_test import SessionEmailApiTestCase
from unittests.posts_test import PostsApiTest

__author__ = "Philgyu,Seong"
__email__ = "phil@treasureisle.co"


def test_all():
    test_support.run_unittest(PostsApiTest)
    # test_support.run_unittest(UsersApiTestCase)

if __name__ == "__main__":
    test_all()
