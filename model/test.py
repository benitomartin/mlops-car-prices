## test.py file

import os
import requests
from dotenv import load_dotenv
from pathlib import Path


# Load environmental variables
load_dotenv()


# URL of the Flask API endpoint
url = 'http://localhost:9696/predict'

try:
    # Send a POST request to the Flask API with the data_path as JSON data in the request body
    # Set a timeout of 5 seconds for the request
    data_path = "C:\\Users\\bmart\\OneDrive\\11_MLOps\\mlops-car-prices\\data\\test_sample.csv"
    response = requests.post(url, json={"data_path": data_path}, timeout=5)

    # Check if the response status code is successful (e.g., 200 OK)
    response.raise_for_status()

    # Print the JSON response containing the predicted values
    print(response.json())

except requests.exceptions.Timeout:
    # If the request timed out (took more than 5 seconds), handle the timeout exception
    print("The request timed out.")

except requests.exceptions.RequestException as e:
    # If any other request-related exception occurred, handle the exception
    print(f"An error occurred: {e}")
