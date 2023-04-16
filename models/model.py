from dataclasses import dataclass
from typing import List,Optional
from dataclass_wizard import JSONSerializable

@dataclass
class Posts(JSONSerializable):
    post: str

@dataclass
class User(JSONSerializable):
    userName: str
    fullName: str
    email: str
    password: str
    followers: Optional[List[str]]
    following: Optional[List[str]]
    postsAdded: Optional[List[Posts]]
    postsOnHomePage: Optional[List[Posts]]

@dataclass
class Follower(JSONSerializable):
    follower: str
