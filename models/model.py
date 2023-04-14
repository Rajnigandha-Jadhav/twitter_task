from dataclasses import dataclass
from typing import List


@dataclass
class Posts:
    post: str

@dataclass
class User:
    userName: str
    fullName: str
    email: str
    password: str
    followers: List[str]
    following: List[str]
    postsAdded: List[Posts]
    postsOnHomePage: List[Posts]

@dataclass
class Follower:
    follower: str
