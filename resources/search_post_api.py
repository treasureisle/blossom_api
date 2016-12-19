# -*- coding:utf-8 -*-

from flask.ext.restful import Resource, marshal_with, reqparse
from flask.globals import request

from common.fields import post_field
from common.api_errors import PostNotFound, NotAllowedSearchType
from common.models import Post, Hashtag, HashtagPost
from utils import api_login_required

__author__ = "Philgyu,Seong"
__email__ = "philgyu.seong@gluvi.co"

KEY_SEARCH_TYPE = "search_type"
KEY_KEYWORD = "keyword"

KEY_SEARCH_TYPE_TITLE = "title"
KEY_SEARCH_TYPE_HASHTAG = "hashtag"

LOCATION_FORM = "form"


class SearchPostApi(Resource):
    def __init__(self):
        self.post_parser = reqparse.RequestParser()
        self.post_parser.add_argument(KEY_SEARCH_TYPE, location=LOCATION_FORM)
        self.post_parser.add_argument(KEY_KEYWORD, location=LOCATION_FORM)

    @marshal_with(post_field, envelope="posts")
    def post(self):
        args = self.post_parser.parse_args()

        search_type = args[KEY_SEARCH_TYPE]
        keyword = args[KEY_KEYWORD]

        if search_type == KEY_SEARCH_TYPE_TITLE:
            words = keyword.split()
            posts = []

            perfect_posts = Post.query.filter(Post.title.like('%'+words+'%')).order_by(Post.score.desc()).all()
            for perfect_post in perfect_posts:
                perfect_post.search_score = 99999
                posts.append(perfect_post)

            for word in words:
                each_posts = Post.query.filter(Post.title.like('%'+word+'%')).order_by(Post.score.desc()).all()

                for searched_post in each_posts:
                    not_overlaped = True
                    for post in posts:
                        if post.id == searched_post.id:
                            post.search_score += 1
                            not_overlaped = False
                            break

                    if not_overlaped:
                        searched_post.search_score = 0
                        posts.append(searched_post)

            if len(posts) == 0:
                raise PostNotFound

            result = []

            for post in posts:
                not_inserted = True
                for index, result_post in enumerate(result):
                    print "post title: " + result_post.title
                    print "post score: %d" % result_post.search_score
                    print "index: %d" % index
                    if post.search_score > result_post.search_score:
                        print "keyword: " + post.title + ", score: %d" % post.search_score
                        result.insert(index, post)
                        not_inserted = False
                        break

                if not_inserted:
                    result.append(post)

        elif search_type == KEY_SEARCH_TYPE_HASHTAG:
            hashtags = Hashtag.query.filter(Hashtag.name.like('%'+keyword+'%')).all()
            hashtag_ids = [hashtag.id for hashtag in hashtags]

            hashtag_posts = HashtagPost.query.filter(HashtagPost.hashtag_id.in_(hashtag_ids)).all()
            post_ids = [hashtag_post.post_id for hashtag_post in hashtag_posts]

            result = Post.query.filter(Post.id.in_(post_ids)).ordey_by(Post.score.desc()).all()

            if result is None:
                raise PostNotFound
        else:
            raise NotAllowedSearchType

        return result
