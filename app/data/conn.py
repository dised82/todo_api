from psycopg import sql

from ..config import data_url
from .db import db_pool, db_trans

# import psycopg as psyc
# from contextlib import contextmanager

# here lies the class tha that manages the database connexion
data = data_url  # this data will be taken in the config.py


class Connexion:
    def __init__(self):
        self._pool = db_pool(data)
        self._trans = db_trans(self._pool)

    @property
    def pool(self):
        return self._pool

    @property
    def trans(self):
        return self._trans

    def __del__(self):
        if getattr(self, "_pool", None):
            self._pool.stop()

    def get_x(self, table: str, **filters):

        if not filters:
            raise ValueError("at least one filer is required")

        where = sql.SQL(" and ").join(
            sql.SQL("{} = %s").format(sql.Identifier(col)) for col in filters
        )

        query = sql.SQL("select * from {} where {}").format(
            sql.Identifier(table), where
        )

        with self.trans.read_only() as cur:
            cur.execute(query, tuple(filters.values()))
            result = cur.fetchone()
            return result

    def get_all(self, table: str, **filters):

        if not filters:
            raise ValueError("at least one filer is required")

        where = sql.SQL(" and ").join(
            sql.SQL("{} = %s").format(sql.Identifier(col)) for col in filters
        )

        query = sql.SQL("select * from {} where {}").format(
            sql.Identifier(table), where
        )

        with self.trans.read_only() as cur:
            cur.execute(query, tuple(filters.values()))
            result = cur.fetchall()
            return result

    def post(self, table: str, keys: list[str], values: list):

        query = sql.SQL("insert into {} ({}) values ({}) returning *").format(
            sql.Identifier(table),
            sql.SQL(", ").join(map(sql.Identifier, keys)),
            sql.SQL(", ").join(sql.Placeholder() * len(keys)),
        )

        with self.trans.transaction() as cur:
            cur.execute(query, values)
            row = cur.fetchone()
            if row is None:
                raise RuntimeError("returned no row")
            return row

    def delete(self, table: str, key: str, value):

        query = sql.SQL("delete from {} where {} = %s returning *").format(
            sql.Identifier(table), sql.Identifier(key)
        )

        with self.trans.transaction() as cur:
            cur.execute(query, (value,))
            return cur.fetchone()

    def patch(self, table: str, data: dict, key: str, value):
        if not data:
            raise ValueError("nothing to update ")

        query = sql.SQL("update {} set {} where {} = %s returning *").format(
            sql.Identifier(table),
            sql.SQL(", ").join(
                sql.SQL("{} = %s").format(sql.Identifier(col)) for col in data
            ),
            sql.Identifier(key),
        )

        with self.trans.transaction() as cur:
            cur.execute(query, [*data.values(), value])
            return cur.fetchall()
