from datetime import datetime, timedelta
from typing import Any, Dict

import pandas as pd
import requests
from dagster import (AssetCheckExecutionContext, AssetCheckResult,
                     AssetExecutionContext, AssetIn, asset, asset_check)
from sqlalchemy import text

from ..resources.db_conn import get_sql_conn
from ..resources.nyt_books_resource import NYTBooksConnectionResource

BOOKS_FULL_OVERVIEW_FILE = "full-overview.json"


@asset(
    compute_kind="json",
    description="""Extracts all bestseller lists of books
        with full-overview from NYT Books API by current date.""",
)
def extract_full_overview(
    context: AssetExecutionContext, api_conn: NYTBooksConnectionResource
) -> Dict[str, Any]:
    current_date = datetime.strftime(datetime.now(), "%Y-%m-%d")
    context.log.info(f"Fetching bestseller lists for date {current_date}...")
    try:
        response = api_conn.request(
            endpoint="lists/full-overview", published_date=current_date
        )
        context.log.info(f"Response status: {response.status_code}")

        if response.status_code != 200:
            context.log.error(
                f"Failed to fetch data: {response.status_code} - {response.text}"
            )
            response.raise_for_status()

        return response.json()

    except requests.exceptions.RequestException as e:
        context.log.error(f"Request failed: {str(e)}")
        raise


@asset(
    ins={"upstream": AssetIn(key="extract_full_overview")},
    compute_kind="pandas",
    io_manager_key="postgres_io_manager",
    description="Compute result of GET requst in a DataFrame and ingesting result in a PostgreSQL db.",
)
def raw_books(context: AssetExecutionContext, upstream: Dict[str, Any]):

    books_published = []

    published_date = upstream["results"]["published_date"]
    published_date_cnvrt = datetime.strptime(published_date, "%Y-%m-%d").strftime(
        "%Y%m%d"
    )

    context.log.info(f"Processing {BOOKS_FULL_OVERVIEW_FILE}")

    for books_list in upstream["results"]["lists"]:

        for book in books_list["books"]:
            books_published.append(
                {
                    "id": published_date_cnvrt + book["primary_isbn13"],
                    "age_group": book["age_group"],
                    "author": book["author"],
                    "book_uri": book["book_uri"],
                    "contributor": book["contributor"],
                    "contributor_note": book.get("contributor_note", ""),
                    "created_date": book["created_date"],
                    "description": book["description"],
                    "updated_date": book["updated_date"],
                    "updated_rate": books_list["updated"],
                    "price": book["price"],
                    "publisher": book["publisher"],
                    "published_date": published_date,
                    "primary_isbn10": book["primary_isbn10"],
                    "primary_isbn13": book["primary_isbn13"],
                    "list_id": books_list["list_id"],
                    "list_name": books_list["list_name"],
                    "rank": book["rank"],
                    "rank_last_week": book["rank_last_week"],
                    "weeks_on_list": book["weeks_on_list"],
                }
            )

    context.add_output_metadata({"num_rows": len(books_published)})
    df = pd.DataFrame(books_published)
    df["published_date"] = pd.to_datetime(df["published_date"])
    return df


@asset_check(asset=extract_full_overview, blocking=True)
def check_data_existance_by_date(context: AssetCheckExecutionContext):
    """Checks if the closest published date to the fetch date is present in the database"""
    check_passed = True

    fetch_date = datetime.now()
    start_date = datetime.strftime(fetch_date, "%Y-%m-%d")
    end_date = datetime.strftime(fetch_date + timedelta(days=7), "%Y-%m-%d")
    check_records_exist_query = """
        SELECT 1
        FROM raw_books
        WHERE published_date BETWEEN :start_date AND :end_date
    """
    check_table_exist_query = """
        SELECT EXISTS (
            SELECT 1
            FROM information_schema.tables
            WHERE table_schema = 'public'
            AND table_name = 'raw_books'
        )
    """
    try:
        with get_sql_conn(context) as conn:

            table_exists = conn.execute(text(check_table_exist_query)).scalar()

            if not table_exists:
                context.log.info(
                    "The 'raw_books' table does not exist. Skipping record existence check."
                )
            else:
                records_exist = conn.execute(
                    text(check_records_exist_query),
                    {"start_date": start_date, "end_date": end_date},
                ).fetchone()

                if not records_exist:
                    context.log.info(
                        f"Records for published date closest to {start_date} do not exist. Proceeding."
                    )
                else:
                    context.log.error(
                        f"Records for published date closest to {start_date} already exist in database."
                    )
                    check_passed = False

    except Exception as e:
        context.log.error(f"Error executing query: {e}")
        check_passed = False

    return AssetCheckResult(passed=check_passed)
