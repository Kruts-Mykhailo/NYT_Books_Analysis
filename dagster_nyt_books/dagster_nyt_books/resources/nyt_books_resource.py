import requests
from dagster import ConfigurableResource, EnvVar
from requests import Response


class NYTBooksConnectionResource(ConfigurableResource):

    def request(self, endpoint: str, **kwargs) -> Response:
        params = {"api-key": EnvVar("NYT_API_KEY").get_value()}
        kwargs.update(params)
        return requests.get(
            f"https://api.nytimes.com/svc/books/v3/{endpoint}.json", params=kwargs
        )
