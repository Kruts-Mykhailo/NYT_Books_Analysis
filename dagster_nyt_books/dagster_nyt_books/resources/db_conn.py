from contextlib import contextmanager
from typing import Iterator

from dagster import EnvVar
from sqlalchemy import Connection, create_engine


def get_pg_dsn() -> str:
    """Generate a DSN string for PostgreSQL connection."""

    required_vars = {
        "dbname": EnvVar("PG_DBNAME"),
        "user": EnvVar("PG_USERNAME"),
        "password": EnvVar("PG_PASSWORD"),
        "host": EnvVar("PG_HOST"),
        "port": EnvVar("PG_PORT"),
    }

    dsn_params = {}

    for key, env_var in required_vars.items():
        value = env_var.get_value()
        if not value:
            raise EnvironmentError(
                f"Environment variable {key} is missing or empty."
                )
        dsn_params[key] = value

    # Create the DSN string
    dsn = (
        f"postgresql://{dsn_params['user']}:"
        f"{dsn_params['password']}@"
        f"{dsn_params['host']}:"
        f"{dsn_params['port']}/"
        f"{dsn_params['dbname']}"
    )

    return dsn


@contextmanager
def get_sql_conn(io_context) -> Iterator[Connection]:
    """Return Postgres connection"""

    conn = None
    engine = create_engine(get_pg_dsn())
    try:
        conn = engine.connect()
        yield conn
    except Exception as e:
        io_context.log.error(f"Error connecting to Postgres: {e}")
        raise
    finally:
        if conn:
            conn.close()
