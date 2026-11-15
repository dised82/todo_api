from psycopg import Error
from argon2 import PasswordHasher
from argon2.exceptions import InvalidHashError, VerificationError, VerifyMismatchError
import logging
# from psycopg.rows import dict_row

from ..data.models import *
from ..data.conn import Connexion
from ..data.models import user, do_list, element

ph = PasswordHasher()
log = logging.getLogger(__name__)


def verify(stored_hash, password):
    try:
        return ph.verify(stored_hash, password)
    except VerifyMismatchError:
        log.warning("password verification failed: incorrect password")
        return False
    except InvalidHashError:
        log.warning("invalid password hash")
        return None
    except VerificationError:
        log.warning("password verification Error")
        return None
    except Exception as e:
        log.warning("unexpected error during password verification")
        return False


conn = Connexion()

# here lies every functions we need


def auhtenticate(username: str, password: str) -> user | None:
    x = conn.get_x("users", username=username)
    if x and verify(x["password_hash"], password):
        return user.dict_put(x)
    return None


# managing the lists as entities


def post_user(username: str, password: str):

    try:
        return conn.post(
            "users", ["username", "password_hash"], [username, ph.hash(password)]
        )
    except Error as e:
        return e


def post_list(usr_id, name: str):

    try:
        return conn.post("list", ["user_id", "name"], [usr_id, name])
    except Error as e:
        return e


def post_element(user_id, list_id, name, content=""):
    if content == "":
        content = name
    try:
        return conn.post(
            "element",
            ["user_id", "list_id", "name", "content"],
            [user_id, list_id, name, content],
        )
    except Error as e:
        return e


def get_lists(user_id):

    try:
        data = conn.get_all("list", user_id=user_id)
    except Error as e:
        return e
    else:
        return [do_list.dict_put(x) for x in data]


def get_list(user_id, list_id):

    try:
        # x = conn.get_x("lists", id=list_id, user_id=id)
        data = conn.get_all("element", list_id=list_id, user_id=user_id)
    except Error as e:
        return e
    else:
        return [element.dict_put(i) for i in data]
    return None


def get_element(user_id, list_id, element_id):
    try:
        return conn.get_x("element", id=id, list_id=list_id)
    except Error as e:
        return e
