from datetime import datetime
from typing import Any, Dict

import pandas as pd
import requests
from dagster import AssetExecutionContext, asset, AssetIn

from ..resources.api import NYTBooksConnectionResource

BOOKS_FULL_OVERVIEW_FILE = "full-overview.json"


@asset(compute_kind="json",
       description="Extracts all bestseller lists of books with full-overview from NYT Books API by current date.")
def extract_full_overview(
    context: AssetExecutionContext, api_conn: NYTBooksConnectionResource
) -> Dict[str, Any]:
    current_date = datetime.strftime(datetime.now(), "%Y-%m-%d")
    context.log.info(f"Fetching bestseller lists for date {current_date}...")
    try:
        response = api_conn.request(endpoint="lists/full-overview", published_date=current_date)
        context.log.info(f"Response status: {response.status_code}")

        if response.status_code != 200:
            context.log.error(f"Failed to fetch data: {response.status_code} - {response.text}")
            response.raise_for_status()  

        return response.json()

    except requests.exceptions.RequestException as e:
        context.log.error(f"Request failed: {str(e)}")
        raise


@asset(
    ins={"upstream": AssetIn(key="extract_full_overview")},
    compute_kind="pandas",
    io_manager_key="postgres_io_manager",
    description="Compute result of GET requst in a DataFrame and ingesting result in a PostgreSQL db."
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

    return pd.DataFrame(books_published)

