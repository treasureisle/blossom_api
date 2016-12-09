# -*- coding:utf-8 -*-
import json

import requests

from common.models import User, Session
from common.service_configs import TEST_USER_USERNAME, TEST_USER_PASSWORD
from unittests.base_test import BaseTestCase

__author__ = "Philgyu,Seong"
__email__ = "philgyu.seong@gluvi.co"


class ApiTestCase(BaseTestCase):
    def setUp(self):
        BaseTestCase.setUp(self)
        self.assert_login()

    def assert_login(self):
        self.test_user = User.query.filter(User.username == TEST_USER_USERNAME).first()

        self.assertIsNotNone(self.test_user)
        data = {
            "email": self.test_user.email,
            "password": TEST_USER_PASSWORD
        }

        r = requests.post(url=self.get_api_url("/session/email"), data=json.dumps(data),
                          headers={"content-type": "application/json"})
        self.assert_200(r)
        session_json = r.json()["session"]
        self.assert_valid_session(session_json)
        self.test_user_session = Session(self.test_user.id, session_json["access_token"], self.test_user.username)

    def assert_valid_user_json(self, user_json):
        if user_json is not None:
            key_id = "id"
            key_username = "username"
            key_is_me = "is_me"
            key_profile_thumb_url = "profile_thumb_url"
            key_introduce = "introduce"

            self.assertIn(key_id, user_json)
            self.assertInt(user_json[key_id])

            self.assertIn(key_username, user_json)

            self.assertIn(key_is_me, user_json)
            self.assertBool(user_json[key_is_me])

            self.assertIn(key_profile_thumb_url, user_json)
            self.assertUrl(user_json[key_profile_thumb_url])

            self.assertIn(key_introduce, user_json)

    def assert_valid_session(self, json):
        if json is not None:
            key_id = "id"
            key_access_token = "access_token"

            self.assertIn(key_id, json)
            self.assertInt(json[key_id])

            self.assertIn(key_access_token, json)

    def assert_valid_user_detail(self, json):
        if json is not None:
            key_id = "id"
            key_username = "username"
            key_profile_thumb_url = "profile_thumb_url"
            key_introduce = "introduce"
            key_is_me = "is_me"
            key_video_count = "video_count"
            key_creativity = "creativity"
            key_contribution = "contribution"

            self.assertIn(key_id, json)
            self.assertInt(json[key_id])

            self.assertIn(key_username, json)

            self.assertIn(key_profile_thumb_url, json)
            self.assertUrl(key_profile_thumb_url)

            self.assertIn(key_introduce, json)

            self.assertIn(key_is_me, json)
            self.assertBool(key_is_me)

            self.assertIn(key_video_count, json)
            self.assertInt(key_video_count)

            self.assertIn(key_creativity, json)
            self.assertInt(key_creativity)

            self.assertIn(key_contribution, json)
            self.assertInt(key_contribution)

    def assert_valid_setting(self, json):
        if json is not None:
            key_id = "id"
            key_username = "username"
            key_profile_thumb_url = "profile_thumb_url"
            key_introduce = "introduce"

            self.assertIn(key_id, json)
            self.assertInt(json[key_id])

            self.assertIn(key_username, json)

            self.assertIn(key_profile_thumb_url, json)
            self.assertUrl(key_profile_thumb_url)

            self.assertIn(key_introduce, json)

    def assert_valid_next_topic(self, json):
        if json is not None:
            key_id = "id"
            key_topic = "topic"
            key_upcount = "upcount"
            key_created_at = "created_at"
            key_is_uped = "is_uped"
            key_is_me = "is_me"
            key_rank = "rank"
            key_next_vote_start_at = "next_vote_start_at"
            key_running_vote_end_at = "running_vote_end_at"

            self.assertIn(key_id, json)
            self.assertInt(key_id)

            self.assertIn(key_topic, json)

            self.assertIn(key_upcount, json)
            self.assertInt(key_upcount)

            self.assertIn(key_created_at, json)
            self.assertIsNotNoneAndNotNullString(key_created_at)

            self.assertIn(key_is_uped, json)
            self.assertBool(key_is_uped)

            self.assertIn(key_is_me, json)
            self.assertBool(key_is_me)

            self.assertIn(key_rank, json)
            self.assertInt(key_rank)

            self.assertIn(key_next_vote_start_at)
            self.assertIsNotNoneAndNotNullString(key_next_vote_start_at)

            self.assertIn(key_running_vote_end_at)
            self.assertIsNotNoneAndNotNullString(key_running_vote_end_at)

    def assert_valid_video_comment(self, json):
        if json is not None:
            key_id = "id"
            key_user_id = "user_id"
            key_video_id = "video_id"
            key_comment = "comment"
            key_created_at = "created_at"
            key_user = "user"

            self.assertIn(key_id, json)
            self.assertInt(key_id)

            self.assertIn(key_user_id, json)
            self.assertInt(key_user_id)

            self.assertIn(key_video_id, json)
            self.assertInt(key_video_id)

            self.assertIn(key_comment, json)

            self.assertIn(key_created_at, json)
            self.assertIsNotNoneAndNotNullString(key_created_at)

            self.assertIn(key_user, json)
            self.assert_valid_user_json(json[key_user])

    def assert_valid_video(self, json):
        if json is not None:
            key_id = "id"
            key_user_id = "user_id"
            key_user = "user"
            key_topic_id = "topic_id"
            key_created_at = "created_at"
            key_url = "url"
            key_length = "length"
            key_up_count = "up_count"
            key_down_count = "down_count"
            key_comment_count = "comment_count"
            key_thumb_url = "thumb_url"
            key_caption = "caption"
            key_size = "size"
            key_bitrate = "bitrate"
            key_is_uped = "is_uped"
            key_is_downed = "is_downed"
            key_is_me = "is_me"
            key_best5_comments = "best5_comments"

            self.assertIn(key_id, json)
            self.assertInt(key_id)

            self.assertIn(key_user_id, json)
            self.assertInt(key_user_id)

            self.assertIn(key_user, json)
            self.assert_valid_user_json(json[key_user])

            self.assertIn(key_topic_id, json)
            self.assertInt(key_topic_id)

            self.assertIn(key_created_at, json)
            self.assertIsNotNoneAndNotNullString(key_created_at)

            self.assertIn(key_url, json)
            self.assertUrl(key_url)

            self.assertIn(key_length, json)
            self.assertInt(key_length)

            self.assertIn(key_up_count, json)
            self.assertInt(key_up_count)

            self.assertIn(key_down_count, json)
            self.assertInt(key_down_count)

            self.assertIn(key_comment_count, json)
            self.assertInt(key_comment_count)

            self.assertIn(key_thumb_url, json)
            self.assertUrl(key_thumb_url)

            self.assertIn(key_caption, json)

            self.assertIn(key_size, json)
            self.assertInt(key_size)

            self.assertIn(key_bitrate, json)
            self.assertInt(key_bitrate)

            self.assertIn(key_is_uped, json)
            self.assertBool(key_is_uped)

            self.assertIn(key_is_downed, json)
            self.assertBool(key_is_downed)

            self.assertIn(key_is_me, json)
            self.assertBool(key_is_me)

            self.assertIn(key_best5_comments, json)
            self.assertLessEqual(len(json[key_best5_comments]), BEST5_COMMENT_COUNT)

    def assert_valid_topic(self, json):
        if json is not None:
            key_id = "id"
            key_topic = "topic"
            key_up_count = "up_count"
            key_started_at = "started_at"
            key_video_count = "video_count"
            key_gif_url = "gif_url"
            key_gif_thumb_url = "gif_thumb_url"
            key_best5_videos = "best5_videos"

            self.assertIn(key_id, json)
            self.assertInt(key_id)

            self.assertIn(key_topic, json)

            self.assertIn(key_up_count, json)
            self.assertInt(key_up_count)

            self.assertIn(key_started_at, json)
            self.assertIsNotNoneAndNotNullString(key_started_at)

            self.assertIn(key_video_count, json)
            self.assertInt(key_video_count)

            self.assertIn(key_gif_url, json)
            self.assertUrl(key_gif_url)

            self.assertIn(key_gif_thumb_url, json)
            self.assertUrl(key_gif_url)

            self.assertIn(key_best5_videos, json)
            self.assert_valid_video(json[key_best5_videos])

    def assert_archive(self, json):
        if json is not None:
            key_month = "month"
            key_topics = "topics"

            self.assertIn(key_month, json)

            self.assertIn(key_topics, json)
            self.assert_valid_topic(json[key_topics])

    def assert_community_rule(self, json):
        if json is not None:
            key_text = "text"

            self.assert_In(key_text, json)

    def assert_term(self, json):
        if json is not None:
            key_text = "text"

            self.assert_In(key_text, json)

    def assert_privacy(self, json):
        if json is not None:
            key_text = "text"

            self.assert_In(key_text, json)
