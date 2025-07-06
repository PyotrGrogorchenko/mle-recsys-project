import os
import boto3
import logging
import pandas as pd

class S3:

    def __init__(self, s3_path, logger = logging.getLogger()):

        self._logger = logger

        self._s3_client = boto3.client('s3', 
            endpoint_url = os.environ.get('MLFLOW_S3_ENDPOINT_URL'),
            aws_access_key_id = os.environ.get('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key = os.environ.get('AWS_SECRET_ACCESS_KEY'))

        self._S3_BUCKET_NAME = os.environ.get('S3_BUCKET_NAME')
        self._S3_PATH = s3_path


        
    def download_file(self, key, filename, **kwargs):
        '''
        Загружает файл из s3
        '''

        self._s3_client.download_file(
            self._S3_BUCKET_NAME,
            f'{self._S3_PATH}/{key}',
            filename)
        
        self._logger.info(f'Loaded data from s3: {key}')
        

if __name__ == '__main__':
    s3 = S3('recsys/recommendations')
    s3.download_file('recommendations.parquet', '../data/recommendations.parquet')   