from boto3.session import Session

class AwsSession:
    def __init__(self, aws_access_key_id, aws_secret_access_key, aws_region):
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key
        self.aws_region = aws_region

    def get_dynamodb_resource(self):
        session = Session(region_name=self.aws_region,
                                aws_secret_access_key=self.aws_secret_access_key,
                                aws_access_key_id=self.aws_access_key_id)
        dynamodb_resource = session.resource('dynamodb')
        return dynamodb_resource

    def get_s3_client(self):
        session = Session(region_name=self.aws_region,
                                aws_secret_access_key=self.aws_secret_access_key,
                                aws_access_key_id=self.aws_access_key_id)
        s3_client = session.client('s3')
        return s3_client
