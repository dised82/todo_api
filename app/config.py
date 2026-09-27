import os
from datetime import timedelta

class config():

    SECRET_KEY = os.environ.get("SECRET_KEY", 'change_by_dev_only')

    PERMANENT_SESSION_LIFETIME = timedelta(days=7)

    SESSION_COOKIE_HTTPONLY = True  # javascript does not read the cookies 
    SESSION_COOKIE_SAMESITE ="Lax"  # basic CRSF protection
    SESSION_COOKIE_SECURE = False   # True in prod (https only)

class prod_config(config):

    SESSION_COOKIE_SECURE = True


class conndata ():
    def __init__(self) -> None:
        self._user = 'todo_conn'
        self._password = 'connexion_pass'
        self._port = '5432'
        self._db = 'to_do'

    @property
    def user(self):
        return self._user

    @property
    def password(self):
        return self._password

    @property
    def port (self):
        return self._port

    @property
    def db(self):
        return self._db

data = conndata()


data_url = os.environ.get("DATABASE_URL",f'postgresql://{data.user}:{data.password}@localhost:{data.port}/{data.db}')

