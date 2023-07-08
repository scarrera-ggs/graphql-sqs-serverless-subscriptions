import json
import os

import requests
from backoff import expo, on_exception
from ratelimit import RateLimitException, limits
from requests.adapters import HTTPAdapter

from gql_sqs_subscription.aws.secretsmanager import SecretsManager
from gql_sqs_subscription.models import ConcertoRequest

API_WORKERS = int(os.environ["CONCERTO_API_WORKERS"])
MAX_RETRIES = int(os.environ["CONCERTO_API_MAX_RETRY_ATTEMPTS"])
QUERY_TIMEOUT = int(os.environ["CONCERTO_QUERY_TIMEOUT_IN_SECONDS"])
REQUESTS_PER_PERIOD = int(os.environ["CONCERTO_API_REQUESTS_PER_PERIOD"])


class ConcertoAPI:
    """Concerto API Interface"""

    def __init__(self, concerto_secrets_arn: str):
        (
            username,
            password,
            token,
        ) = SecretsManager().get_concerto_credentials(concerto_secrets_arn)

        self.user = username
        self.password = password
        self.token = token

        self.session = requests.Session()
        adapter = HTTPAdapter(pool_connections=API_WORKERS, pool_maxsize=API_WORKERS)

        self.session.mount("https://", adapter)
        self.session.mount("http://", adapter)

        if self.user is None or self.password is None:
            raise Exception("Missing information in Concerto credentials secrets")

    @on_exception(
        expo,
        (
            RateLimitException,
            requests.exceptions.Timeout,
            requests.exceptions.ConnectionError,
            requests.exceptions.HTTPError,
        ),
        max_tries=MAX_RETRIES,
    )
    @limits(calls=REQUESTS_PER_PERIOD, period=1)
    def send_request(self, request: ConcertoRequest) -> dict:
        """Concerto API request handler, handles retry logic and rate limit requests"""
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.token}",
        }
        headers.update(request.headers)

        response = self.session.request(
            method=request.method,
            url=request.url,
            headers=headers,
            data=json.dumps(request.data),
        )

        response.raise_for_status()

        response_info = {
            "status_code": response.status_code,
            "reason": response.reason,
            "headers": response.headers,
            "payload": json.dumps(response.json()),
        }

        print(f"Concerto request info {request.model_dump_json()}")
        print(f"Concerto response info {response_info}")

        return response
