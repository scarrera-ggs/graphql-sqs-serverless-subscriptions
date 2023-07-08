import json
import os

from gql_sqs_subscription.aws.lambda_client import LambdaClient
from gql_sqs_subscription.aws.secretsmanager import SecretsManager
from gql_sqs_subscription.concerto.api import ConcertoAPI
from gql_sqs_subscription.concerto.queries import authenticate_mutation
from gql_sqs_subscription.models import ConcertoRequest


def lambda_handler(event: dict, context: dict) -> None:
    """
    This Lambda rotate/update a Concerto access token in AWS Secrets Manager
    """
    CONCERTO_ROOT_URL = os.environ["CONCERTO_ROOT_URL"]
    CONCERTO_SECRETS_ARN = os.environ["CONCERTO_SECRETS_ARN"]

    (
        username,
        password,
        _,
    ) = SecretsManager().get_concerto_credentials(CONCERTO_SECRETS_ARN)

    concerto_request = ConcertoRequest(
        method="POST",
        url=CONCERTO_ROOT_URL + "/3.0/graphql",
        headers={},
        data=authenticate_mutation(username, password),
        message_attributes={},
    )
    response = ConcertoAPI(CONCERTO_SECRETS_ARN).send_request(concerto_request)
    response_payload = response.json()

    new_token = response_payload["data"]["authenticate"]["accessToken"]

    new_secret = {
        "username": username,
        "password": password,
        "token": new_token,
    }

    SecretsManager().update_concerto_token(CONCERTO_SECRETS_ARN, json.dumps(new_secret))
