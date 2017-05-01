# -*- coding:utf-8 -*-

__author__ = "Philgyu, Seong"
__email__ = "phil@treasureisle.co"

DEBUG = True

# FLASK_LOGIN 에서 자동 로그인때 쓰인다
SECRET_KEY = "gluvi5+짤동"

# mysql db 주소
SQLALCHEMY_DATABASE_URI = "mysql+pymysql://user:password@host:port/dbname"

SQLALCHEMY_TRACK_MODIFICATIONS = True

# aws access key
AWS_ACCESS_KEY_ID = "AWS_ACCESS_KEY"

# aws access secret
AWS_ACCESS_SECRET = "AWS_ACCESS_SECRET"

# s3 bucket
S3_BUCKET = "S3_BUCKET"

WEB_URL = "http(s)://WEB_URL"

# CDN URL (버킷이 있다면 버킷까지 포함)
# ex) https://s3-ap-northeast-1.amazonaws.com/gluvi5dev
CDN_URL = "http(s)://CDN_URL"

# local url
# ex) http://dev.gluvi.co
# ex) http://192.168.25.41:5000
LOCAL_URL = "LOCAL_URL"

# api url
# ex) http://dev.gluvi.co/api
# ex) http://192.168.25.41:5000/api
API_URL = "http://0.0.0.0:5000"

# celery broker url
BROKER_URL = "redis://host:port/dbname"

CELERY_IMPORTS = ("tasks",)

# celery result backend
CELERY_RESULT_BACKEND = "redis://host:port/dbname"

FIREBASE_KEY = "AIzaSyAZIpKFzpZbPI2-trS9LHXtOHUQRVeiFoo"

# frontend url
# ex) http://gluvi5.com
WWW_URL = "http(s)://WWW_URL"

# api 에서 ip 체크할때 화이트 리스트
# ex) ["127.0.0.1","53.41.4.41"]
WHITE_IPS = ["IP1","IP2","..."]
