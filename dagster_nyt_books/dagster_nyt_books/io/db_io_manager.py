import pandas as pd
from dagster import EnvVar, InputContext, IOManager, OutputContext, io_manager

from ..resources.db_conn import get_sql_conn  # type: ignore


class PostgresDataframeIOManager(IOManager):
    def __init__(self) -> None:
        self.name = EnvVar("PG_DBNAME")

    def handle_output(self, context: OutputContext, obj: pd.DataFrame):

        if obj is None:
            return

        table_name = context.asset_key.path[-1]

        with get_sql_conn(context) as conn:
            obj.to_sql(table_name, conn, if_exists="append", index=False)

        context.add_output_metadata(
            {
                "db_name": self.name,
                "num_rows": len(obj),
                "table_name": table_name,
            }
        )

    def load_input(self, context: InputContext) -> pd.DataFrame:

        table_name = context.asset_key.path[-1]

        with get_sql_conn(context) as conn:
            df = pd.read_sql(f"SELECT * FROM public.{table_name}", conn)

        return df


@io_manager
def postgres_io_manager(_):
    return PostgresDataframeIOManager()
