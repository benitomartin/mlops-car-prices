#!/bin/bash

AWS_REGION="eu-central-1"

# Dynamically generated by TF
export MODEL_BUCKET_PROD="stg-mlflow-models-car-owners-mlops-zoomcamp"
export PREDICTIONS_STREAM_NAME="stg_car_predictions-mlops-zoomcamp"
export LAMBDA_FUNCTION="stg_prediction_lambda_mlops-zoomcamp"

# Model artifacts bucket from the previous weeks (MLflow experiments)
export MODEL_BUCKET_DEV="mlflow-tracking-remote"

# Get latest RUN_ID from latest S3 partition.
# NOT FOR PRODUCTION!
# In practice, this is generally picked up from your experiment tracking tool such as MLflow or DVC
export RUN_ID=aa806b4bc4044777a0a25d5b8a24d7d5


# NOT FOR PRODUCTION!
# Just mocking the artifacts from training process in the Prod env
aws s3 sync s3://${MODEL_BUCKET_DEV} s3://${MODEL_BUCKET_PROD}

# Set new var RUN_ID in existing set of vars.
variables="{PREDICTIONS_STREAM_NAME=${PREDICTIONS_STREAM_NAME}, MODEL_BUCKET=${MODEL_BUCKET_PROD}, RUN_ID=${RUN_ID}}"

# https://docs.aws.amazon.com/lambda/latest/dg/configuration-envvars.html
aws lambda update-function-configuration --function-name ${LAMBDA_FUNCTION} --environment "Variables=${variables}"





