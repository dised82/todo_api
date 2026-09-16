from app.db import db_pool, db_trans
import psycopg as psyc
from contextlib import contextmanager

#here lies the class tha that manages the data
data = None #this data will be taken in the config.py 

class Connexion ():

    def __init__(self):
        self._pool = db_pool(data.user(), data.password(), data.port(), data.db())
        self._trans = db_trans(self._pool)
        self._pool.start()

    @property
    def pool(self):
        return self._pool
    @property
    def trans(self):
        return self._trans


    def __del__(self):
        self._pool.close()

    def get_x(self,table:str, key:str, value:str):
        with self.trans.read_only() as cur:
            cur.execute(f'select * from {table} where {key}: {value}')
            result = cur.fetchall()
            return result
