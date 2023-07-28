import os
import pandas as pd
import pytest
from sklearn.compose import ColumnTransformer, make_column_transformer
from sklearn.preprocessing import RobustScaler, StandardScaler, MinMaxScaler
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import OneHotEncoder
from dotenv import load_dotenv
from test_data_cleaning import clean_data


# Load environmental variables
load_dotenv()

# The file path of the CSV data you want to use for prediction
TEST_PATH = os.path.join(os.getenv('BASE_DIR'), os.getenv('DATA_PATH'))

# The clean data before preprocessing
df = clean_data(TEST_PATH)

@pytest.fixture
def test_data():
    """Fixture to provide the cleaned DataFrame as test data."""
    return clean_data(TEST_PATH)

def preprocess(X: pd.DataFrame) -> ColumnTransformer:
    """
    Preprocess the input DataFrame using a combination of scalers for numerical features
    and one-hot encoding for categorical features.

    Parameters:
        X (pd.DataFrame): Input DataFrame containing the data to be preprocessed.

    Returns:
        ColumnTransformer: A preprocessor object that applies the appropriate transformations
                           to numerical and categorical features.
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


def test_preprocess(test_data):
    """
    Test the preprocess function with the provided test data.

    Parameters:
        test_data (pd.DataFrame): The cleaned DataFrame obtained from the test_data fixture.
    """
        
    # Sample input DataFrame for testing
    X = test_data.drop(columns=["price"])


    # Call the preprocess function
    preprocessor = preprocess(X)

    # Assert that the returned preprocessor is not None
    assert preprocessor is not None

    # Assert that the preprocessor is an instance of ColumnTransformer
    assert isinstance(preprocessor, ColumnTransformer)

    # Print a message indicating the test passed successfully
    print("Data preprocessing check test passed!")


if __name__ == "__main__":
    # Run the test when executing this script directly
    pytest.main([__file__])