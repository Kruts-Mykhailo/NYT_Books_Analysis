from pathlib import Path

from dagster_dbt import DbtProject

dbt_nyt_books_project = DbtProject(
    project_dir=Path(__file__).joinpath("..", "..", "..", "dbt_nyt_books").resolve(),
    packaged_project_dir=Path(__file__).joinpath("..", "..", "dbt-project").resolve(),
)
dbt_nyt_books_project.prepare_if_dev()