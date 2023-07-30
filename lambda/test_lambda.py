from lambda_function import lambda_handler

# Create a sample event JSON object
# pylint: disable=R0801
# Similar lines of code in this file with test_docker.py
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

# Call the lambda_handler function with the sample event
result = lambda_handler(sample_event, None)

# Print the result (this will include the predictions printed from the function)
print(result)


## Unencoded Sample Event
# sample_event = {
#     "Records": [
#         {
#             "kinesis": {
#                 "data": {
#                     "car_ID": 10,
#                     "symboling": 0,
#                     "CarName": "audi 5000s (diesel)",
#                     "fueltype": "gas",
#                     "aspiration": "std",
#                     "doornumber": "two",
#                     "carbody": "hatchback",
#                     "drivewheel": "4wd",
#                     "enginelocation": "front",
#                     "wheelbase": 99.5,
#                     "carlength": 178.2,
#                     "carwidth": 67.9,
#                     "carheight": 52,
#                     "curbweight": 3053,
#                     "enginetype": "ohc",
#                     "cylindernumber": "five",
#                     "enginesize": 131,
#                     "fuelsystem": "mpfi",
#                     "boreratio": 3.13,
#                     "stroke": 3.4,
#                     "compressionratio": 7,
#                     "horsepower": 160,
#                     "peakrpm": 5500,
#                     "citympg": 16,
#                     "highwaympg": 22,
#                     "price": 17859.17
#                 }
#             }
#         }
#     ]
# }
