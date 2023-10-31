import json

import requests

from gql_sqs_subscription.concerto.queries import (
    all_sqs_subscription_query,
    asset_lifecycle_subscription,
)
from gql_sqs_subscription.models import ConcertoRequest

# URL = "https://concerto-adapters.qa.enbala-engine.com/3.0/graphql"
URL = "http://localhost:4000/3.0/graphql"

OAUTH_TOKEN = "eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJhcHBsaWNhdGlvbiI6eyJpZCI6ImE0ZmUyZjY1ZDAyZDY0YzY4MTZhMTc1YmFiNDY3ZDQwZTI2MzQ2ZWNiNGUxYmM0N2I1MzU5Y2I1NzQzNWFjNDcifSwiYXVkIjoiZW5iYWxhX3ZwcCIsImV4cCI6MTY5ODg2MDgwNywiaWF0IjoxNjk4Nzc0NDA3LCJpc3MiOiJlbmJhbGFfdnBwIiwianRpIjoiYWIxMTliZTItNzgzZS00MWY1LTliZDItNmQxMGNiYzk0YTg4IiwibmJmIjoxNjk4Nzc0NDA2LCJzY29wZXMiOlsiYXNzZXRfbWFuYWdlIiwic3Vic2NyaXB0aW9uX21hbmFnZSJdLCJzdWIiOiJhNGZlMmY2NWQwMmQ2NGM2ODE2YTE3NWJhYjQ2N2Q0MGUyNjM0NmVjYjRlMWJjNDdiNTM1OWNiNTc0MzVhYzQ3IiwidHlwIjoiYWNjZXNzIn0.tWF_bD0vP5p_iMrlYjNJj2n0ljyrj-kNZzx-ZjEVh3yMzawnwYhHpDHqCR9uOIi7qSLnTz_h2MwxwDkLXGdSug"

QUEUE_URL = "https://sqs.us-west-2.amazonaws.com/968796807695/gql-sqs-serverless-subscription-AssetSubscriptionQueue-lrulaKK45Bmj"

STS_ACCESS_KEY = "ASIA6DEGKEIH4SNHWJOD"
STS_SECRET_ACCESS_KEY = "k40pUnpOjQqvyTvDKuH5AvJX/kjngxrdLh+ZfVLV"
STS_TOKEN = "IQoJb3JpZ2luX2VjEMr//////////wEaCXVzLXdlc3QtMiJHMEUCIGf75HbKXGqo/ra9VVBZnOTFuzmLbcC1Kj578U0M8WXwAiEA561AXmKoCn7a6p1x9PJeuT6lpt+J6XxbpNSmAcNVpJ4qkwII8///////////ARAAGgw5Njg3OTY4MDc2OTUiDPE8u4JOSk0eAbBIrirnATq46ovNsjKgSiGdTUW2TT+353vaHrZEWYRHBJ0ppzp1KvkmfbwcT73QI7pXOO/6A3Krkx5WjlwpkURXR6g63pviBQdKkhGwMDOA3wYzihT5BKxXHAcA/LFjHINDyrIf5eTBwZRrHKiLTXano+iXWFjCEzlZpnBDC0/E4ddFevZWLQKPWyhxAmI8c7t+dIc9hRX0dePCpbEByZ2QqKykFQ2+9GMWMHCjM/QvvGi+NHNyMqaK6vT4PgH7fc4I8eSPyp3F2j2NSPIb4RMocrPrDGsVrhbjj6WN+UGvHA+JZDGdY2QSJ3M1UjDS/ISqBjqZAVynV9xn4hL+mWmLRCC5UucDHqVQwTuYRWpxXBvv9CEcmvw48RmjfPKAaKJoV9Dej5GcmjFOPfjrFv+S5hjvqNcK8o6NvG2tBpamwFGQ+KfUmNyHwJWBDLzFOXt9C49ldF8l3GNxrJEJCO9eBg/8nqQOCvhDKdWCc5skEz8oEqbSSuYECJvaK/D6Dm1fJDPXbwJ/KTClhujtaQ=="


def _send_request(request: ConcertoRequest) -> dict:
    """Concerto API request handler, handles retry logic and rate limit requests"""
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + OAUTH_TOKEN,
    }
    headers.update(request.headers)

    response = requests.request(
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


concerto_request = ConcertoRequest(
    method="POST",
    url=URL,
    headers={
        "subscription-name": "test-subscription-mason",
        "subscription-transport": "SQS",
        "subscription-sqs-queue-url": QUEUE_URL,
        "subscription-sqs-access-key-id": STS_ACCESS_KEY,
        "subscription-sqs-secret-access-key": STS_SECRET_ACCESS_KEY,
        "subscription-sqs-security-token": STS_TOKEN,
    },
    data=asset_lifecycle_subscription(),
    message_attributes={},
)

response = _send_request(concerto_request)
response_payload = response.json()
