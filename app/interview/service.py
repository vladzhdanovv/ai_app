import json

from uuid import uuid4

from botocore.exceptions import BotoCoreError, ClientError

from app.exception_handler import CustomBotoCoreError, CustomClientError


from app.session import AwsSession


def assign_candidate_id() -> str:
    return str(uuid4())


def save_to_s3(aws_session: AwsSession, bucket: str, filename: str, file_entry: dict):
    try:
        s3_client = aws_session.get_s3_client()
        s3_client.put_object(
            Bucket=bucket,
            Key=filename,
            Body=json.dumps(file_entry)
        )
    except BotoCoreError as e:
        raise CustomBotoCoreError("An error occurred in save_to_s3") from e
    except ClientError as e:
        raise CustomClientError("An error occurred in save_to_s3") from e


def save_to_dynamodb(aws_session: AwsSession, table_name: str, item: dict):
    try:
        dynamodb_resource = aws_session.get_dynamodb_resource()
        table = dynamodb_resource.Table(table_name)
        table.put_item(Item=item)
    except BotoCoreError as e:
        raise CustomBotoCoreError("An error occurred in save_to_dynamodb") from e
    except ClientError as e:
        raise CustomClientError("An error occurred in save_to_dynamodb") from e
