import json


def lambda_handler(event: dict, context: dict) -> None:
    print(f"Received {event=}")

    messages = _extract_messages_from_records(event["Records"])
    for message in messages:
        subscription_type = message["__typename"]

        if subscription_type == "AssetDeleteEvent":
            print(message)
        else:
            asset_name = message["asset"]["name"]
            remote_id = message["asset"]["remoteId"]
            print(f"Processing... {subscription_type=} {asset_name=} {remote_id=}")


def _extract_messages_from_records(records: list) -> list:
    parsed_records = [json.loads(record["body"]) for record in records]

    return [
        record["result"]["data"]["assetLifeCycleEvents"] for record in parsed_records
    ]
