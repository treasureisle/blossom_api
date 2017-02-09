# -*- coding:utf-8 -*-

# 서비스 설정

__author__ = "Philgyu, Seong"
__email__ = "phil@treasureisle.co"

# 트위터 연동 key
TWITTER_CONSUMER_KEY = "dB6GZlyWie6EFR3rth09CXpdu"
TWITTER_CONSUMER_SECRET = "YUUhozso7iAkorhMcXdtFg8QJQcPvn1VKVYIzIc1mhq04o174Y"

# sendgrid api key
SENDGRID_FORGOT_PASSWORD_API_KEY = "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"

# sqlalchemy 버전업 되면서 워닝 제거
SQLALCHEMY_TRACK_MODIFICATIONS = True

TEST_USER_USERNAME = "testuser2"
TEST_USER_PASSWORD = "qqqqqqqq"

# 최소 유저네임 길이
MIN_USERNAME_LENGTH = 4

# 최대 유저네임 길이
MAX_USERNAME_LENGTH = 16

# 댓글 최대 길이
MAX_REPLY_LENGTH = 200

CLIENT_ACCESS_TOKEN_SALT = "rdk`{KG9_L+FS28S\*``6WbE{+L@,#"

# 댓글 페이지당 줄수
REPLY_ROW = 30

# 유저 프로필 썸네일 width
USER_PROFILE_WIDTH_NORMAL = 200

# 유저 프로필 썸네일 height
USER_PROFILE_HEIGHT_NORMAL = 200

# 포스트 페이징 수
POST_ROW = 20

# 메세지 페이징 수
MESSAGE_ROW = 20

# 유저 프로필에 나오는 포스트 페이지당 갯수
USER_POST_ROW = 20

MIN_PASSWORD_LEN = 6
