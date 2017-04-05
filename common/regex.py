# -*- coding:utf-8 -*-

__author__ = "Philgyu, Seong"
__email__ = "phil@treasureisle.co"

REGEX_EMAIL = r"[^@]+@[^@]+\.[^@]+"
REGEX_USERNAME = r"^[a-zA-Z0-9ㄱ-ㅣ가-힣_]{4,15}$"
# URL REGEX
# https://mathiasbynens.be/demo/url-regex @imme_emosol 참고
REGEX_URL = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
