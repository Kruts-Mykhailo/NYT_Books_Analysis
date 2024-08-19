from dagster import asset
from resources.api import NYTBooksConnectionResource

from datetime import datetime
from typing import Dict, Any

from dagster_po

BOOKS_FULL_OVERVIEW_FILE = 'full-overview.json'


@asset(compute_kind='json')
def extract_full_overview(api_conn: NYTBooksConnectionResource) -> Dict[str, Any]:
    current_date = datetime.strftime(datetime.now(), '%Y-%m-%d')
    return api_conn.request(endpoint='full-overview', published_date=current_date).json()


@asset(deps=[extract_full_overview], compute_kind='python')
def lists_api_ingest(full_overview: Dict[str, Any]):
    raise NotImplementedError


@asset(deps=[extract_full_overview], compute_kind='python')
def books_api_ingest():
    raise NotImplementedError

