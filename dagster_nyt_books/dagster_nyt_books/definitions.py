from dagster import Definitions, define_asset_job
from dagster_dbt import DbtCliResource

from .assets.dbt import dbt_nyt_books_dbt_assets
from .assets.raw_data import (check_data_existance_by_date,
                              extract_full_overview, raw_books)
from .project import dbt_nyt_books_project
from .resources.nyt_books_resource import NYTBooksConnectionResource
from .resources.pg_io_manager import PostgresDataframeIOManager
from .schedules import schedules

nyt_books_pipeline_job = define_asset_job(
    "process_nyt_books",
    description="Fetch data for books from api and load into a database.",
)

defs = Definitions(
    assets=[extract_full_overview, raw_books, dbt_nyt_books_dbt_assets],
    asset_checks=[check_data_existance_by_date],
    jobs=[nyt_books_pipeline_job],
    schedules=schedules,
    resources={
        "api_conn": NYTBooksConnectionResource(),
        "postgres_io_manager": PostgresDataframeIOManager(),
        "dbt": DbtCliResource(project_dir=dbt_nyt_books_project),
    },
)
