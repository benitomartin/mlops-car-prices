## predict.py file
import os
import mlflow
import pandas as pd
from flask import Flask, request, jsonify
from dotenv import load_dotenv

# Load environmental variables
load_dotenv()

# # Get the RUN_ID after running orchestrate_s3.py and save it in .env
RUN_ID = os.getenv("RUN_ID")
BUCKET_NAME = os.getenv("BUCKET_NAME")
EXPERIMENT_ID = os.getenv("EXPERIMENT_ID")

# # Path to the model
logged_model = f's3://{BUCKET_NAME}/{EXPERIMENT_ID}/{RUN_ID}/artifacts/models_mlflow'


# logged_model = 's3://mlflow-tracking-remote/29/aa806b4bc4044777a0a25d5b8a24d7d5/artifacts/models_mlflow'

# Load model as a PyFuncModel.
model = mlflow.pyfunc.load_model(logged_model)

dependencies = mlflow.pyfunc.get_model_dependencies(logged_model)
print(dependencies)