from dagster import ConfigurableResource, resource

import requests
from requests import Response
from datetime import datetime


class NYTBooksResource(ConfigurableResource):

    API_KEY: str

    @resource(description='pulls lists of books by rank up to level 15 for a specific published date')
    def request_full_overview(self, published_date: datetime) -> Response:
        return requests.get(f"https://api.nytimes.com/svc/books/v3/lists/full-overview.json?published_date={published_date}&api-key={self.API_KEY}")
    
