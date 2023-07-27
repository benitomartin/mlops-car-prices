# Make sure to create state bucket beforehand
terraform {
  required_version = ">= 1.0"
  
# Define the S3 backend configuration to store Terraform state
backend "s3" {
  bucket  = "tf-state-ben"                # Name of the "state" S3 bucket to store state
  key     = "mlops-zoomcamp-stg.tfstate"  # Name of the "state" file within the bucket
  region  = "eu-central-1"                # AWS region where the S3 bucket resides
  encrypt = true                          # Enable server-side encryption for the state file
}

}

# Define the AWS provider configuration to specify the region
provider "aws" {
  region = var.aws_region
}

# Use the "aws_caller_identity" data source to get information about the AWS account
data "aws_caller_identity" "current_identity" {}

# Define a local variable to store the AWS account ID obtained from the data source
locals {
  account_id = data.aws_caller_identity.current_identity.account_id
}

# Create a Kinesis stream for ride_events using the custom module "kinesis"
module "source_kinesis_stream" {
  source = "./modules/kinesis"
  retention_period = 48                                       # Retention period for Kinesis data (in hours)
  shard_count = 2                                             # Number of shards for the Kinesis stream
  stream_name = "${var.source_stream_name}-${var.project_id}" # Name of the "Source" Kinesis stream
  tags = var.project_id                                       # Tags to be associated with the Kinesis stream
}


# Create another Kinesis stream for ride_predictions using the custom module "kinesis"
module "output_kinesis_stream" {
  source = "./modules/kinesis"
  retention_period = 48                                       # Retention period for Kinesis data (in hours)
  shard_count = 2                                              # Number of shards for the Kinesis stream
  stream_name = "${var.output_stream_name}-${var.project_id}" # Name of the "Output" Kinesis stream
  tags = var.project_id                                       # Tags to be associated with the Kinesis stream
}

# Create an S3 bucket for model storage using the custom module "s3"
module "s3_bucket" {
  source = "./modules/s3"
  bucket_name = "${var.model_bucket}-${var.project_id}" # Name of the S3 bucket
}

# Create an Elastic Container Registry (ECR) repository for image storage using the custom module "ecr"
module "ecr_image" {
  source = "./modules/ecr"
  ecr_repo_name = "${var.ecr_repo_name}_${var.project_id}"    # Name of the ECR repository
  account_id = local.account_id                               # AWS account ID where the ECR repository will be created
  lambda_function_local_path = var.lambda_function_local_path # Local path to the Lambda function code
  docker_image_local_path = var.docker_image_local_path       # Local path to the Docker image
}

module "lambda_function" {
  source = "./modules/lambda"
  image_uri = module.ecr_image.image_uri
  lambda_function_name = "${var.lambda_function_name}_${var.project_id}"
  model_bucket = module.s3_bucket.name
  output_stream_name = "${var.output_stream_name}-${var.project_id}"
  output_stream_arn = module.output_kinesis_stream.stream_arn
  source_stream_name = "${var.source_stream_name}-${var.project_id}"
  source_stream_arn = module.source_kinesis_stream.stream_arn
}