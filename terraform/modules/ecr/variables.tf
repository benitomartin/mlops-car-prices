# Define the variable for the ECR repository name
variable "ecr_repo_name" {
    type        = string
    description = "ECR repo name"
}

# Define the variable for the ECR image tag
variable "ecr_image_tag" {
    type        = string
    description = "ECR repo name"
    default = "latest"
}

# Define the variable for the local path to the Lambda function or Python file
variable "lambda_function_local_path" {
    type        = string
    description = "Local path to lambda function / python file"
}

# Define the variable for the local path to the Dockerfile
variable "docker_image_local_path" {
    type        = string
    description = "Local path to Dockerfile"
}

# Define the variable for the AWS region
variable "region" {
    type        = string
    description = "region"
    default = "eu-central-1"
}

# Define the variable for the AWS account ID
variable "account_id" {
    # The type is not explicitly defined, so it will default to string
    # There is no description provided for this variable
}
