# MLOps Project Car Prices Prediction

![car](https://github.com/benitomartin/templates/assets/116911431/d5d98b26-f096-42bf-b97d-d2fefdebe555)

This project is currently being developed as part [MLOps Zoomcamp](https://github.com/DataTalksClub/mlops-zoomcamp) course provided by [DataTalks](https://datatalks.club/).Club.

The dataset used has been downloaded from [Kaggle](https://www.kaggle.com/datasets/hellbuoy/car-price-prediction) and a preliminary data analysis was performed (see [notebooks](https://github.com/benitomartin/mlops-car-prices/tree/main/notebooks) folder), to get some insights for the further project development.

Below you can find some instructions to understand the project content. Feel free to clone this repo :wink:

## Tech Stack

![Visual Studio Code](https://img.shields.io/badge/Visual%20Studio%20Code-0078d7.svg?style=for-the-badge&logo=visual-studio-code&logoColor=white)
![Jupyter Notebook](https://img.shields.io/badge/jupyter-%23FA0F00.svg?style=for-the-badge&logo=jupyter&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white)
![Matplotlib](https://img.shields.io/badge/Matplotlib-%23d9ead3.svg?style=for-the-badge&logo=Matplotlib&logoColor=black)
![scikit-learn](https://img.shields.io/badge/scikit--learn-%23F7931E.svg?style=for-the-badge&logo=scikit-learn&logoColor=white)
![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)
![mlflow](https://img.shields.io/badge/mlflow-%23FF0000.svg?style=for-the-badge&logo=numpy&logoColor=blue)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
![Anaconda](https://img.shields.io/badge/Anaconda-%2344A833.svg?style=for-the-badge&logo=anaconda&logoColor=white)
![Linux](https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=white)
![AWS](https://img.shields.io/badge/AWS-%23FF9900.svg?style=for-the-badge&logo=amazon-aws&logoColor=white)
![Grafana](https://img.shields.io/badge/grafana-%23F46800.svg?style=for-the-badge&logo=grafana&logoColor=white)
![Git](https://img.shields.io/badge/git-%23F05033.svg?style=for-the-badge&logo=git&logoColor=white)

## Project Structure

The project has been structured with the following folders and files:

- `.github`: contains the CI/CD files (GitHub Actions)
- `data`: dataset and test sample for testing the model
- `integration_tests`: prediction integration test with docker compose
- `lamdba`: test of the lambda handler with and w/o docker
- `model`: full pipeline from preporcessing till prediction and monitoring using MLflow, Prefect, Grafana, Adminer and docker compose
- `notebooks`: EDA and Modeling performed at the beginning of the project to stablish a baseline
- `tests`: unit tests
- `terraform`: IaC stream-based pipeline infrastructure in AWS using Terraform
- `Makefile`: set of execution tasks
- `pyproject.toml`: linting and formatting
- `setup.py`: project installation module
- `requirements.txt`: project requirements

## Project Set Up

1. Clone the repo:

   ```bash
   git clone https://github.com/benitomartin/mlops-car-prices.git

2. Create the virtual environment named `main-env` using Conda with Python version 3.9:

   ```bash
   conda create -n main-env python=3.9
   conda activate main-env

3. Install `setuptools` and `wheel`:

    ```bash
    conda install setuptools wheel

4. Execute the `setup.py` script and install the project dependencies included in the requirements.txt:

    ```bash
    pip install .

    or
 
    make install

## Project Description

The dataset was downloaded from Kaggle and contains several columns with car details and prices. An Exploratory Data Analysis was performed in order to preprocess numerical and categorical features and select scalers and encoders for the preprocessing pipeline. The model is being selected after performing a GridSearch with several regrssion models. The best models reach an R2 of around 0.9, mainly RandomForestRegressor and GradientBoostingRegressor.

![notebook](https://github.com/benitomartin/mlops-car-prices/assets/116911431/cbaccce2-e3ed-4480-a715-3060d56465af)
![grafana_dashboard](https://github.com/benitomartin/mlops-car-prices/assets/116911431/6201ae65-383b-44bf-b30f-11ad2b75bf34)

The models have been tested and deployed initially using MLflow and Prefect and monitored in Grafana and Adminer Database. Later a project infrastructure has been set up in Terraform with modules in AWS like Kinesis Streams (Producer & Consumer), Lambda (Serving API), S3 Bucket (Model artifacts) and ECR (Image Registry)

![Deployment Prefect UI](https://github.com/benitomartin/mlops-car-prices/assets/116911431/63053687-7fe7-4eb1-876d-8416cccf5645)
![Artifacts Prefect UI](https://github.com/benitomartin/mlops-car-prices/assets/116911431/ec8a3fab-53c2-4a23-a41d-f5b8c4570f60)
