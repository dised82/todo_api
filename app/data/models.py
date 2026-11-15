# this file all the contains data models used in this program
from dataclasses import dataclass, fields
from datetime import datetime


@dataclass
class data_root:
    @classmethod
    def dict_put(cls, data: dict):  # cls represent the class and self the instance
        names = {f.name for f in fields(cls)}
        return cls(**{k: v for k, v in data.items() if k in names})


@dataclass
class user(data_root):
    id: int  # id
    name: str  # name
    username: str  # username (same name as the column in db.sql)
    created_at: datetime  # creation date (timestamp column in db.sql)


@dataclass
class do_list(data_root):
    id: int
    name: str
    user_id: int


@dataclass
class element(data_root):
    id: int
    list_id: int
    name: str  # the title of the element in the list
    content: str  # the content of the task by default same as the title
    state: bool  # the state of the task checked or unchecked
