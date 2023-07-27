# test_docker.py
import requests 
import json


# Create a sample event JSON object
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

# Convert the sample event to JSON format
json_data = json.dumps(sample_event)

# response = requests.post(url, json=sample_event)
response = requests.post(url, headers=headers, json={"sample_event": sample_event}, timeout=5)

# print("Response status code:", response.status_code)
# print("Response headers:", response.headers)
# print("Response text:", response.text)
# print("json_data:", json_data)


try:
    response_json = response.json()
    prediction_events = response_json.get('Prediction Events', [])
    for event in prediction_events:
        print("Model Version:", event['Model Version'])
        print("Prediction:", event['Prediction'])
        print("Real Price:", event['Real Price'])
except ValueError:
    print("Response is not in JSON format.")