## train.py

import os
import warnings
from pathlib import Path
from dotenv import load_dotenv
import joblib

import pandas as pd
from preprocess import clean_data, split_dataframe, preprocess
from create_db import prep_db

from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import make_pipeline
from sklearn.linear_model import Ridge, ElasticNet
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor, AdaBoostRegressor, GradientBoostingRegressor
from sklearn.metrics import r2_score, mean_squared_error
from sklearn.exceptions import FitFailedWarning

import mlflow
from prefect import flow, task
from prefect_aws import S3Bucket
from prefect.artifacts import create_markdown_artifact

# Load environmental variables
load_dotenv()


@task
def train_model(X_train: pd.DataFrame,
                X_test: pd.DataFrame,
                y_train: pd.Series,
                y_test: pd.Series,
                preprocessor: ColumnTransformer,
                data_directory_path:str,
                random_seed:int,
                test_size:float) -> pd.DataFrame:
    


    # Start a new MLflow run
    with mlflow.start_run():
        # Get the RUN ID and EXPERIMENT ID of the active run
        run_id = mlflow.active_run().info.run_id
        experiment_id = mlflow.active_run().info.experiment_id


        models_names = ["Ridge",
                        "ElasticNet",
                        "DecisionTreeRegressor",
                        "RandomForestRegressor",
                        "AdaBoostRegressor",
                        "GradientBoostingRegressor"
                       ]


        # Define the list of regression models to be evaluated
        models = [Ridge(),
                  ElasticNet(),
                  DecisionTreeRegressor(),
                  RandomForestRegressor(),
                  AdaBoostRegressor(),
                  GradientBoostingRegressor()
                 ]

        # Define the hyperparameter grid for each model
        param_grid = {

            'Ridge': {'ridge__alpha': [0.1, 1.0, 10.0]},


            'ElasticNet': {'elasticnet__alpha': [0.1, 1.0, 10.0], 
                           'elasticnet__l1_ratio': [0.2, 0.5, 0.8], 
                           'elasticnet__max_iter': [10000, 2000]},

            'DecisionTreeRegressor': {'decisiontreeregressor__max_depth': [None, 5, 10]},

            'RandomForestRegressor': {'randomforestregressor__n_estimators': [50, 100, 200], 
                                      'randomforestregressor__max_depth': [None, 5, 10]},

            'AdaBoostRegressor': {'adaboostregressor__n_estimators': [50, 100, 200], 
                                  'adaboostregressor__learning_rate': [0.01, 0.1, 1.0]},

            'GradientBoostingRegressor': {'gradientboostingregressor__n_estimators': [50, 100, 200], 
                                          'gradientboostingregressor__learning_rate': [0.01, 0.1, 1.0], 
                                          'gradientboostingregressor__max_depth': [3, 5, 7]}
        }

        
        best_models = {}         # Dictionary to store the best models for each model type
        evaluation_results = []  # List to store the evaluation results for each model


        # Perform grid search for each model
        for model_name, model in zip(models_names, models):


            # Create a pipeline with the preprocessor and the current model
            model_pipeline = make_pipeline(preprocessor, model)

            # Create a GridSearchCV object for hyperparameter tuning
            grid_search = GridSearchCV(model_pipeline, param_grid[model_name], cv=5, n_jobs=-1, error_score='raise')

            # Perform grid search on the training data
            try:
                
                # Perform grid search on the training data
                grid_search.fit(X_train, y_train)

            except ValueError as exception:
                warnings.warn(f"Model '{model_name}' fit failed. Exception message: {str(exception)}", FitFailedWarning)
                continue
            except Exception as exception:
                warnings.warn(f"Model '{model_name}' fit failed due to an unexpected error. Exception message: {str(exception)}")
                continue

            # Store the best model obtained from the grid search
            best_models[model_name] = grid_search.best_estimator_

            # Evaluate the best model on the test data
            model = best_models[model_name]
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)
            test_score = r2_score(y_test, y_pred)
            mse = mean_squared_error(y_test, y_pred)


            # Append the evaluation results to the list
            evaluation_results.append({'Model Name': model_name, 'R_2': test_score, 'MSE': mse})
            print(f"Evaluation results for {model_name}:")
            print(evaluation_results[-1])  # Print the last added element in the results list


 
        # Convert the evaluation results list to a DataFrame
        results_df = pd.DataFrame(evaluation_results)


         # Sort the DataFrame based on the "R_2" score in descending order
        sorted_results = results_df.sort_values(by='R_2', ascending=False)

        # Get the name of the best model (first row in the sorted DataFrame)
        best_model_name = sorted_results.iloc[0]['Model Name']

        # Get the best model itself from the best_models dictionary
        best_model = best_models[best_model_name]

                # Save the best model to a file using joblib.dump() locally
        models_folder = "trained_models"     
        model_filename = f"{best_model_name}_best_model.joblib"
        model_path = os.path.join(models_folder, model_filename)

        joblib.dump(best_model, model_path)

        # joblib.dump(best_model, model_filename)


        # Evaluate the best model on the test data again (for logging)
        best_model.fit(X_train, y_train)
        y_pred = best_model.predict(X_test)
        test_score = r2_score(y_test, y_pred)
        mse = mean_squared_error(y_test, y_pred)

        # Log R2 and MSE for the best model
        mlflow.log_metric("Best Model R2", test_score)
        mlflow.log_metric("Best Model MSE", mse)


        # Set a tag to identify the developer
        DEVELOPER = os.getenv('DEVELOPER')
        mlflow.set_tag("developer", DEVELOPER)

        # Log params and evaluation results to MLflow
        mlflow.log_param("data-path", data_directory_path)
        mlflow.log_param("random_seed", random_seed)
        mlflow.log_param("test_size", test_size)
        mlflow.log_metric("R2", test_score)
        mlflow.log_metric("MSE", mse)
        
        # Log the local model 
        # mlflow.log_artifact(model_filename)
        mlflow.log_artifact(model_path)

        # # Log model and artifact
        artifact_path = "models_mlflow"
        artifact_uri = mlflow.get_artifact_uri()

   
        mlflow.sklearn.log_model(sk_model=best_model,
                                 artifact_path=artifact_path,
                                 registered_model_name="regression-model"
                                 )



        # Save a report as an artifact in Prefect UI
        markdown__r2_report = f"""# RMSE Report

                ## METRICS BEST MODEL

                |--> f"{best_model_name} R_2: {test_score:.2f}" 
                |--> f"{best_model_name} MSE: {mse:.2f}"            

                """

        create_markdown_artifact(
            key="best-metrics-report", markdown=markdown__r2_report
        )
        

        # Print R2 Report
        print(markdown__r2_report)

        # Print Results
        print("Results DataFrame:")
        print(sorted_results)

        # Print experiment data
        print(f"Model filename: {model_filename}")
        print(f"Artifact path: {artifact_path}")
        print("Artifact uri: {}".format(artifact_uri))
        print(f"RUN_ID: {run_id}")
        print(f"EXPERIMENT_ID: {experiment_id}")


    return sorted_results



@flow()
def main_flow() -> None:
    """The main training pipeline"""

    # Enter experiment name
    experiment_name = input("Enter experiment name: ")

    
    # Select a tracking URI
    AWS_URI = os.getenv('AWS_URI')
    mlflow.set_tracking_uri(AWS_URI)

    # Set experiment name
    mlflow.set_experiment(f"{experiment_name}")


    # ## Load and save data in AWS Bucket
    # BUCKET_NAME = os.getenv("BUCKET_NAME")
    # s3_bucket_block = S3Bucket.load(BUCKET_NAME)
    # s3_bucket_block.download_folder_to_path(from_folder="data", to_folder="data")
    
    BASE_DIR = os.getenv('BASE_DIR')
    DATA_PATH = os.getenv('DATA_PATH') 
    data_directory_path = Path(BASE_DIR) / DATA_PATH

 
    # Call the clean_data task
    cleaned_data = clean_data(data_directory_path)

    # Call the split_dataframe task
    X_data, y_data = split_dataframe(cleaned_data)

    # Call the preprocess task
    preprocessor = preprocess(X_data)

    # Split variables
    random_seed = 42
    test_size = 0.2

    X_train, X_test, y_train, y_test = train_test_split(X_data, y_data, test_size=test_size, random_state=random_seed)

    # train_model(X_train, X_test, y_train, y_test, preprocessor, data_directory_path, random_seed, test_size)


    # Call the train_model task

    sorted_results = train_model(X_train, X_test, y_train, y_test, preprocessor, data_directory_path, random_seed, test_size)

    create_table_query = """
        CREATE TABLE IF NOT EXISTS evaluation_results (
                "Model Name" VARCHAR,
                "R_2" FLOAT,
                "MSE" FLOAT
                )
                """
    prep_db(create_table_query, sorted_results)

if __name__ == "__main__":
    try:
        main_flow()
    except Exception as err:
        print(f"An error occurred: {err}")
