import boto3

_lambda_client = None


class LambdaClient:
    """AWS lambda wrapper.

    This detached class helps to mock lambda interactions in tests.
    """

    def __init__(self):
        global _lambda_client

        if _lambda_client is None:
            _lambda_client = boto3.client("lambda")

        self.client = _lambda_client

    def invoke(self, **kwargs) -> None:  # noqa
        self.client.invoke(**kwargs)
