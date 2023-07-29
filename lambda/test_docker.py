# test_docker.py
import json
import requests 


# Create a sample event JSON object
# pylint: disable=R0801
# Similar lines of code in this file with test_lambda.py
sample_event = {
    "Records": [
        {
            "kinesis": {
                "data": {
                    "car_ID": 10,
                    "symboling": 0,
                    "CarName": "audi 5000s (diesel)",
                    "fueltype": "gas",
                    "aspiration": "std",
                    "doornumber": "two",
                    "carbody": "hatchback",
                    "drivewheel": "4wd",
                    "enginelocation": "front",
                    "wheelbase": 99.5,
                    "carlength": 178.2,
                    "carwidth": 67.9,
                    "carheight": 52,
                    "curbweight": 3053,
                    "enginetype": "ohc",
                    "cylindernumber": "five",
                    "enginesize": 131,
                    "fuelsystem": "mpfi",
                    "boreratio": 3.13,
                    "stroke": 3.4,
                    "compressionratio": 7,
                    "horsepower": 160,
                    "peakrpm": 5500,
                    "citympg": 16,
                    "highwaympg": 22,
                    "price": 17859.17
                }
            }
        }
    ]
}




url = 'http://localhost:8080/2015-03-31/functions/function/invocations'

headers = {'Content-Type': 'application/json'}

json_data = json.dumps(sample_event)
# Convert the sample event to JSON format
# json_data = json.dumps(sample_event)
print("json_data:", json_data)

# Get the response
response = requests.post(url, headers=headers, data=sample_event, timeout=5)
print("Response status code:", response.status_code)
print("Response headers:", response.headers)
print("Response text:", response.text)


try:
    response_json = response.json()
    prediction_events = response_json.get('Prediction Events', [])
    for event in prediction_events:
        print("Model Version:", event['Model Version'])
        print("Prediction:", event['Prediction'])
        print("Real Price:", event['Real Price'])
except ValueError as e:
    # Print the actual ValueError message instead of just "{ValueError}".
    print("Error:", str(e))


#   "body": "{\"error\": \"An error occurred (AccessDeniedException) when calling the 
# PutRecord operation: User: arn:aws:sts::406468071577:assumed-role/lambda-kinesis-role/car-model-prediction 
# is not authorized to perform: kinesis:PutRecord on resource: 
# arn:aws:kinesis:eu-central-1:406468071577:stream/car_events 
# because no identity-based policy allows the kinesis:PutRecord action\"}"
