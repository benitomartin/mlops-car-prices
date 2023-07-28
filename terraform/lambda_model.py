## lambda_model.py

import os
import json
import mlflow.pyfunc
import pandas as pd
import boto3
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


    def lambda_handler(self, event):
        """
        Lambda function to make predictions based on incoming Kinesis records.

        Parameters:
            event (dict): The Lambda event containing Kinesis records.

        Returns:
            dict: The prediction results.
        """

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


class KinesisCallback:
    """
    Class representing a callback for putting prediction events into a Kinesis stream.
    """

    def __init__(self, kinesis_client, prediction_stream_name):
        self.kinesis_client = kinesis_client
        self.prediction_stream_name = prediction_stream_name

    def put_record(self, prediction_event):
        real_price = prediction_event['real_price']

        self.kinesis_client.put_record(
            StreamName=self.prediction_stream_name,
            Data=json.dumps(prediction_event),
            PartitionKey=str(real_price),
        )


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

    callbacks = []

    if not test_run:
        kinesis_client = create_kinesis_client()
        kinesis_callback = KinesisCallback(kinesis_client, prediction_stream_name)
        callbacks.append(kinesis_callback.put_record)

    model_service = ModelService(model=model, model_version=run_id, callbacks=callbacks)

    return model_service