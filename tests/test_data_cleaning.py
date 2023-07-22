import os
import pytest
import pandas as pd
from dotenv import load_dotenv

# Load environmental variables
load_dotenv()

# The file path of the CSV data you want to use for prediction
TEST_PATH = os.path.join(os.getenv('BASE_DIR'), os.getenv('DATA_PATH'))


def clean_data(TEST_PATH: str) -> pd.DataFrame:
    """
    Clean the data in the given CSV file.

    Parameters:
        TEST_PATH (str): File path of the CSV data to be cleaned.

    Returns:
        pd.DataFrame: The cleaned DataFrame.
    """
    
    # Read the CSV file into a DataFrame
    df = pd.read_csv(TEST_PATH)
    
    # Drop unnecessary columns 'car_ID' and 'CarName'
    df.drop(columns=['car_ID', 'CarName'], inplace=True)
    
    # Map 'cylindernumber' values to numeric format
    df["cylindernumber"] = df["cylindernumber"].map({"four": 4, "six": 6, "eight": 8,
                                                     "two": 2, "twelve": 12, "three": 3})
    
    # Drop duplicate rows
    df = df.drop_duplicates()
    df = df.dropna()
    
    # Return the cleaned DataFrame
    return df

@pytest.mark.parametrize("TEST_PATH", [TEST_PATH])
def test_clean_data_column_names(TEST_PATH):
    """
    Test function to check if the cleaned DataFrame has the correct column names.

    Parameters:
        TEST_PATH (str): File path of the CSV data used for testing.

    Raises:
        AssertionError: If the cleaned DataFrame does not have the expected column names.
    """

    # Call the clean_data function
    cleaned_df = clean_data(TEST_PATH)

    # Expected column names after cleaning
    expected_column_names = ['symboling', 'wheelbase', 'carlength', 'carwidth', 'carheight',
                            'curbweight', 'cylindernumber', 'enginesize', 'boreratio', 'stroke',
                            'compressionratio', 'horsepower', 'peakrpm', 'citympg', 'highwaympg',
                            'price', "fueltype", "aspiration", "doornumber", "carbody", "drivewheel", 
                            "enginelocation", "enginetype", "fuelsystem"]

    # Check the column names in the cleaned DataFrame
    assert set(cleaned_df.columns.tolist()) == set(expected_column_names)

    # Check if the "cylindernumber" column is numeric
    assert pd.api.types.is_numeric_dtype(cleaned_df['cylindernumber'])

    # Print a message indicating the test passed successfully
    print("Data cleaning and column check test passed!")

if __name__ == "__main__":
    # Run the test when executing this script directly
    pytest.main([__file__])
