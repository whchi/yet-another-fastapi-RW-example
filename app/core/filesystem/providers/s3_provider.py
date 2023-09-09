from io import BytesIO
import logging

import boto3
from botocore.exceptions import ClientError

from app.core import get_app_settings
from app.core.filesystem.contracts.file_system_manager import (
    FileSystemManager,
)
from app.core.filesystem.file_util import FileUtil


class S3Provider(FileSystemManager):
    app_config = get_app_settings()

    def __init__(self) -> None:
        config = {
            'id': self.storage_config.AWS_ACCESS_KEY_ID,
            'secret': self.storage_config.AWS_SECRET_ACCESS_KEY,
            'region': self.storage_config.AWS_S3_REGION,
            'bucket': self.storage_config.AWS_S3_BUCKET,
        }
        self.config = config
        self.s3 = boto3.client('s3',
                               aws_access_key_id=config['id'],
                               aws_secret_access_key=config['secret'],
                               region_name=config['region'])

    @classmethod
    def register(cls) -> 'S3Provider':
        return cls()

    def read(self, filepath: str) -> bytes:
        s3_obj = self.s3.get_object(Bucket=self.config['bucket'], Key=filepath)
        response = s3_obj['Body'].read()
        return response

    def write(self, filepath: str, content: str | bytes, **kwargs: str | None) -> None:
        content = FileUtil.convert_content_type(content, BytesIO)  # type: ignore
        self.s3.upload_fileobj(
            content,
            self.config['bucket'],
            filepath,
            ExtraArgs={
                # 沒開 ACL，uncomment this line if aws acl is available
                # 'ACL': 'public-read',
                'ContentType': kwargs.get('content_type', 'application/octet-stream')
            })

    def exists(self, filepath: str) -> bool:
        try:
            response = self.s3.head_object(Bucket=self.config['bucket'], Key=filepath)
            return response['ResponseMetadata']['HTTPStatusCode'] == 200
        except ClientError as e:
            logging.info(e)
            return False

    def url(self, filename: str) -> str:
        return f'{self.app_config.APP_URL}/api/common/attachments/{filename}'

    def make_dirs(self, filepath: str) -> None:
        raise NotImplementedError(
            f'method make_dirs not implemented in {self.__class__}')

    def remove_file(self, filepath: str) -> None:
        self.s3.delete_object(Bucket=self.config['bucket'], Key=filepath)

    def remove_dir(self, dir_path: str) -> None:
        if dir_path[-1] != '/':
            raise ValueError('dir_path MUST endswith "/"')

        response = self.s3.list_objects(Bucket=self.config['bucket'], Prefix=dir_path)
        if 'Contents' in response:
            for obj in response['Contents']:
                self.remove_file(obj['Key'])
