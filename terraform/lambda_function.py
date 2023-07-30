## lambda_function.py

# Import required libraries
import os
import logging
import json
from dotenv import load_dotenv
import lambda_model


# Load environment variables from .env file
load_dotenv()

# Read environment variables or use default values
PREDICTIONS_STREAM_NAME = os.getenv('PREDICTIONS_STREAM_NAME', 'car_predictions')
RUN_ID=os.getenv('RUN_ID')
TEST_RUN = os.getenv('TEST_RUN', 'False') == 'True'

# Initialize the model service using the lambda_model module
model_service = lambda_model.init(
    prediction_stream_name=PREDICTIONS_STREAM_NAME,
    run_id=RUN_ID,
    test_run=TEST_RUN,
)

# Set up logging to display logs in the console
logging.basicConfig(level=logging.DEBUG)


# Set up logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Create a console handler for displaying logs in CloudWatch logs
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

# Create a formatter and attach it to the handler
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)

# Add the console handler to the logger
logger.addHandler(console_handler)


# Lambda function handler
# Unused context argument is required
# pylint: disable=unused-argument
def lambda_handler(event, context):
    # pylint: disable=unused-argument  
    # Debug using print statements
    print("Lambda function is running.")
    print(f"Event received: {event}")

    # Debug using logging statements
    logger.debug("Lambda function is running.")
    logger.debug(f"Event received: {event}")

    # Convert the event to a JSON string
    # event_json = json.dumps(event)

    # Call the model service with the JSON string
    prediction = model_service.lambda_handler(event)

    # Log the prediction value
    logger.debug(f"Prediction: {prediction}")

    return prediction
