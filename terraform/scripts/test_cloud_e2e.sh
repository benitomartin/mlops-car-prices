#!/bin/bash

export KINESIS_STREAM_INPUT="stg_car_events-mlops-zoomcamp"
export KINESIS_STREAM_OUTPUT="stg_ride_predictions-mlops-zoomcamp"

SHARD_ID=$(aws kinesis put-record 
        --stream-name ${KINESIS_STREAM_INPUT}  
        --partition-key 1  --cli-binary-format raw-in-base64-out  
        --data '{
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
    }'  
        --query 'ShardId'
    )


    aws kinesis put-record \
    --stream-name "${KINESIS_STREAM_INPUT}" \
    --partition-key "1" \
    --data '{
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
    }'


#SHARD_ITERATOR=$(aws kinesis get-shard-iterator --shard-id ${SHARD_ID} --shard-iterator-type TRIM_HORIZON --stream-name ${KINESIS_STREAM_OUTPUT} --query 'ShardIterator')

#aws kinesis get-records --shard-iterator $SHARD_ITERATOR