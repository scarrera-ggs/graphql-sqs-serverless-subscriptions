def asset_lifecycle_subscription() -> dict:
    query = """
    subscription {
        assetLifeCycleEvents {
            __typename
            ... on AssetCreateEvent {
                asset {
                    remoteId
                    name
                    adapterConfiguration {
                        name
                    }
                }
            }
            ... on AssetDeleteEvent {
                deletedAsset {
                    remoteId
                }
            }
            ... on AssetUpdateEvent {
                asset {
                    adapterConfiguration {
                        name
                    }
                    name
                    remoteId
                }
            }
        }
    }
    """

    variables = {}

    return {"query": query, "variables": variables}


def authenticate_mutation(email: str, password: str) -> dict:
    query = """
    mutation authenticate($input: AuthenticateInput!) {
        authenticate(input: $input) {
            accessToken
        }
    }
    """

    variables = {"input": {"email": f"{email}", "password": f"{password}"}}

    return {"query": query, "variables": variables}


def all_sqs_subscription_query(current_page: int, per_page: int) -> dict:
    query = """
    query ($current_page: PosInteger!, $per_page: PosInteger!) {
        allSqsSubscriptions {
            totalCount
            data(currentPage: $current_page, perPage: $per_page) {
                sqsSubscriptions {
                    id
                    name
                }
            }
        }
    }
    """

    variables = {"current_page": current_page, "per_page": per_page}

    return {"query": query, "variables": variables}


def sqs_subscription_credentials_update_mutation(
    access_key_id: str,
    secret_access_key: str,
    security_token: str,
    subscription_id: str,
) -> dict:
    query = """
    mutation ($input: SqsSubscriptionCredentialsUpdateInput!) {
        sqsSubscriptionCredentialsUpdate(input: $input) {
            status
        }
    }
    """

    variables = {
        "input": {
            "accessKeyId": access_key_id,
            "secretAccessKey": secret_access_key,
            "securityToken": security_token,
            "subscriptionId": subscription_id,
        }
    }

    return {"query": query, "variables": variables}


# "variables": {k: v for k, v in variables.items() if v is not None},
