import os 

class conndata ():
    def __init__(self) -> None:
        self._user = 'admin'
        self._password = 'kali'
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

