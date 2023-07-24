## prefect_s3_bucket_block.py

from time import sleep
import os
from prefect_aws import S3Bucket, AwsCredentials
from dotenv import load_dotenv

# Load environmental variables
load_dotenv()

"""
This functions will create Bucket Blocks in prefect
Make sure to run "prefect server start" in a terminal before
"""    


def create_aws_creds_block():
    """
    Create and save AWS credentials object using environment variables.
    """

    my_aws_creds_obj = AwsCredentials(aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID"),
                                      aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY"))


    my_aws_creds_obj.save(name="my-aws-creds", 
                          overwrite=True)


def create_s3_bucket_block():
    """
    Create and save an S3 bucket object using the previously saved AWS credentials.
    """

    # Load Credentials
    aws_creds = AwsCredentials.load("my-aws-creds")

    BUCKET_NAME = os.getenv("BUCKET_NAME")

    # AWS Bucket Name (must be previously created)
    my_s3_bucket_obj = S3Bucket(bucket_name=BUCKET_NAME,
                                credentials=aws_creds)
    
    # Block Name in Prefect
    my_s3_bucket_obj.save(name=BUCKET_NAME,
                          overwrite=True)


if __name__ == "__main__":
    create_aws_creds_block()
    sleep(5)
    create_s3_bucket_block()
