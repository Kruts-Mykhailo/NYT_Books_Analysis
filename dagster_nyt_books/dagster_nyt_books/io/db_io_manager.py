import pandas as pd
import psycopg2

from resources.db_conn import get_pg_conn_params
from types import Dict
from dagster import (

    IOManager,
    InputContext,
    OutputContext,
    io_manager,
)

class PostgresDataframeIOManager(IOManager):
    def __init__(self, conn_params: Dict[str, str]) -> None:
        self.conn_params = conn_params

    def handle_output(self, context: OutputContext, obj: pd.DataFrame):

        if obj is None:
            return

        table_name = context.asset_key.to_python_identifier()
        
        with psycopg2.connect(self.conn_params) as conn:
            obj.to_sql(table_name, conn, if_exists='append', index=False)

        context.add_output_metadata({"db_name": self.conn_params.get('dbname'), "num_rows": len(obj), "table_name": table_name})

    def load_input(self, context: InputContext):

        table_name = context.upstream_output.asset_key.to_python_identifier()
        
        with psycopg2.connect(self.conn_params)as conn:
            df = pd.read_sql( f"SELECT * FROM public.{table_name}", conn)
  
        return df


@io_manager
def postgres_io_manager(_):
    return PostgresDataframeIOManager(get_pg_conn_params())