import uuid
from contextlib import contextmanager

from psycopg.rows import dict_row
from psycopg_pool import ConnectionPool


class db_pool:
    def __init__(self, database_url) -> None:
        self.dsn = database_url
        self._pool = None
        self.start()

    def start(self):
        if not self._pool is None:
            self.stop()
        self._pool = ConnectionPool(
            self.dsn,
            min_size=2,
            max_size=10,
            check=ConnectionPool.check_connection,
            kwargs={"row_factory": dict_row},
            open=False,
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
    def transaction(self):  # the basic to read and write everything
        with (
            self._db.pool.connection() as conn,
            conn.cursor(row_factory=dict_row) as cur,
        ):
            yield cur

    @contextmanager
    def read_only(self):  # the read_only
        with (
            self._db.pool.connection() as conn,
            conn.cursor(row_factory=dict_row) as cur,
        ):
            cur.execute("SET TRANSACTION READ ONLY")
            yield cur

    @contextmanager
    def cursor_server(self, itersize: int = 2000):  # for larges strams
        with (
            self._db.pool.connection() as conn,
            conn.cursor(name=f"cur_{uuid.uuid4().hex}", row_factory=dict_row) as cur,
        ):
            cur.itersize = itersize
            yield cur
