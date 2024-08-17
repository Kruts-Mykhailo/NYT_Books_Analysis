from dagster import AssetExecutionContext, asset
from dagster_dbt import DbtCliResource, dbt_assets

from .project import dbt_nyt_books_project

import pandas as pd

@asset
def lists_df() -> pd.DataFrame:
    return pd.DataFrame()

@dbt_assets(manifest=dbt_nyt_books_project.manifest_path)
def dbt_nyt_books_dbt_assets(context: AssetExecutionContext, dbt: DbtCliResource):
    yield from dbt.cli(["build"], context=context).stream()
    