import psycopg2
from dagster import EnvVar
from types import Dict

def get_pg_conn_params() -> Dict[str: str]:
    return {
        'dbname': EnvVar('PG_DBNAME'),
        'user': EnvVar('PG_USERNAME'),
        'password': EnvVar('PG_PASSWORD'),
        'host': EnvVar('PG_HOST'),
        'port': EnvVar('PG_PORT')
    }

def get_sql_conn():
    """Return Postgres connection"""
    
    conn = psycopg2.connect(get_pg_conn_params)

    try:
        return conn
    except:
        print("Error connecting to Postgres")