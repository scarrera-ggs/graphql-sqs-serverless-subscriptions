import json

from boto3.session import Session

_secretsmanager_client = None


class SecretsManager:
    """AWS Secrets Manager wrapper.

    This class interacts with AWS Secrets Manager and helps to mock this resource in the tests.
    """

    def __init__(self):
        global _secretsmanager_client

        if _secretsmanager_client is None:
            session = Session()
            _secretsmanager_client = session.client("secretsmanager")

        self.client = _secretsmanager_client

    def get_iam_user_credentials(self, secret_arn: str) -> tuple:
        response = self.client.get_secret_value(SecretId=secret_arn)
        subscription_user_secrets = json.loads(response["SecretString"])

        return (
            subscription_user_secrets["user_name"],
            subscription_user_secrets["access_key"],
            subscription_user_secrets["secret_access_key"],
        )

    def get_concerto_credentials(self, secret_arn: str) -> tuple:
        response = self.client.get_secret_value(SecretId=secret_arn)
        concerto_secrets = json.loads(response["SecretString"])

        return (
            concerto_secrets["username"],
            concerto_secrets["password"],
            concerto_secrets["token"],
        )

    def update_concerto_token(self, secret_arn: str, new_secret_string: str) -> None:
        response = self.client.get_secret_value(SecretId=secret_arn)
        current_version_id = response["VersionId"]

        response = self.client.put_secret_value(
            SecretId=secret_arn,
            SecretString=new_secret_string,
            VersionStages=["AWSPENDING"],
        )
        new_version_id = response["VersionId"]

        self.client.update_secret_version_stage(
            SecretId=secret_arn,
            VersionStage="AWSCURRENT",
            MoveToVersionId=new_version_id,
            RemoveFromVersionId=current_version_id,
        )

        print("Successfully rotate Concerto token value")
