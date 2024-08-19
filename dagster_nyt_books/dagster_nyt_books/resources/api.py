from dagster import asset, ConfigurableResource, EnvVar
import requests
from requests import Response

class NYTBooksConnectionResource(ConfigurableResource):

    def request(self, endpoint: str, **kwargs) -> Response:
        params = {'api-key': EnvVar.str("NYT_API_KEY")}
        params.update(kwargs)
        return requests.get(f"https://api.nytimes.com/svc/books/v3/{endpoint}.json", params=params)