## lambda_function.py

import os
import logging
import json
import mlflow.pyfunc
import pandas as pd
import boto3
from dotenv import load_dotenv


# Load environmental variables from '.env' file
load_dotenv()

# Debbuging Options:
logging.basicConfig(level=logging.INFO)
# logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

## Use this one to show the 
# def log_print(message):
#     logging.info(message)
#     print(message)


# Path to the model
BUCKET_NAME="mlflow-tracking-remote"
RUN_ID="aa806b4bc4044777a0a25d5b8a24d7d5"
EXPERIMENT_ID=29

S3_MODEL_PATH = f's3://{BUCKET_NAME}/{EXPERIMENT_ID}/{RUN_ID}/artifacts/models_mlflow'

# # Load model as a PyFuncModel.
# model = mlflow.pyfunc.load_model(S3_MODEL_PATH)
try:
    logging.info("Attempting to load the MLflow model...")
    model = mlflow.pyfunc.load_model(S3_MODEL_PATH)
    logging.info("MLflow model loaded successfully.")
except Exception as e:
    logging.error("Error loading the MLflow model:", exc_info=True)
    raise


kinesis_client = boto3.client('kinesis')


PREDICTIONS_STREAM_NAME =  os.getenv("PREDICTIONS_STREAM_NAME", "car_events")
TEST_RUN = os.getenv('TEST_RUN', 'False') == 'True'


def clean_data(data_df: pd.DataFrame) -> pd.DataFrame:
    # Drop unnecessary columns 'car_ID' and 'CarName'
    data_df.drop(columns=['car_ID', 'CarName'], inplace=True)
    
    # Map 'cylindernumber' values to numeric format
    data_df["cylindernumber"] = data_df["cylindernumber"].map({
                                                "four": 4, "six": 6, "five": 5, "eight": 8,
                                                "two": 2, "twelve": 12, "three": 3
                                            })
    
    # Drop duplicate rows
    data_df = data_df.drop_duplicates()
    
    # Return the cleaned DataFrame
    return data_df

def split_dataframe(data_df: pd.DataFrame) -> pd.DataFrame:
    # Separate the feature data (X) from the target variable data (y)
    X_test = data_df.drop(columns=["price"])  # DataFrame containing feature columns (all columns except 'price')

    return X_test 


def predict(X_test: pd.DataFrame) -> pd.DataFrame:
    # Make predictions using the pre-trained model
    y_pred = model.predict(X_test)

    # Convert the NumPy array to a Python list
    y_pred_list = y_pred.tolist()

    # Print the predictions (you may comment out or remove this line in production)

    return y_pred_list


def lambda_handler(event, context):
    logging.info("Received Lambda event: {}".format(json.dumps(event)))

    prediction_events = []

    ## This is the Record
    # print(json.dumps(event))
    
    try:
        for record in event["Records"]:

            car_data = record["kinesis"]["data"]

            real_price = car_data['price']
                
            
            # # # Assuming you receive the data as a JSON dictionary in the event
            data_df = pd.DataFrame(car_data, index=[0])
            
            
            # Clean the data
            cleaned_data = clean_data(data_df)
            
            # Split the Dataframe
            X_test = split_dataframe(cleaned_data)

            # Make predictions (Replace predict with actual model prediction)
            predictions = predict(X_test)
            
            
            prediction_event = {
                             'Model Version': "1",
                             'Prediction': round(predictions[0],2 ),
                             'Real Price': real_price
                         }
            
            logging.info("Generated Prediction Event: {}".format(json.dumps(prediction_event)))


            
            if not TEST_RUN:
                kinesis_client.put_record(StreamName=PREDICTIONS_STREAM_NAME,
                                        Data=json.dumps(prediction_event),
                                        PartitionKey=str(real_price)
                                        )
                                        
                prediction_events.append(prediction_event)
            
        # Log the prediction events before returning the response


        return {
             'Prediction Events': prediction_events,
      
         }
        
                
    except Exception as err:
        # Handle any exceptions that might occur during the prediction process
        error_msg = str(err)
        logging.error("Error occurred during prediction: {}".format(error_msg))

        return {
            'statusCode': 500,
            'body': json.dumps({'error': error_msg})
        }
