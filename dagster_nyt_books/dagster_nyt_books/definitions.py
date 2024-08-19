from dagster import Definitions
from dagster_dbt import DbtCliResource
from .assets import dbt_nyt_books_dbt_assets
from .project import dbt_nyt_books_project
from .schedules import schedules
from .resources.api import NYTBooksConnectionResource

defs = Definitions(
    assets=[dbt_nyt_books_dbt_assets],
    schedules=schedules,
    resources={
        "api_conn": NYTBooksConnectionResource(),
        "dbt": DbtCliResource(project_dir=dbt_nyt_books_project),
    },
)