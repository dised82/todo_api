# this file all the contains data models used in this program
from dataclasses import dataclass
from date import Date
from typing import dataclass_transform


@dataclass
class user:
    id : int # id
    name: str # name
    uname : str # username
    cr_date : date # creation date type date 


@dataclass
class list:
    id : int 
    name : str 
    user_id : int 


@dataclass
class element:
    id : int
    list_id: int
    name: str # the title of the element in the list
    content : str # the content of the task by default same as the title
    state : bool # the state of the task checked or unchecked
