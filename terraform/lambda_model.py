## lambda_model.py

import os
import json
from typing import Dict, Any, Callable
import boto3
import mlflow.pyfunc
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

# pylint: disable=R0801
def get_model_location(run_id):
    """
    Get the model location from environment variables or construct it using default values.

    Parameters:
        run_id (str): The ID of the MLflow run.

    Returns:
        str: The model location.
    """
        
    model_location = os.getenv('MODEL_LOCATION')

    if model_location is not None:
        return model_location

    model_bucket = os.getenv('MODEL_BUCKET', 'mlflow-tracking-remote')
    experiment_id = os.getenv('MLFLOW_EXPERIMENT_ID', '29')

    model_location = f's3://{model_bucket}/{experiment_id}/{run_id}/artifacts/models_mlflow'

    return model_location


# pylint: disable=R0801
def load_model(run_id):
    model_path = get_model_location(run_id)
    model = mlflow.pyfunc.load_model(model_path)
    return model

# pylint: disable=R0801
class ModelService:
    """
    Class representing a model service that handles data cleaning, predictions, and callbacks.
    """

    def __init__(self, model, model_version=None, callbacks=None):
        """
        Initialize the ModelService.

        Parameters:
            model: The pre-trained model.
            model_version (str): The version of the model (optional).
            callbacks (list): List of callback functions (optional).
        """
        
        self.model = model
        self.model_version = model_version
        self.callbacks = callbacks or []

    def clean_data(self, data_df: pd.DataFrame) -> pd.DataFrame:
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

    def split_dataframe(self, data_df: pd.DataFrame) -> pd.DataFrame:
        # Separate the feature data (X) from the target variable data (y)
        X_test = data_df.drop(columns=["price"])  # DataFrame containing feature columns (all columns except 'price')

        return X_test 


    def predict(self, X_test: pd.DataFrame) -> pd.DataFrame:
        # Make predictions using the pre-trained model
        y_pred = self.model.predict(X_test)
        
        # Convert the NumPy array to a Python list
        y_pred_list = y_pred.tolist()

        return y_pred_list

    # pylint: disable=W0613
    def lambda_handler(self, event, context):
        """
        Lambda function to make predictions based on incoming Kinesis records.

        Parameters:
            event (dict): The Lambda event containing Kinesis records.

        Returns:
            dict: The prediction results.
        """
        print("Received Lambda event:", event)
        print("Received Lambda context:", context)

        prediction_events = []
      
        try:
            for record in event["Records"]:

                car_data = record["kinesis"]["data"]

                real_price = car_data['price']
                               
                data_df = pd.DataFrame(car_data, index=[0])
                
                
                # Clean the data
                cleaned_data = self.clean_data(data_df)
                
                # Split the Dataframe
                X_test = self.split_dataframe(cleaned_data)

                # Make predictions (Replace predict with actual model prediction)
                predictions = self.predict(X_test)
                
                
                prediction_event = {
                                'Model': "model",
                                "Version": self.model_version,
                                'prediction': predictions,
                                'real_price': real_price
                            }
                
                
                for callback in self.callbacks:
                    callback(prediction_event)
                                            
                prediction_events.append(prediction_event)
                

            return {
                'prediction': prediction_events,
            }
            
                    
        except Exception as e:
            # Handle any exceptions that might occur during the prediction process
            error_msg = str(e)
            return {
                'statusCode': 500,
                'body': json.dumps({'error': error_msg})
            }



def put_kinesis_record(kinesis_client, prediction_stream_name: str, prediction_event: Dict[str, Any]):
    """
    Put a prediction event into a Kinesis stream.

    Parameters:
        kinesis_client: The AWS Kinesis client.
        prediction_stream_name (str): The name of the Kinesis stream for predictions.
        prediction_event (dict): The prediction event to be put into the stream.
    """
    real_price = prediction_event['real_price']
    kinesis_client.put_record(
        StreamName=prediction_stream_name,
        Data=json.dumps(prediction_event),
        PartitionKey=str(real_price),
    )


def create_kinesis_callback(prediction_stream_name: str, test_run: bool) -> Callable:
    if not test_run:
        # If test_run is False, create a Kinesis client and return a callback function
        kinesis_client = create_kinesis_client()
        return lambda prediction_event: put_kinesis_record(kinesis_client, prediction_stream_name, prediction_event)
    # If test_run is True, return a dummy callback function that does nothing
    return lambda prediction_event: None


def create_kinesis_client():
    """
    Create an AWS Kinesis client.

    Returns:
        boto3.client: The Kinesis client.
    """

    endpoint_url = os.getenv('KINESIS_ENDPOINT_URL')

    if endpoint_url is None:
        return boto3.client('kinesis')

    return boto3.client('kinesis', endpoint_url=endpoint_url)


def init(prediction_stream_name: str, run_id: str, test_run: bool):
    """
    Initialize the model service.

    Parameters:
        prediction_stream_name (str): The name of the Kinesis stream for predictions.
        run_id (str): The ID of the MLflow run.
        test_run (bool): Whether it's a test run or not.

    Returns:
        ModelService: The initialized model service.
    """
        
    model = load_model(run_id)

    kinesis_callback = create_kinesis_callback(prediction_stream_name, test_run)
    callbacks = [kinesis_callback]

    model_service = ModelService(model=model, model_version=run_id, callbacks=callbacks)

    return model_service