# -*- coding:utf-8 -*-

import werkzeug
import hashlib
import os

from werkzeug.utils import secure_filename
from flask.ext.restful import Resource, reqparse, marshal_with
from flask.ext.login import current_user
from flask.globals import current_app, request
from PIL import Image

from common.mods import db
from common.api_errors import NotAllowedOrderType, PostNotFound, Forbidden
from common.models import Post
from common.fields import post_field
from common.service_configs import POST_ROW
from common.config_keys import KEY_CDN_URL
from utils import get_page_offset, api_login_required, get_now_mysql_datetime, upload_file_to_s3, \
    rotate_image_with_exif, make_s3_url
from tasks import task_delete_s3_key

__author__ = "Philgyu,Seong"
__email__ = "philgyu.seong@gluvi.co"

KEY_POST_TYPE = "post_type"
KEY_ORDER = "order"
KEY_ROW = "row"
KEY_PAGE = "page"
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

ORDER_SCORE = "score"
POST_TYPE_SELL = "sell"
POST_TYPE_BUY = "buy"
POST_TYPE_REVIEW = "review"
POST_TYPE_STORE = "store"

LOCATION_FORM = "form"
LOCATION_FILE = "files"

class PostsApi(Resource):
    def __init__(self):
        self.post_parser = reqparse.RequestParser()
        self.post_parser.add_argument(KEY_POST_TYPE, location=LOCATION_FORM)
        self.post_parser.add_argument(KEY_IMG1, type=werkzeug.datastructures.FileStorage,
                                      location=LOCATION_FILE, required=True)
        self.post_parser.add_argument(KEY_IMG2, type=werkzeug.datastructures.FileStorage,
                                      location=LOCATION_FILE)
        self.post_parser.add_argument(KEY_IMG3, type=werkzeug.datastructures.FileStorage,
                                      location=LOCATION_FILE)
        self.post_parser.add_argument(KEY_IMG4, type=werkzeug.datastructures.FileStorage,
                                      location=LOCATION_FILE)
        self.post_parser.add_argument(KEY_IMG5, type=werkzeug.datastructures.FileStorage,
                                      location=LOCATION_FILE)
        self.post_parser.add_argument(KEY_TITLE, location=LOCATION_FORM)
        self.post_parser.add_argument(KEY_BRAND, location=LOCATION_FORM)
        self.post_parser.add_argument(KEY_PRODUCT_NAME, location=LOCATION_FORM)
        self.post_parser.add_argument(KEY_ORIGIN_PRICE, location=LOCATION_FORM)
        self.post_parser.add_argument(KEY_PURCHASE_PRICE, location=LOCATION_FORM)
        self.post_parser.add_argument(KEY_FEE, location=LOCATION_FORM)
        self.post_parser.add_argument(KEY_REGION, location=LOCATION_FORM)
        self.post_parser.add_argument(KEY_HASHTAG, location=LOCATION_FORM)
        self.post_parser.add_argument(KEY_TEXT, location=LOCATION_FORM)

    @marshal_with(post_field, envelope="posts")
    def get(self):

        post_type = request.args.get(KEY_POST_TYPE, default=POST_TYPE_SELL)
        row = int(request.args.get(KEY_ROW, default=POST_ROW))
        page = int(request.args.get(KEY_PAGE, default=1))
        order = request.args.get(KEY_ORDER, default=ORDER_SCORE)

        post_type_code = 0

        if post_type == POST_TYPE_BUY:
            post_type_code = 1
        elif post_type == POST_TYPE_REVIEW:
            post_type_code = 2
        elif post_type == POST_TYPE_STORE:
            post_type_code = 3

        if order == ORDER_SCORE:
            posts = Post.query.filter(Post.post_type == post_type_code).order_by(Post.score.desc()).\
                offset(get_page_offset(page, row)).limit(row).all()

            return posts
        else:
            raise NotAllowedOrderType

    @api_login_required
    @marshal_with(post_field, envelope="posts")
    def post(self):
        args = self.post_parser.parse_args()

        post_type = int(args[KEY_POST_TYPE])
        title = args[KEY_TITLE]
        brand = args[KEY_BRAND]
        product_name = args[KEY_PRODUCT_NAME]
        origin_price = int(args[KEY_ORIGIN_PRICE])
        purchase_price = int(args[KEY_PURCHASE_PRICE])
        fee = int(args[KEY_FEE])
        region = args[KEY_REGION]
        hashtag = args[KEY_HASHTAG]
        text = args[KEY_TEXT]

        image1 = args[KEY_IMG1]
        image2 = args[KEY_IMG2]
        image3 = args[KEY_IMG3]
        image4 = args[KEY_IMG4]
        image5 = args[KEY_IMG5]

        # 임시 파일 저장
        temp_filename = os.path.join("/tmp", secure_filename(image1.filename))
        image1.save(temp_filename)

        new_post = Post(post_type=post_type, user_id=current_user.id, title=title, brand=brand,
                        product_name=product_name, origin_price=origin_price, purchase_price=purchase_price, fee=fee,
                        region=region, hashtag=hashtag, text=text, created_at=get_now_mysql_datetime())

        db.session.add(new_post)
        db.session.flush()
        db.session.refresh(new_post)

        if image1 is not None:
            image_file_name = self.make_image_filename(new_post.id, 1)
            image_key_name = self.make_image_keyname(image_file_name)

            stream = image1.stream
            image = Image.open(stream)
            image = rotate_image_with_exif(image)
            image.save(image_file_name, format="JPEG")

            upload_file_to_s3(app=current_app, filename=image_file_name, keyname=image_key_name)
            new_post.img_url1 = make_s3_url(current_app, image_key_name)

            os.remove(image_file_name)

            if image2 is not None:
                image_file_name = self.make_image_filename(new_post.id, 2)
                image_key_name = self.make_image_keyname(image_file_name)

                stream = image2.stream
                image = Image.open(stream)
                image = rotate_image_with_exif(image)
                image.save(image_file_name, format="JPEG")

                upload_file_to_s3(app=current_app, filename=image_file_name, keyname=image_key_name)
                new_post.img_url2 = make_s3_url(current_app, image_key_name)

                os.remove(image_file_name)

                if image3 is not None:
                    image_file_name = self.make_image_filename(new_post.id, 3)
                    image_key_name = self.make_image_keyname(image_file_name)

                    stream = image3.stream
                    image = Image.open(stream)
                    image = rotate_image_with_exif(image)
                    image.save(image_file_name, format="JPEG")

                    upload_file_to_s3(app=current_app, filename=image_file_name, keyname=image_key_name)
                    new_post.img_url3 = make_s3_url(current_app, image_key_name)

                    os.remove(image_file_name)

                    if image4 is not None:
                        image_file_name = self.make_image_filename(new_post.id, 4)
                        image_key_name = self.make_image_keyname(image_file_name)

                        stream = image4.stream
                        image = Image.open(stream)
                        image = rotate_image_with_exif(image)
                        image.save(image_file_name, format="JPEG")

                        upload_file_to_s3(app=current_app, filename=image_file_name, keyname=image_key_name)
                        new_post.img_url4 = make_s3_url(current_app, image_key_name)

                        os.remove(image_file_name)

                        if image5 is not None:
                            image_file_name = self.make_image_filename(new_post.id, 5)
                            image_key_name = self.make_image_keyname(image_file_name)

                            stream = image5.stream
                            image = Image.open(stream)
                            image = rotate_image_with_exif(image)
                            image.save(image_file_name, format="JPEG")

                            upload_file_to_s3(app=current_app, filename=image_file_name, keyname=image_key_name)
                            new_post.img_url5 = make_s3_url(current_app, image_key_name)

                            os.remove(image_file_name)

        db.session.merge(new_post)
        db.session.commit()

        return new_post

    @api_login_required
    def delete(self, post_id):
        post = Post.query.filter(Post.id == post_id).first()

        if post is None:
            raise PostNotFound

        if post.user_id != current_user.id:
            raise Forbidden

        # s3에서 이미지 삭제
        if post.img_url1 is not None:
            task_delete_s3_key(current_app, post.imgurl1[len(current_app.config[KEY_CDN_URL]) + 1:])
            if post.img_url2 is not None:
                task_delete_s3_key(current_app, post.imgurl2[len(current_app.config[KEY_CDN_URL]) + 1:])
                if post.img_url3 is not None:
                    task_delete_s3_key(current_app, post.imgurl3[len(current_app.config[KEY_CDN_URL]) + 1:])
                    if post.img_url4 is not None:
                        task_delete_s3_key(current_app, post.imgurl4[len(current_app.config[KEY_CDN_URL]) + 1:])
                        if post.img_url5 is not None:
                            task_delete_s3_key(current_app, post.imgurl5[len(current_app.config[KEY_CDN_URL]) + 1:])

        db.session.delete(post)
        db.session.commit()

        return post_id


    def make_image_filename(self, post_id, number):
        h = hashlib.md5()
        h.update(str(post_id))
        return "%s_%d.jpg" % (h.hexdigest(), number)

    def make_image_keyname(self, image_filename):
        return "images/%s" % image_filename