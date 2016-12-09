# -*- coding:utf-8 -*-
from flask.ext.bcrypt import Bcrypt
from flask.ext.login import LoginManager
from flask.ext.restful import Api
from flask.ext.sqlalchemy import SQLAlchemy

__author__ = "Woong Bi,Kim"
__email__ = "ssinss@gmail.com"

db = SQLAlchemy()

bcrypt = Bcrypt()

api = Api()

login_manager = LoginManager()

