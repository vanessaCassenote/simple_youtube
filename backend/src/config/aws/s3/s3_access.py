import botocore
import boto3
from boto3.s3.transfer import TransferConfig
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env")

class S3:
    def __init__(self):
        self.s3 = boto3.client(
            service_name = "s3",
            region_name = os.getenv("REGION_NAME"),
            aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
        )
        self.config = TransferConfig() #multipart_threshold
        self.bucket = None
        self.key = None
        self.upload_id = None
    
    def create_multipart_upload(self, bucket, object_name):
        response = self.s3.create_multipart_upload( 
            Bucket=bucket,
            Key=object_name,
            ContentType="video/mp4",
        )
        self.bucket = bucket
        self.key = object_name
        self.upload_id = response['UploadId']
    
    def upload_part(self, file_to_upload, part_number):
        response = self.s3.upload_part(
            Body=file_to_upload,
            Bucket=self.bucket,
            Key=self.key,
            PartNumber=part_number,
            UploadId=self.upload_id
        )
        
        return  {
                    'ETag': response['ETag'],
                    'PartNumber': part_number,
                }
    
    def complete_multipart_upload(self, parts):
        response = self.s3.complete_multipart_upload(
            Bucket=self.bucket,
            Key=self.key,
            MultipartUpload={
                'Parts': parts, # list
            },
            UploadId=self.upload_id,
        )
        return response['Location']
        
    def get_client(self):
        return self.s3
