import json
import os

import boto3

from gql_sqs_subscription.aws.lambda_client import LambdaClient
from gql_sqs_subscription.aws.secretsmanager import SecretsManager
from gql_sqs_subscription.concerto.api import ConcertoAPI
from gql_sqs_subscription.concerto.queries import (
    all_sqs_subscription_query,
    asset_lifecycle_subscription,
    sqs_subscription_credentials_update_mutation,
)
from gql_sqs_subscription.models import ConcertoRequest


def lambda_handler(event: dict, context: dict) -> None:
    QUEUE_URL = os.environ["ASSET_SUBSCRIPTION_QUEUE_URL"]
    CONCERTO_ROOT_URL = os.environ["CONCERTO_ROOT_URL"]
    CONCERTO_SECRETS_ARN = os.environ["CONCERTO_SECRETS_ARN"]
    IAM_USER_SECRETS_ARN = os.environ["ASSET_SUBSCRIPTION_USER_SECRETS_ARN"]
    SUBSCRIPTION_NAME = "sqs-asset-lifecycle-subscription"

    concerto_api = ConcertoAPI(CONCERTO_SECRETS_ARN)

    (
        fu_access_key,
        fu_secret_access_key,
        fu_token,
    ) = _get_federated_user_credentials(IAM_USER_SECRETS_ARN)

    (
        subscription_exists,
        subscription_id,
    ) = _subscription_exists(SUBSCRIPTION_NAME, concerto_api, CONCERTO_ROOT_URL)

    # if subscription exists update federated user credentials, else create subscription
    if subscription_exists:
        concerto_request = ConcertoRequest(
            method="POST",
            url=CONCERTO_ROOT_URL + "/3.0/graphql",
            headers={},
            data=sqs_subscription_credentials_update_mutation(
                fu_access_key,
                fu_secret_access_key,
                fu_token,
                subscription_id,
            ),
            message_attributes={},
        )

        response = concerto_api.send_request(concerto_request)
        response_payload = response.json()

        if "errors" in response_payload:
            _request_error_handler(response_payload["errors"])
            return

        print("Successfully update subscription federated user credentials")
    else:
        concerto_request = ConcertoRequest(
            method="POST",
            url=CONCERTO_ROOT_URL + "/3.0/graphql",
            headers={
                "subscription-name": SUBSCRIPTION_NAME,
                "subscription-transport": "SQS",
                "subscription-sqs-queue-url": QUEUE_URL,
                "subscription-sqs-access-key-id": fu_access_key,
                "subscription-sqs-secret-access-key": fu_secret_access_key,
                "subscription-sqs-security-token": fu_token,
            },
            data=asset_lifecycle_subscription(),
            message_attributes={},
        )

        response = concerto_api.send_request(concerto_request)
        response_payload = response.json()

        if "errors" in response_payload:
            _request_error_handler(response_payload["errors"])
            return

        subscription_id = response_payload["subscriptionId"]
        print(f"Subscription created. {subscription_id=}")


def _get_federated_user_credentials(iam_user_secrets_arn: str) -> tuple:
    # get iam user credentials to create federated user
    (
        iam_user_name,
        iam_user_access_key,
        iam_user_secret_access_key,
    ) = SecretsManager().get_iam_user_credentials(iam_user_secrets_arn)

    # get federated user credentials
    sts_client = boto3.client(
        "sts",
        aws_access_key_id=iam_user_access_key,
        aws_secret_access_key=iam_user_secret_access_key,
    )

    response = sts_client.get_federation_token(
        Name=iam_user_name,
        DurationSeconds=3600,
    )
    federated_user_credentials = response["Credentials"]

    sts_client.close()

    return (
        federated_user_credentials["AccessKeyId"],
        federated_user_credentials["SecretAccessKey"],
        federated_user_credentials["SessionToken"],
    )


def _subscription_exists(
    subscription_name: str,
    concerto_api: ConcertoAPI,
    concerto_root_url: str,
) -> tuple:
    # get existing subscriptions
    concerto_request = ConcertoRequest(
        method="POST",
        url=concerto_root_url + "/3.0/graphql",
        headers={},
        data=all_sqs_subscription_query(current_page=1, per_page=10),
        message_attributes={},
    )

    response = concerto_api.send_request(concerto_request)
    response_payload = response.json()

    if "errors" in response_payload:
        _request_error_handler(response_payload["errors"])
        return False, None

    subscriptions = response_payload["data"]["allSqsSubscriptions"]["data"][
        "sqsSubscriptions"
    ]

    for subscription in subscriptions:
        if subscription_name == subscription["name"]:
            print("Subscription found in Concerto instance, updating credentials.")
            return True, subscription["id"]

    print("Subscription wasn't found on Concerto instance, creating a new one.")
    return False, None


def _request_error_handler(response_errors: list) -> None:
    for error in response_errors:
        if error["message"] == "Unauthorized":
            print("Token expired or was not provided, fetching...")

            LambdaClient().invoke(
                FunctionName=os.environ["CONCERTO_TOKEN_ROTATION_ARN"],
                InvocationType="Event",
            )
        else:
            print(f"Received error from mutation. {error['path']=} {error['message']=}")
