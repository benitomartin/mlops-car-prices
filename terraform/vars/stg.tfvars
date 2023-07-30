# Define the source Kinesis stream name for staging environment
source_stream_name = "stg_car_events"                  # Name of the source Kinesis stream for car events in the staging environment

# Define the output Kinesis stream name for staging environment
output_stream_name = "stg_car_predictions"             # Name of the output Kinesis stream for car predictions in the staging environment

# Define the name of the S3 bucket for model storage in staging environment
model_bucket = "stg-mlflow-models-car-owners"          # Name of the S3 bucket where models are stored in the staging environment

# Define the local path to the Lambda function code or Python file
lambda_function_local_path = "./lambda_function.py"    # Local path to the Lambda function code

# Define the local path to the Dockerfile for building the Docker image
docker_image_local_path = "./Dockerfile"               # Local path to the Dockerfile

# Define the name of the Elastic Container Registry (ECR) repository for the Docker image in staging environment
ecr_repo_name = "stg_stream_model_duration"             # Name of the ECR repository in the staging environment

# Define the name of the Lambda function in staging environment
lambda_function_name = "stg_prediction_lambda"          # Name of the Lambda function in the staging environment
