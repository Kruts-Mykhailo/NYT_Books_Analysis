from dagster import Definitions
from dagster_dbt import DbtCliResource

from .assets.dbt import dbt_nyt_books_dbt_assets
from .assets.raw_data import extract_full_overview, raw_books
from .io.db_io_manager import PostgresDataframeIOManager
from .project import dbt_nyt_books_project
from .resources.api import NYTBooksConnectionResource
from .schedules import schedules

defs = Definitions(
    assets=[extract_full_overview, raw_books, dbt_nyt_books_dbt_assets],
    schedules=schedules,
    resources={
        "api_conn": NYTBooksConnectionResource(),
        "postgres_io_manager": PostgresDataframeIOManager(),
        "dbt": DbtCliResource(project_dir=dbt_nyt_books_project),
    },
)
