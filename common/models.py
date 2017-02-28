# -*- coding:utf-8 -*-
from flask.ext.login import current_user
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm.util import aliased
from sqlalchemy.sql.functions import func

from api_errors import UserNotFound
from mods import db

__author__ = "Philgyu, Seong"
__email__ = "phil@treasureisle.co"


class SessionType(object):
    EMAIL = "email"
    FB = "fb"
    TWITTER = "twitter"

    def __init__(self, type):
        self.type = type


class Session(object):
    def __init__(self, user_id, generated_access_token, username):
        session_user = User.query.filter(User.id == user_id).first()

        if session_user is None:
            raise UserNotFound

        self.id = session_user.id
        self.access_token = generated_access_token
        self.username = username

        self.types = []

        if session_user.password is not None:
            self.types.append(SessionType(SessionType.EMAIL))
        elif session_user.fb_id is not None:
            self.types.append(SessionType(SessionType.FB))
        elif session_user.twitter_id is not None:
            self.types.append(SessionType(SessionType.TWITTER))


class User(db.Model):
    # 소셜 계정 미적용
    id = db.Column(db.INT, primary_key=True)
    access_token = db.Column(db.VARCHAR(64))
    username = db.Column(db.VARCHAR(32), unique=True)
    email = db.Column(db.VARCHAR(64), unique=True)
    password = db.Column(db.VARCHAR(64))
    name = db.Column(db.VARCHAR(32))
    zipcode = db.Column(db.INT)
    address1 = db.Column(db.VARCHAR(128))
    address2 = db.Column(db.VARCHAR(128))
    recent_name = db.Column(db.VARCHAR(32))
    recent_zipcode = db.Column(db.INT)
    recent_add1 = db.Column(db.VARCHAR(128))
    recent_add2 = db.Column(db.VARCHAR(128))
    phone = db.Column(db.VARCHAR(16))
    level = db.Column(db.INT)
    point = db.Column(db.INT)
    region = db.Column(db.VARCHAR(32))
    seller_level = db.Column(db.INT)
    bank_account = db.Column(db.VARCHAR(32))
    biz_num = db.Column(db.VARCHAR(32))
    recommender_id = db.Column(db.INT)
    profile_thumb_url = db.Column(db.VARCHAR(128))
    last_logged_at = db.Column(db.DATETIME)
    introduce = db.Column(db.VARCHAR(64))
    created_at = db.Column(db.DATETIME)
    is_activated = db.Column(db.INT)

    post = db.relationship("Post", backref="user", cascade="all,delete", lazy="dynamic")
    like = db.relationship("Like", backref="user", cascade="all,delete", lazy="dynamic")
    reply = db.relationship("Reply", backref="user", cascade="all,delete", lazy="dynamic")
    basket = db.relationship("Basket", backref="user", cascade="all,delete", lazy="dynamic")

    def __init__(self, username, created_at, last_logged_at, profile_thumb_url, access_token="", level=0, point=0,
                 seller_level=0, is_activated=0,
                 password=None, name=None, zipcode=None, address1=None, address2=None,
                 recent_name=None, recent_zipcode=None, recent_add1=None, recent_add2=None,
                 phone=None, region=None, bank_account=None, biz_num=None, recommender_id=None,
                 introduce=None, email=None):
        self.access_token = access_token
        self.username = username
        self.email = email
        self.password = password
        self.name = name
        self.zipcode = zipcode
        self.address1 = address1
        self.address2 = address2
        self.recent_name = name
        self.recent_zipcode = recent_zipcode
        self.recent_add1 = recent_add1
        self.recent_add2 = recent_add2
        self.phone = phone
        self.level = level
        self.point = point
        self.region = region
        self.seller_level = seller_level
        self.bank_account = bank_account
        self.biz_num = biz_num
        self.recommender_id = recommender_id
        self.profile_thumb_url = profile_thumb_url
        self.last_logged_at = last_logged_at
        self.introduce = introduce
        self.created_at = created_at
        self.is_activated = is_activated

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anoymous(self):
        return False

    def get_id(self):
        return self.id

    @hybrid_property
    def is_me(self):
        if not current_user.is_authenticated:
            return False
        return current_user.id == self.id


class Post(db.Model):
    id = db.Column(db.INT, primary_key=True)
    post_type = db.Column(db.INT)
    user_id = db.Column(db.ForeignKey("user.id"))
    img_url1 = db.Column(db.VARCHAR(128))
    img_url2 = db.Column(db.VARCHAR(128))
    img_url3 = db.Column(db.VARCHAR(128))
    img_url4 = db.Column(db.VARCHAR(128))
    img_url5 = db.Column(db.VARCHAR(128))
    title = db.Column(db.VARCHAR(256))
    brand = db.Column(db.VARCHAR(64))
    product_name = db.Column(db.VARCHAR(64))
    origin_price = db.Column(db.INT)
    purchase_price = db.Column(db.INT)
    fee = db.Column(db.INT)
    region = db.Column(db.VARCHAR(32))
    hashtag = db.Column(db.VARCHAR(256))
    text = db.Column(db.VARCHAR(1024))
    replies = db.Column(db.INT)
    likes = db.Column(db.INT)
    created_at = db.Column(db.DATETIME)

    color_size = db.relationship("ColorSize", backref="post", cascade="all,delete", lazy="dynamic")
    like = db.relationship("Like", backref="post", cascade="all,delete", lazy="dynamic")
    reply = db.relationship("Reply", backref="post", cascade="all,delete", lazy="dynamic")
    purchase = db.relationship("Purchase", backref="post", cascade="all,delete", lazy="dynamic")
    hashtag_post = db.relationship("HashtagPost", backref="post", cascade="all,delete", lazy="dynamic")
    basket = db.relationship("Basket", backref="post", cascade="all,delete", lazy="dynamic")

    def __init__(self, post_type, user_id, title, brand, product_name, origin_price, purchase_price, fee,
                 region, text, created_at, replies=0, likes=0,
                 img_url1=None, img_url2=None, img_url3=None, img_url4=None, img_url5=None, hashtag=None):
        self.post_type = post_type
        self.user_id = user_id
        self.img_url1 = img_url1
        self.img_url2 = img_url2
        self.img_url3 = img_url3
        self.img_url4 = img_url4
        self.img_url5 = img_url5
        self.title = title
        self.brand = brand
        self.product_name = product_name
        self.origin_price = origin_price
        self.purchase_price = purchase_price
        self.fee = fee
        self.region = region
        self.hashtag = hashtag
        self.text = text
        self.replies = replies
        self.likes = likes
        self.created_at = created_at

    @hybrid_property
    def score(self):
        """
        랭킹 스코어, reddit score 적용
        https://github.com/reddit/reddit/blob/af09fa8dee69bef4f65a1662d9ad91c2329946e1/r2/r2/lib/db/_sorts.pyx
        :return:
        """
        started_at = 1426255018  # unix timestamp Fri Mar 13 13:56:58 2015 GMT
        time_factor = 3600 * 5
        order = func.log10(func.greatest((self.likes), 1))
        seconds = func.unix_timestamp(self.created_at) - started_at

        return func.round(order + seconds / time_factor, 7)

    @hybrid_property
    def is_liked(self):
        if not current_user.is_authenticated:
            return False
        my_like = Like.query.filter(Like.user_id == current_user.id). \
            filter(Like.post_id == self.id).first()

        return my_like is not None


class ColorSize(db.Model):
    id = db.Column(db.INT, primary_key=True)
    post_id = db.Column(db.ForeignKey("post.id"))
    name = db.Column(db.VARCHAR(32))
    available = db.Column(db.INT)
    created_at = db.Column(db.DATETIME)

    basket = db.relationship("Basket", backref="color_size", cascade="all,delete", lazy="dynamic")

    def __init__(self, post_id, name, available, created_at):
        self.post_id = post_id
        self.name = name
        self.available = available
        self.created_at = created_at


class Hashtag(db.Model):
    id = db.Column(db.INT, primary_key=True)
    name = db.Column(db.VARCHAR(32))
    number = db.Column(db.INT)
    created_at = db.Column(db.DATETIME)
    hidden = db.Column(db.INT)

    hashtag_post = db.relationship("HashtagPost", backref="hashtag", cascade="all,delete", lazy="dynamic")
    hashtag_score = db.relationship("HashtagScore", backref="hashtag", cascade="all,delete", lazy="dynamic")

    def __init__(self, name, created_at):
        self.name = name
        self.number = 0
        self.created_at = created_at
        self.hidden = 0

    @hybrid_property
    def score(self):
        """
        랭킹 스코어, reddit score 적용
        https://github.com/reddit/reddit/blob/af09fa8dee69bef4f65a1662d9ad91c2329946e1/r2/r2/lib/db/_sorts.pyx
        :return:
        """
        started_at = 1426255018  # unix timestamp Fri Mar 13 13:56:58 2015 GMT
        time_factor = 3600 * 5
        order = func.log10(func.greatest((self.number), 1))
        seconds = func.unix_timestamp(self.created_at) - started_at

        return func.round(order + seconds / time_factor, 7)


class HashtagPost(db.Model):
    id = db.Column(db.INT, primary_key=True)
    hashtag_id = db.Column(db.ForeignKey("hashtag.id"))
    post_id = db.Column(db.ForeignKey("post.id"))
    created_at = db.Column(db.DATETIME)

    def __init__(self, hashtag_id, post_id, created_at):
        self.hashtag_id = hashtag_id
        self.post_id = post_id
        self.created_at = created_at


class HashtagScore(db.Model):
    id = db.Column(db.INT, primary_key=True)
    hashtag_id = db.Column(db.ForeignKey("hashtag.id"))
    category_id = db.Column(db.ForeignKey("category.id"))
    score = db.Column(db.INT)

    def __init__(self, hashtag_id, category_id):
        self.hashtag_id = hashtag_id
        self.category_id = category_id
        self.score = 0


class Category(db.Model):
    id = db.Column(db.INT, primary_key=True)
    name = db.Column(db.VARCHAR(64))
    parent_id = db.Column(db.INT)
    depth = db.Column(db.INT)

    hashtag_score = db.relationship("HashtagScore", backref="category", cascade="all,delete", lazy="dynamic")

    def __init__(self, name, parent_id, depth):
        self.name = name
        self.parent_id = parent_id
        self.depth = depth


class Follow(db.Model):
    id = db.Column(db.INT, primary_key=True)
    follower_id = db.Column(db.ForeignKey("user.id"))
    following_id = db.Column(db.ForeignKey("user.id"))
    created_at = db.Column(db.DATETIME)

    def __init__(self, follower_id, following_id, created_at):
        self.follower_id = follower_id
        self.following_id = following_id
        self.created_at = created_at


class Like(db.Model):
    id = db.Column(db.INT, primary_key=True)
    user_id = db.Column(db.ForeignKey("user.id"))
    post_id = db.Column(db.ForeignKey("post.id"))
    created_at = db.Column(db.DATETIME)

    def __init__(self, user_id, post_id, created_at):
        self.user_id = user_id
        self.post_id = post_id
        self.created_at = created_at


class Reply(db.Model):
    id = db.Column(db.INT, primary_key=True)
    user_id = db.Column(db.ForeignKey("user.id"))
    post_id = db.Column(db.ForeignKey("post.id"))
    parent_id = db.Column(db.INT)
    depth = db.Column(db.INT)
    text = db.Column(db.VARCHAR(512))
    likes = db.Column(db.INT)
    replies = db.Column(db.INT)
    created_at = db.Column(db.DATETIME)

    replyLike = db.relationship("ReplyLike", backref="reply", cascade="all,delete", lazy="dynamic")

    def __init__(self, user_id, post_id, text, created_at, parent_id=0, depth=0):
        self.user_id = user_id
        self.post_id = post_id
        self.parent_id = parent_id
        self.depth = depth
        self.text = text
        self.likes = 0
        self.replies = 0
        self.created_at = created_at

    @hybrid_property
    def is_liked(self):
        if not current_user.is_authenticated:
            return False
        my_like = ReplyLike.query.filter(ReplyLike.user_id == current_user.id). \
            filter(ReplyLike.reply_id == self.id).first()

        return my_like is not None


class ReplyLike(db.Model):
    id = db.Column(db.INT, primary_key=True)
    user_id = db.Column(db.ForeignKey("user.id"))
    reply_id = db.Column(db.ForeignKey("reply.id"))
    created_at = db.Column(db.DATETIME)

    def __init__(self, user_id, reply_id, created_at):
        self.user_id = user_id
        self.reply_id = reply_id
        self.created_at = created_at


class Purchase(db.Model):
    id = db.Column(db.INT, primary_key=True)
    post_id = db.Column(db.ForeignKey("post.id"))
    seller_id = db.Column(db.ForeignKey("user.id"))
    buyer_id = db.Column(db.ForeignKey("user.id"))
    color_size_id = db.Column(db.ForeignKey("color_size.id"))
    amount = db.Column(db.INT)
    price = db.Column(db.INT)
    payment = db.Column(db.INT) # 0:카드 1:계좌이체 2:휴대폰결제
    zipcode = db.Column(db.INT)
    name = db.Column(db.VARCHAR(32))
    address1 = db.Column(db.VARCHAR(128))
    address2 = db.Column(db.VARCHAR(128))
    phone = db.Column(db.VARCHAR(16))
    comment = db.Column(db.VARCHAR(128))
    delivery_code = db.Column(db.INT)
    delivery_number = db.Column(db.VARCHAR(32))
    created_at = db.Column(db.DATETIME)

    def __init__(self, post_id, seller_id, buyer_id, color_size_id, amount, price, payment, name, zipcode, address1,
                 address2, phone, creaetd_at, comment=None, delivery_code=None, delivery_number=None):
        self.post_id = post_id
        self.seller_id = seller_id
        self.buyer_id = buyer_id
        self.color_size_id = color_size_id
        self.amount = amount
        self.price = price
        self.payment = payment
        self.name = name
        self.zipcode = zipcode
        self.address1 = address1
        self.address2 = address2
        self.phone = phone
        self.comment = comment
        self.delivery_code = delivery_code
        self.delivery_number = delivery_number
        self.created_at = creaetd_at


class Basket(db.Model):
    id = db.Column(db.INT, primary_key=True)
    user_id = db.Column(db.ForeignKey("user.id"))
    post_id = db.Column(db.ForeignKey("post.id"))
    color_size_id = db.Column(db.ForeignKey("color_size.id"))
    amount = db.Column(db.INT)
    created_at = db.Column(db.DATETIME)

    def __init__(self, user_id, post_id, color_size_id, amount, created_at):
        self.user_id = user_id
        self.post_id = post_id
        self.color_size_id = color_size_id
        self.amount = amount
        self.created_at = created_at


class Wish(db.Model):
    id = db.Column(db.INT, primary_key=True)
    user_id = db.Column(db.ForeignKey("user.id"))
    post_id = db.Column(db.ForeignKey("post.id"))
    created_at = db.Column(db.DATETIME)

    def __init__(self, user_id, post_id, created_at):
        self.user_id = user_id
        self.post_id = post_id
        self.created_at = created_at


class Message(db.Model):
    id = db.Column(db.INT, primary_key=True)
    sender_id = db.Column(db.ForeignKey("user.id"))
    reciever_id = db.Column(db.ForeignKey("user.id"))
    message = db.Column(db.VARCHAR(512))
    created_at = db.Column(db.DATETIME)

    sender = db.relationship("User", foreign_keys=[sender_id])
    reciever = db.relationship("User", foreign_keys=[reciever_id])

    def __init__(self, sender_id, reciever_id, message, created_at):
        self.sender_id = sender_id
        self.reciever_id = reciever_id
        self.message = message
        self.created_at = created_at


class Store(db.Model):
    id = db.Column(db.INT, primary_key=True)
    num_events = db.Column(db.INT)
    event1_hashtag_id = db.Column(db.INT)
    event1_img_url = db.Column(db.String)
    event2_hashtag_id = db.Column(db.INT)
    event2_img_url = db.Column(db.String)
    event3_hashtag_id = db.Column(db.INT)
    event3_img_url = db.Column(db.String)
    event4_hashtag_id = db.Column(db.INT)
    event4_img_url = db.Column(db.String)
    event5_hashtag_id = db.Column(db.INT)
    event5_img_url = db.Column(db.String)
    seller_id = db.Column(db.INT)
    today_seller_title = db.Column(db.String)
    editors_pick_hashtag_id = db.Column(db.INT)
    editors_pick_title = db.Column(db.String)

    def __init__(self, num_events, seller_id, today_seller_title, editors_pick_hashtag_id,
                 editors_pick_title, event1_hashtag_id, event1_img_url, event2_hashtag_id=None, event2_img_url=None,
                 event3_hashtag_id=None, event3_img_url=None, event4_hashtag_id=None, event4_img_url=None,
                 event5_hashtag_id=None, event5_img_url=None):
        self.num_events = num_events
        self.event1_hashtag_id = event1_hashtag_id
        self.event1_img_url = event1_img_url
        self.event2_hashtag_id = event2_hashtag_id
        self.event2_img_url = event2_img_url
        self.event3_hashtag_id = event3_hashtag_id
        self.event3_img_url = event3_img_url
        self.event4_hashtag_id = event4_hashtag_id
        self.event4_img_url = event4_img_url
        self.event5_hashtag_id = event5_hashtag_id
        self.event5_img_url = event5_img_url
        self.seller_id = seller_id
        self.today_seller_title = today_seller_title
        self.editors_pick_hashtag_id = editors_pick_hashtag_id
        self.editors_pick_title = editors_pick_title

