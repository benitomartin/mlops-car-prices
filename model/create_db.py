## create_db.py

import os
import pandas as pd
from prefect import task
from sqlalchemy import create_engine, text
import psycopg
from dotenv import load_dotenv

# Load environmental variables
load_dotenv()


create_table_query = """
        CREATE TABLE IF NOT EXISTS evaluation_results (
                "Model Name" VARCHAR,
                "R_2" FLOAT,
                "MSE" FLOAT
                )
                """

@task
def prep_db(sql_query: str, sorted_results: pd.DataFrame) -> None:
    """
    Create a database and table if they don't exist, and write the data from sorted_results DataFrame into the table.

    Args:
    create_table_query (str): SQL query string to create the 'evaluation_results' table.
    sorted_results (pd.DataFrame): DataFrame containing the sorted evaluation results.

    Returns:
    None
    """

    # First, connect to the default database (postgres) to check if 'cars' database exists
    POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
    POSTGRES_DB = os.getenv('POSTGRES_DB')
    
    # Create DB
    with psycopg.connect(f"host=localhost port=5432 user=postgres password={POSTGRES_PASSWORD}", autocommit=True) as conn:

        res = conn.execute(f"SELECT 1 FROM pg_database WHERE datname='{POSTGRES_DB}'")
        
        if len(res.fetchall()) == 0:
            # Create the 'cars' database
            conn.execute(f"CREATE DATABASE {POSTGRES_DB};")


    # Remove unnecessary whitespace characters
    sql_query = text(sql_query.strip())

    # Now, connect to the 'cars' database to create the table and write sorted_results
    connection_uri = f"postgresql://postgres:{POSTGRES_PASSWORD}@localhost:5432/{POSTGRES_DB}"
    engine = create_engine(connection_uri)

    try:
        # Create the table
        with engine.connect() as conn:
            conn.execute(sql_query)

        # Write sorted_results DataFrame to the 'evaluation_results' table.
        # To replace the existing table: if_exists='replace'
        sorted_results.to_sql('evaluation_results', con=engine, if_exists='replace', index=False)
    finally:
        engine.dispose()


