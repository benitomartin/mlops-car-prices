## test_integration.py file
import os
import requests
import pytest
from dotenv import load_dotenv


# Load environmental variables
load_dotenv()


# URL of the Flask API endpoint
url = 'http://localhost:9696/predict'

TEST_DATA_PATH = os.getenv("TEST_DATA_PATH")


def test_prediction():
    
    # The file path of the CSV data you want to use for prediction
    data_path = f'/app/{TEST_DATA_PATH}'

    print(f'TEST_DATA_PATH: {data_path}')  # Add this line to print the value

    try:
        # Send a POST request to the Flask API with the data_path as JSON data in the request body
        # Set a timeout of 5 seconds for the request
        response = requests.post(url, json={"data_path": data_path}, timeout=5)

        # Check if the response status code is successful (e.g., 200 OK)
        response.raise_for_status()

        # Extract the JSON response containing the predicted values
        json_response = response.json()

        # Check if the response contains the 'prediction' key
        assert 'prediction' in json_response


    except requests.exceptions.Timeout:
        # If the request timed out (took more than 5 seconds), handle the timeout exception
        pytest.fail("The request timed out.")

    except requests.exceptions.RequestException as err:
        # If any other request-related exception occurred, handle the exception
        pytest.fail(f"An error occurred: {err}")