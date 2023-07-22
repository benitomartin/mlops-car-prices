## predict.py file

import joblib
import pandas as pd
from flask import Flask, request, jsonify


# Replace 'GradientBoostingRegressor_best_model.joblib' with the actual path to your saved model file
model = joblib.load('GradientBoostingRegressor_best_model.joblib')

import logging
logging.getLogger().setLevel(logging.INFO)

def clean_data(data_path: str) -> pd.DataFrame:
    # Read the CSV file into a DataFrame
    df = pd.read_csv('/app/data/test_sample.csv')
    
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
    data_path = request.json.get('data_path')

    # Clean the CSV data and prepare the feature DataFrame
    df = clean_data(data_path)
    X_test = split_dataframe(df)

    # Make predictions using the model
    y_pred = predict(X_test)

    # Create a response dictionary containing the predictions
    prediction = {
        "prediction": y_pred.tolist()  # Convert NumPy array to a list for JSON serialization
    }

    logging.info("Response: %s", prediction)

    # Return the response as JSON
    return jsonify(prediction)

if __name__ == "__main__":
    # Start the Flask app on the specified host and port
    app.run(debug=True, host='0.0.0.0', port=9696)
