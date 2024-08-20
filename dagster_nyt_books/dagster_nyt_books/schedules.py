from typing import List

from dagster import ScheduleDefinition

# from dagster_dbt import build_schedule_from_dbt_selection

# from .assets.dbt import dbt_nyt_books_dbt_assets

schedules: List[ScheduleDefinition] = [
    #     build_schedule_from_dbt_selection(
    #         [dbt_nyt_books_dbt_assets],
    #         job_name="materialize_dbt_models",
    #         cron_schedule="0 0 * * *",
    #         dbt_select="fqn:*",
    #     ),
]
