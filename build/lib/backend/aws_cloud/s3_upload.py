import os
import time
import boto3
import botocore
from dotenv import load_dotenv
import datetime

load_dotenv()

session = boto3.Session(
        region_name=os.environ.get('AWS_REGION_NAME'),
        aws_access_key_id=os.environ.get('AWS_ACCESS_KEY'),
        aws_secret_access_key=os.environ.get('AWS_ACCESS_KEY_SECRET')
    )

s3 = session.resource('s3')


src_bucket = s3.Bucket('damg-aircast')

def file_upload(filname: str):
    now = datetime.datetime.now()
    now_str = now.strftime('%Y%m%d%H%M%S')

    src_bucket.upload_file(filname, f"raw-data/{now_str}.csv")


    return f"https://damg-aircast.s3.amazonaws.com/raw-data/{now_str}.csv"