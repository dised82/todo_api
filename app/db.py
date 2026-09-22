import psycopg
from contextlib import contextmanager
from psycopg.errors import RaiseException
from psycopg.rows import dict_row
from psycopg_pool import ConnectionPool
from app.config import data_url
#from psycopg import sql

def conexion(user, password, port, database):

    data = f'postgresql://{user}:{password}@localhost:{port}/{database}'

    try:
        conn = psycopg.connect(data)
    except psycopg.Error as e :
        print ("postgreSQL error:", e )
    else:
        cur = conn.cursor()

#test = conexion('admin', 'kali', '5432', 'to_do')
#data = {'user':'admin', 'password':'kali', 'port':'5432', 'db': 'to_do'}


class db_pool:
    def __init__(self, database_url) -> None:
        self.dsn = database_url
        self._pool = None

    def start(self):
        self._pool = ConnectionPool(
            self.dsn,
            min_size=2,
            max_size=10,
            check=ConnectionPool.check_connection,
            kwargs={'row_factory':dict_row},
            open=False
        )
        self._pool.open()
        self._pool.wait()
        return self

    def stop(self):
        if self._pool:
            self._pool.close()
            self._pool = None

    @property
    def pool(self):
        if self._pool is None:
            raise RuntimeError("non started pool: use start().")
        return self._pool

class db_trans:
    def __init__(self, db: db_pool) -> None:
        self._db = db

    @contextmanager
    def transaction(self):
        with self._db.pool.connection() as conn :
            with conn.cursor(row_factory=dict_row) as cur:
                yield cur

    def read_only(self):
        with self._db.pool.connection() as conn:
            conn.read_only = True
            with conn.cursor(row_factory=dict_row) as cur:
                yield cur

    def cursor_server(self):
        with self._db.pool.connection() as conn:
            with conn.cursor(name="name",row_factory=dict_row) as cur:
                yield cur

pool = db_pool(data_url)
if pool._pool:
    print ('pool')
    pool.stop()
else:
    pool.start()
    pool.pool
    print('pooled')
    pool.stop()
