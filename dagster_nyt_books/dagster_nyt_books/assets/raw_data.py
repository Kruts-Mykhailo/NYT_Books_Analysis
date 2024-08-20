from datetime import datetime
from typing import Any, Dict

import pandas as pd
from dagster import AssetExecutionContext, asset

from ..resources.api import NYTBooksConnectionResource

BOOKS_FULL_OVERVIEW_FILE = "full-overview.json"


@asset(compute_kind="json")
def extract_full_overview(
    context: AssetExecutionContext, api_conn: NYTBooksConnectionResource
) -> Dict[str, Any]:
    current_date = datetime.strftime(datetime.now(), "%Y-%m-%d")
    context.log.info(f"Fetching bestseller lists for date {current_date}...")
    response = api_conn.request(endpoint="full-overview", published_date=current_date)
    context.log.info(f"Response status: {response.status_code}")
    return response.json()


@asset(
    deps=[extract_full_overview],
    compute_kind="pandas",
    io_manager_key="postgres_io_manager",
)
def raw_books(full_overview: Dict[str, Any], context: AssetExecutionContext):

    books_published = []

    published_date = full_overview["results"]["published_date"]
    published_date_cnvrt = datetime.strptime(published_date, "%Y-%m-%d").strftime(
        "%Y%m%d"
    )

    context.log.info(f"Processing {BOOKS_FULL_OVERVIEW_FILE}")

    for books_list in full_overview["results"]["lists"]:

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

    return pd.DataFrame(books_published)
