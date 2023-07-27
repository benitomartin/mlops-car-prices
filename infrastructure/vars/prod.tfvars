# Define the source Kinesis stream name for production environment
source_stream_name = "prod_car_events"                 # Name of the source Kinesis stream for car events

# Define the output Kinesis stream name
output_stream_name = "prod_car_predictions"            # Name of the output Kinesis stream for car predictions

# Define the name of the S3 bucket for model storage
model_bucket = "prod-mlflow-models-car-owners"         # Name of the S3 bucket where models are stored

# Define the local path to the Lambda function code or Python file
lambda_function_local_path = "./lambda_function.py"    # Local path to the Lambda function code

# Define the local path to the Dockerfile for building the Docker image
docker_image_local_path = "./Dockerfile"               # Local path to the Dockerfile

# Define the name of the Elastic Container Registry (ECR) repository for the Docker image
ecr_repo_name = "prod_stream_model_duration"            # Name of the ECR repository

# Define the name of the Lambda function
lambda_function_name = "prod_prediction_lambda"         # Name of the Lambda function


