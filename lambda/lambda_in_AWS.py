import json
# import mlflow.pyfunc
import pandas as pd
import os
import boto3

# # Path to the model
# logged_model = f's3://{BUCKET_NAME}/{EXPERIMENT_ID}/{RUN_ID}/artifacts/models_mlflow'

#logged_model = f's3://mlflow-tracking-remote/aa806b4bc4044777a0a25d5b8a24d7d5/29/artifacts/models_mlflow'

# Load model as a PyFuncModel.
#model = mlflow.pyfunc.load_model(logged_model)

kinesis_client = boto3.client('kinesis')

PREDICTIONS_STREAM_NAME =  os.getenv("PREDICTIONS_STREAM_NAME", "car_events")


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
    # Replace this function with your actual model prediction logic
    # For demonstration purposes, let's assume the model returns constant values
    # predictions = pd.DataFrame(predictions, columns=["predicted_price"])
    
    return 10
    

def lambda_handler(event, context):

    prediction_events = []

    ## This is the Record
    # print(json.dumps(event))
    
    try:
        for record in event["Records"]:

            car_data = record["kinesis"]["data"]

            real_price = car_data['price']
            # print(real_price)
            
            
            # # # Assuming you receive the data as a JSON dictionary in the event
            data_df = pd.DataFrame(car_data, index=[0])
            
            
            # Clean the data
            cleaned_data = clean_data(data_df)
            
            # Split the Dataframe
            X_test = split_dataframe(cleaned_data)

            # Make predictions (Replace predict with actual model prediction)
            predictions = predict(X_test)
            
            
            prediction_event = {
                             'Model': "model",
                             "Version": "model version",
                             'prediction': predictions,
                             'real_price': real_price
                         }
            
            # # Convert the result DataFrame to JSON
            # result_json = predictions.to_json(orient='records')
            
            kinesis_client.put_record(StreamName=PREDICTIONS_STREAM_NAME,
                                      Data=json.dumps(prediction_event),
                                      PartitionKey=str(real_price)
                                      )
                                      
            prediction_events.append(prediction_event)
            

        return {
             'statusCode': 200,
             'prediction': prediction_events,
         }

        # return {
        #     'statusCode': 200,
        #     'body': result_json,
        #     'car_event': car_event
        # }
        
    except Exception as e:
        # Handle any exceptions that might occur during the prediction process
        error_msg = str(e)
        return {
            'statusCode': 500,
            'body': json.dumps({'error': error_msg})
        }