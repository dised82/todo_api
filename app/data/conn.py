from .db import db_pool, db_trans
import psycopg as psyc
# from contextlib import contextmanager
from config import data_url
from psycopg import sql

#here lies the class tha that manages the database connexion 
data = data_url #this data will be taken in the config.py 

class Connexion ():

    def __init__(self):
        self._pool = db_pool(data)
        self._trans = db_trans(self._pool)
        self._pool.start()

    @property
    def pool(self):
        return self._pool
    @property
    def trans(self):
        return self._trans


    def __del__(self):
        self._pool.stop()

    def get_x(self, table:str, key:str, value:str):

        query = sql.SQL("select * from {} where {} = %s").format(
            sql.Identifier(table),
            sql.Identifier(key)
        )

        with self.trans.read_only() as cur:
            cur.execute(query, (value,))
            result = cur.fetchall()
            return result

    def get_all(self, table:str ):

        query = sql.SQL("select * from {}").format(sql.Identifier(table))

        with self.trans.read_only() as cur:
            cur.execute(query)
            result = cur.fetchall()
            return result

    def put(self, table:str, keys:list[str], values:list ):

        query = sql.SQL("insert into {} ({}) values ({}) returning *").format(
            sql.Identifier(table),
            sql.SQL(", ").join(map(sql.Identifier, keys)),
            sql.SQL(", ").join(sql.Placeholder() * len(keys))
        )

        with self.trans.transaction() as cur:
            cur.execute(query, values)
            return cur.fetchone()

