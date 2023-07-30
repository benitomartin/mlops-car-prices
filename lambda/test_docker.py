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
                        "kinesisSchemaVersion": "1.0",
                        "partitionKey": "1",
                        "sequenceNumber": "49642967535840470808541827224503229287713030842930429960",
                        "data": "eyJkYXRhIjogeyJjYXJfSUQiOiAxMCwgInN5bWJvbGluZyI6IDAsICJDYXJOYW1lIjogImF1ZGkgNTAwMHMgKGRpZXNlbCkiLCAiZnVlbHR5cGUiOiAiZ2FzIiwgImFzcGlyYXRpb24iOiAic3RkIiwgImRvb3JudW1iZXIiOiAidHdvIiwgImNhcmJvZHkiOiAiaGF0Y2hiYWNrIiwgImRyaXZld2hlZWwiOiAiNHdkIiwgImVuZ2luZWxvY2F0aW9uIjogImZyb250IiwgIndoZWVsYmFzZSI6IDk5LjUsICJjYXJsZW5ndGgiOiAxNzguMiwgImNhcndpZHRoIjogNjcuOSwgImNhcmhlaWdodCI6IDUyLCAiY3VyYndlaWdodCI6IDMwNTMsICJlbmdpbmV0eXBlIjogIm9oYyIsICJjeWxpbmRlcm51bWJlciI6ICJmaXZlIiwgImVuZ2luZXNpemUiOiAxMzEsICJmdWVsc3lzdGVtIjogIm1wZmkiLCAiYm9yZXJhdGlvIjogMy4xMywgInN0cm9rZSI6IDMuNCwgImNvbXByZXNzaW9ucmF0aW8iOiA3LCAiaG9yc2Vwb3dlciI6IDE2MCwgInBlYWtycG0iOiA1NTAwLCAiY2l0eW1wZyI6IDE2LCAiaGlnaHdheW1wZyI6IDIyLCAicHJpY2UiOiAxNzg1OS4xN319"
    
                        ,
                        "approximateArrivalTimestamp": 1690286668.54
                    },
                    "eventSource": "aws:kinesis",
                    "eventVersion": "1.0",
                    "eventID": "shardId-000000000000:49642967535840470808541827224503229287713030842930429954",
                    "eventName": "aws:kinesis:record",
                    "invokeIdentityArn": "arn:aws:iam::406468071577:role/lambda-kinesis-role",
                    "awsRegion": "eu-central-1",
                    "eventSourceARN": "arn:aws:kinesis:eu-central-1:406468071577:stream/car_events"
                    }
                ]
                }


url = 'http://localhost:8080/2015-03-31/functions/function/invocations'

# Convert the sample event to JSON format for comparison.
# However the post request get the sample_event
json_data = json.dumps(sample_event)
print("json_data:", json_data)

# Get the response
response = requests.post(url, json=sample_event, timeout=5)
print("Response status code:", response.status_code)
print("Response headers:", response.headers)
print("Response content:", response.content)
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