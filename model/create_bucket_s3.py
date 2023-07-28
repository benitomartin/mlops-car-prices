import os
import boto3
from dotenv import load_dotenv

# Load environmental variables
load_dotenv()

def create_s3_bucket(bucket_name):
    """
    Create an S3 bucket with the given name.

    This function uses the AWS SDK (boto3) to create a new S3 bucket with the specified name.
    The bucket name must be globally unique across all existing bucket names in Amazon S3.

    Parameters:
        bucket_name (str): The desired name for the new S3 bucket.

    Returns:
        None: The function does not return anything, but it creates the bucket on AWS.

    Raises:
        botocore.exceptions.ClientError: If there is an error creating the bucket.
    """
        
    s3_client = boto3.client('s3')
    s3_client.create_bucket(Bucket=bucket_name)
    print(f"Bucket '{bucket_name}' created successfully!")

if __name__ == "__main__":
    aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
    
    # Configure AWS credentials (this is optional if you have AWS CLI or environment variables set up)
    session = boto3.Session(aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
    
    BUCKET_NAME = os.getenv("BUCKET_NAME")
    print(f"Bucket name: {BUCKET_NAME}") 

    create_s3_bucket(BUCKET_NAME)
