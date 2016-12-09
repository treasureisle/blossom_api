# -*- coding:utf-8 -*-
from werkzeug.exceptions import HTTPException

__author__ = "Philgyu, Seong"
__email__ = "phil@treasureisle.co"


class AlreadyVoted(HTTPException):
    pass


class MyVoteNotFound(HTTPException):
    pass


class Forbidden(HTTPException):
    pass


class UserNotFound(HTTPException):
    pass


class CommentTooLong(HTTPException):
    pass


class CommentTooShort(HTTPException):
    pass


class CommentNotFound(HTTPException):
    pass


class PostNotFound(HTTPException):
    pass


class UserNotFound(HTTPException):
    pass


class NotValidAccessToken(HTTPException):
    pass


class WrongPassword(HTTPException):
    pass


class NotValidFbAccessToken(HTTPException):
    pass


class UsernameTooShort(HTTPException):
    pass


class UsernameTooLong(HTTPException):
    pass


class NotValidUsername(HTTPException):
    pass


class UsernameAlreadyTaken(HTTPException):
    pass


class NotValidEmail(HTTPException):
    pass


class EmailAlreadyTaken(HTTPException):
    pass


class UserAlreadyExist(HTTPException):
    pass


class NotAllowedListType(HTTPException):
    pass


class NotAllowedOrderType(HTTPException):
    pass


class TopicNotFound(HTTPException):
    pass


class TopicIdRequired(HTTPException):
    pass


class VoteEnded(HTTPException):
    pass


class PasswordTooShort(HTTPException):
    pass


class InternalServerError(HTTPException):
    pass


# message 는 소문자로 시작, 마침표를 찍지 않는다.
errors = {
    "AlreadyVoted": {
        "message": "already voted",
        "status": 409
    },
    "NextTopicNotFound": {
        "message": "next topic not exist",
        "status": 404
    },
    "Forbidden": {
        "message": "forbidden",
        "status": 403
    },
    "MyVoteNotFound": {
        "message": "my vote not exist",
        "status": 404
    },
    "SQLAlchemyError": {
        "message": "sql error",
        "status": 500
    },
    "UserNotFound": {
        "message": "user not found",
        "status": 404
    },
    "CommentTooLong": {
        "message": "comment is too long",
        "status": 400
    },
    "CommentTooShort": {
        "message": "comment is too short",
        "status": 400
    },
    "CommentNotFound": {
        "message": "comment not found",
        "status": 404
    },
    "PostNotFound": {
        "message": "post not found",
        "status": 404
    },
    "ForbiddenException": {
        "message": "forbidden",
        "status": 403,
    },
    "TopicTooLong": {
        "message": "topic is too long",
        "status": 400
    },
    "TopicTooShort": {
        "message": "topic is too short",
        "status": 400
    },
    "NotValidAccessToken": {
        "message": "access token is not valid",
        "status": 403
    },
    "WrongPassword": {
        "message": "wrong password",
        "status": 400
    },
    "NotValidFbAccessToken": {
        "message": "fb access token is not valid",
        "status": 403
    },
    "UsernameTooShort": {
        "message": "username is too short",
        "status": 400
    },
    "UsernameTooLong": {
        "message": "username is too long",
        "status": 400
    },
    "NotValidUsername": {
        "message": "username is not valid",
        "status": 400
    },
    "UsernameAlreadyTaken": {
        "message": "username is already taken",
        "status": 409
    },
    "NotValidEmail": {
        "message": "email is not valid",
        "status": 400
    },
    "EmailAlreadyTaken": {
        "message": "email is already taken",
        "status": 409
    },
    "UserAlreadyExist": {
        "message": "user already exist",
        "status": 409
    },
    "NotAllowedListType": {
        "message": "not allowed list type",
        "status": 400
    },
    "TopicNotFound": {
        "message": "topic not found",
        "status": 404
    },
    "TopicIdRequired": {
        "message": "topic id required",
        "status": 400
    },
    "VoteEnded": {
        "message": "vote next topic is ended",
        "status": 406
    },
    "NotAllowedOrderType": {
        "message": "not allowed order type",
        "status": 400
    },
    "PasswordTooShort": {
        "message": "password is too short",
        "status": 400
    },
    "InternalServerError": {
        "message": "something wrong with api server",
        "status": 500
    }
}
