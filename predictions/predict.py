## predict.py file
import os
import mlflow
import pandas as pd
from flask import Flask, request, jsonify
from dotenv import load_dotenv
import boto3

# Load environmental variables
load_dotenv()

# # Get the RUN_ID after running orchestrate_s3.py and save it in .env
RUN_ID = os.getenv("RUN_ID")
BUCKET_NAME = os.getenv("BUCKET_NAME")
EXPERIMENT_ID = os.getenv("EXPERIMENT_ID")
# AWS_ACCESS_KEY_ID=os.getenv("AWS_ACCESS_KEY_ID")
# AWS_SECRET_ACCESS_KEY=os.getenv("AWS_SECRET_ACCESS_KEY")

# session = boto3.Session(
#                         aws_access_key_id=AWS_ACCESS_KEY_ID,
#                         aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
#                         )

# s3 = session.resource('s3')

# # Path to the model
logged_model = f's3://{BUCKET_NAME}/{EXPERIMENT_ID}/{RUN_ID}/artifacts/models_mlflow'


# Load model as a PyFuncModel.
model = mlflow.pyfunc.load_model(logged_model)

# Get the data
BASE_DIR = os.getenv("BASE_DIR")
TEST_DATA_PATH = os.getenv("TEST_DATA_PATH")

data_path = os.path.normpath(os.path.join(BASE_DIR, TEST_DATA_PATH))


def clean_data(data_path: str) -> pd.DataFrame:
    # Read the CSV file into a DataFrame
    df = pd.read_csv(data_path)
    
    # Drop unnecessary columns 'car_ID' and 'CarName'
    df.drop(columns=['car_ID', 'CarName'], inplace=True)
    
    # Map 'cylindernumber' values to numeric format
    df["cylindernumber"] = df["cylindernumber"].map({
                                                "four": 4, "six": 6, "five": 5, "eight": 8,
                                                "two": 2, "twelve": 12, "three": 3
                                            })
    
    # Drop duplicate rows
    df = df.drop_duplicates()
    
    # Return the cleaned DataFrame
    return df

def split_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    # Separate the feature data (X) from the target variable data (y)
    X_test = df.drop(columns=["price"])  # DataFrame containing feature columns (all columns except 'price')

    return X_test 

def predict(X_test: pd.DataFrame) -> pd.DataFrame:
    # Make predictions using the pre-trained model
    y_pred = model.predict(X_test)

    # Print the predictions (you may comment out or remove this line in production)
    print(f"{y_pred}")

    return y_pred

app = Flask('price-prediction')

@app.route('/predict', methods=['POST'])
def predict_price():
    # Get the data_path from the JSON payload in the request
    data_path = request.json['data_path']

    # Clean the CSV data and prepare the feature DataFrame
    df = clean_data(data_path)
    X_test = split_dataframe(df)

    # Make predictions using the model
    y_pred = predict(X_test)

    # Create a response dictionary containing the predictions
    prediction = {
        "prediction": y_pred.tolist()  # Convert NumPy array to a list for JSON serialization
    }

    # Return the response as JSON
    return jsonify(prediction)

if __name__ == "__main__":
    # Start the Flask app on the specified host and port
    app.run(debug=True, host='0.0.0.0', port=9696)
