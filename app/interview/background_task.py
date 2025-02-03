from datetime import datetime

from .model import InterviewFileLogEntry, InterviewLogEntry
from .decorator import handle_background_exception
from .service import save_to_s3, save_to_dynamodb
from app.exception_handler import BackgroundTaskError
from app.session import AwsSession

@handle_background_exception
def save_data(
        aws_session: AwsSession,
        data: dict,
        bucket: str,
        table_name: str,
):
    try:
        current_time = datetime.now()
        file_entry = InterviewFileLogEntry(**data)

        filename = "{candidate_id}_{datetime}.json".format(candidate_id=data["candidate_id"],
                                                           datetime=current_time.strftime('%Y%m%d%H%M%S'))

        # Define the AWS S3 and DynamoDB operations

        save_to_s3(aws_session, bucket, filename, file_entry.model_dump())

        item_entry = InterviewLogEntry(**data)
        item_entry.file_path = filename
        item_entry.dt = current_time.isoformat()

        save_to_dynamodb(aws_session, table_name, item_entry.model_dump())
    except Exception as e:
        raise BackgroundTaskError("An error occurred in save_data") from e
