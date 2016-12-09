# -*- coding:utf-8 -*-

from celery import Celery
from flask.app import Flask

from common.config_keys import KEY_BROKER_URL, KEY_CELERY_RESULT_BACKEND, KEY_S3_BUCKET
from common.mods import db
from utils import get_boto_client

__author__ = "Philgyu, Seong"
__email__ = "phil@treasureisle.co"

app = Flask(__name__)
app.config.from_pyfile("configs.py")
app.config.from_envvar("TREASUREISLE_CONFIGS")

db.init_app(app)

with app.test_request_context():
    celery = Celery(broker=app.config[KEY_BROKER_URL], backend=app.config[KEY_CELERY_RESULT_BACKEND])


@celery.task
def task_add(x, y):
    with app.test_request_context():
        return x + y


@celery.task
def task_delete_s3_key(app, keyname):
    with app.test_request_context():
        app.logger.info("deleting %s" % keyname)

        client = get_boto_client(app, "s3")
        response = client.delete_object(Bucket=app.config[KEY_S3_BUCKET], Key=keyname)
        print response
