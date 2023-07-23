## preprocess.py

import os
from pathlib import Path
import pandas as pd
from sklearn.preprocessing import RobustScaler, StandardScaler, MinMaxScaler, OneHotEncoder
from sklearn.compose import make_column_transformer, ColumnTransformer
from sklearn.pipeline import make_pipeline
from prefect import task
from dotenv import load_dotenv

# Load environmental variables
load_dotenv()

# Get Data
BASE_DIR = os.getenv('BASE_DIR')
DATA_PATH = os.getenv('DATA_PATH')
data_directory_path = Path(BASE_DIR) / DATA_PATH


@task
def clean_data(data_directory_path: str) -> pd.DataFrame:
    """
    Read the CSV file into a DataFrame and perform data cleaning operations.

    Returns:
    pd.DataFrame: The cleaned DataFrame.
    """

    # Read the CSV file into a DataFrame
    df = pd.read_csv(data_directory_path)
    
    #Drop unnecessary columns 'car_ID' and 'CarName'
    df.drop(columns = ['car_ID', 'CarName'], inplace = True)
    
    # Map 'cylindernumber' values to numeric format
    df["cylindernumber"] = df["cylindernumber"].map({"four":4, "six":6, "eight":8,
                                                     "two":2, "twelve":12, "three":3})
    # Drop duplicate rows
    df = df.drop_duplicates()
    df = df.dropna()
    
    # Return the cleaned DataFrame
    return df


@task
def split_dataframe(df: pd.DataFrame) -> tuple:
    """
    Split the DataFrame into feature data (X) and target variable data (y).

    Args:
    df (pd.DataFrame): The DataFrame containing the data.

    Returns:
    tuple: A tuple containing the feature data (X) and target variable data (y).
    """

    # Separate the feature data (X) from the target variable data (y)
    X = df.drop(columns=["price"])   
    y = df["price"]                  

    # Return the feature data (X) and target variable data (y)
    return X, y


@task
def preprocess(X: pd.DataFrame) -> pd.DataFrame:
    """
    Preprocess the feature data (X) using various scaling techniques for numerical features and one-hot encoding for categorical features.

    Args:
    X (pd.DataFrame): The feature data DataFrame.

    Returns:
    pd.DataFrame: The preprocessor for further data transformation.
    """

    X_num = X.select_dtypes(exclude = ['object'])
    X_cat = X.select_dtypes(include=['object'])

    features_robust = ["wheelbase", "cylindernumber", "enginesize", "stroke", \
                       "compressionratio", "horsepower", "citympg"]

    features_standard = ["symboling", "carlength", "carwidth", "carheight",\
                              "curbweight", "boreratio", "highwaympg"]

    features_minmax = ["peakrpm"]
    

    scalers = ColumnTransformer([("robust_scaler", RobustScaler(), features_robust),
                                 ("standard_scaler", StandardScaler(), features_standard),
                                 ("minmax_scaler", MinMaxScaler(), features_minmax)
                                ],
                                 remainder='drop'
                            )
    

    # Define the numerical and categorical features
    num_features = X_num.columns
    cat_features  = X_cat.columns

    # Create the preprocessor for numerical features
    num_preprocessor = make_pipeline(scalers)

    # Create the preprocessor for categorical features
    cat_preprocessor = make_pipeline(OneHotEncoder(sparse_output=False, 
                                                  handle_unknown='ignore'))

                                


    # Create the preprocessor using `make_column_transformer`
    preprocessor = make_column_transformer(
                                            (num_preprocessor, num_features),
                                            (cat_preprocessor, cat_features),
                                        )
    
    return preprocessor