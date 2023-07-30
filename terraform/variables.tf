# Define the AWS region where resources will be created
variable "aws_region" {
  description = "AWS region to create resources"
  default     = "eu-central-1"
}

# Define the project_id variable to uniquely identify the project
variable "project_id" {
  description = "project_id"
  default = "mlops-zoomcamp"
}

# Define the source_stream_name variable to specify the name of the Kinesis stream for car events
variable "source_stream_name" {
  description = "Name of the Kinesis stream for car events"
  # No default value provided, it should be explicitly specified during Terraform apply
}

# Define the output_stream_name variable to specify the name of the Kinesis stream for car predictions
variable "output_stream_name" {
  description = "Name of the Kinesis stream for car predictions"
  # No default value provided, it should be explicitly specified during Terraform apply
}

# Define the model_bucket variable to specify the name of the S3 bucket for model storage
variable "model_bucket" {
  description = "Name of the S3 bucket for model storage"
  # No default value provided, it should be explicitly specified during Terraform apply
}

# Define the lambda_function_local_path variable to specify the local path to the Lambda function code
variable "lambda_function_local_path" {
  description = "Local path to the Lambda function code"
  # No default value provided, it should be explicitly specified during Terraform apply
}

# Define the docker_image_local_path variable to specify the local path to the Docker image
variable "docker_image_local_path" {
  description = "Local path to the Docker image"
  # No default value provided, it should be explicitly specified during Terraform apply
}

# Define the ecr_repo_name variable to specify the name of the ECR repository
variable "ecr_repo_name" {
  description = "Name of the ECR repository"
  # No default value provided, it should be explicitly specified during Terraform apply
}

variable "lambda_function_name" {
  description = "The name of the Lambda function"
  type        = string
  # Add any other required attributes for the variable, such as default value, etc.
}