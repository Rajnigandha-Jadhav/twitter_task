from models.model import User,Posts,Follower
from marshmallow import Schema, fields, post_load, validate


class PostsSchema(Schema):
    post=fields.Str(required=True)

    @post_load
    def make_posts(self, data, **kwargs):
        return Posts(**data)



class UserSchema(Schema):
    userName = fields.Str(required=True)
    fullName = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Str(required=True)
    followers = fields.List(fields.Str(), missing=[])
    following = fields.List(fields.Str(), missing=[])
    postsAdded = fields.List(fields.Nested(PostsSchema), missing=[])
    postsOnHomePage = fields.List(fields.Nested(PostsSchema), missing=[])

    @post_load
    def make_user(self, data, **kwargs):
        return User(**data)

class FollowerSchema(Schema):
    follower=fields.Str(required=True)

    @post_load
    def make_follower(self, data, **kwargs):
        return Follower(**data)



