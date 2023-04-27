# %%
import os
import boto3
import boto3.s3
import botocore
from dotenv import load_dotenv
# %%
load_dotenv()

# %%

class S3Model():


    def __init__(self) -> None:

        if not os.path.exists('models'):
            os.makedirs('models')
            print('Models directory created successfully')
            
        session = boto3.Session(
            region_name='us-east-1',
            aws_access_key_id=os.environ.get('AWS_ACCESS_KEY'),
            aws_secret_access_key=os.environ.get('AWS_ACCESS_KEY_SECRET')
        )
        s3 = session.resource('s3')
        self.src_bucket = s3.Bucket(os.environ.get('AWS_BUCKET_NAME'))

    def download_model_in_directory(self, model_pickle_name:str):
        try:
            self.src_bucket.download_file(f"models/{model_pickle_name}", f"./models/{model_pickle_name}")
            
            print(f'{model_pickle_name} model file downloaded from AWS')
            
            return True
        except:
            print(f'{model_pickle_name} failed to downloaded from AWS')

            return False


# %%
S3ModelObj = S3Model()

# %%
# S3ModelObj.download_model_in_directory(model_pickle_name='250250042.pkl')

# %%
