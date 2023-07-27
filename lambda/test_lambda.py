from lambda_function import lambda_handler

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

# Call the lambda_handler function with the sample event
result = lambda_handler(sample_event, None)

# Print the result (this will include the predictions printed from the function)
print(result)
