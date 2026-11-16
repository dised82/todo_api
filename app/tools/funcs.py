import logging

from argon2 import PasswordHasher
from argon2.exceptions import InvalidHashError, VerificationError, VerifyMismatchError

from ..data.conn import Connexion
from ..data.models import do_list, element, user
from .errors import NotFound, Unauthorized

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
        return False
    except VerificationError:
        log.warning("password verification Error")
        return False


conn = Connexion()

# here lies every functions we need


def authenticate(username: str, password: str) -> user:
    x = conn.get_x("users", username=username)
    if x and verify(x["password_hash"], password):
        return user.dict_put(x)
    raise Unauthorized("Wrong username or password.")


# managing the lists as entities


def post_user(username: str, password: str) -> user:
    data = conn.post(
        "users", ["username", "password_hash"], [username, ph.hash(password)]
    )
    return user.dict_put(data)


def post_list(user_id, name: str) -> do_list:
    data = conn.post("list", ["user_id", "name"], [user_id, name])
    return do_list.dict_put(data)


def post_element(user_id, list_id, name, content="") -> element:
    if not conn.get_x("list", id=list_id, user_id=user_id):
        raise NotFound("list not found")
    if content == "":
        content = name

    data = conn.post(
        "element",
        ["user_id", "list_id", "name", "content"],
        [user_id, list_id, name, content],
    )
    return element.dict_put(data)


def get_lists(user_id) -> list[do_list]:
    data = conn.get_all("list", user_id=user_id)
    return [do_list.dict_put(x) for x in data]


def get_list(user_id, list_id) -> list[element]:
    data = conn.get_all("element", list_id=list_id, user_id=user_id)
    return [element.dict_put(i) for i in data]


def get_element(user_id, list_id, element_id) -> element | None:
    data = conn.get_x("element", id=element_id, list_id=list_id, user_id=user_id)
    if data is not None:
        return element.dict_put(data)
    return None
