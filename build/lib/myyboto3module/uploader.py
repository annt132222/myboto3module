from boto3 import client
from botocore.exceptions import NoCredentialsError, BotoCoreError
from botocore.config import Config as BotoConfig
from concurrent.futures import ThreadPoolExecutor
from .config import Config
import os
from .utils import create_metadata

class UpLoader:
    def __init__(self, file_paths, progress_callback=None, complete_callback=None):
        self.file_paths = file_paths
        self.progress_callback = progress_callback
        self.complete_callback = complete_callback
        self.upload_params = {}
        self.cumulative_bytes = {}
        config_para = Config.instance()
        self.s3_client = client(
            's3',
            endpoint_url=config_para.get("MINIO_ENDPOINT"),
            aws_access_key_id=config_para.get("MINIO_ACCESS_KEY"),
            aws_secret_access_key=config_para.get("MINIO_SECRET_KEY"),
            config=BotoConfig(signature_version='s3v4')
        )
        self.bucket_name = config_para.get("MINIO_BUCKET")

    def upload_files(self):
        executor = ThreadPoolExecutor(max_workers=3)
        for file_path in self.file_paths:
            executor.submit(self.upload_file, file_path)
        executor.shutdown(wait=False)

    def handle_callback(self, file_path, file_size, transferred):
        self.cumulative_bytes[file_path] += transferred
        progress_value = (self.cumulative_bytes[file_path] / file_size) * 100
        if self.progress_callback and callable(self.progress_callback):
            self.progress_callback(file_path, progress_value)

    def upload_file(self, file_path):
        try:
            file_name = file_path.split("/")[-1]
            file_size = os.path.getsize(file_path)
            self.cumulative_bytes[file_path] = 0
            
            self.s3_client.upload_file(file_path, 
                                       self.bucket_name, 
                                       file_name, 
                                       Callback=lambda bytes_transferred, *args: self.handle_callback(file_path, file_size, bytes_transferred), 
                                       )
            
        except NoCredentialsError:
            print("Error: Invalid MinIO credentials!")
        except BotoCoreError as e:
            print(f"Boto3 error: {str(e)}")
        except Exception as e:
            print(f"Error: {str(e)}")
        else:
            if self.progress_callback and callable(self.progress_callback):
                self.progress_callback(file_path, 100)
            print(f"{file_name} uploaded successfully!")
            create_metadata(file_name)
        finally:
            if self.complete_callback and callable(self.complete_callback):
                self.complete_callback(file_path)