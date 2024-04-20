# MLOps Project Car Prices Prediction

<p>
    <img src="/integration_tests/results_printouts/Money-car.jpg"/>
    </p>

This project has been developed as part of the [MLOps Zoomcamp](https://github.com/DataTalksClub/mlops-zoomcamp) course provided by [DataTalks.Club](https://datatalks.club/).

The dataset used has been downloaded from [Kaggle](https://www.kaggle.com/datasets/hellbuoy/car-price-prediction) and a preliminary data analysis was performed (see [notebooks](/notebooks) folder), to get some insights for the further project development.

Below you can find some instructions to understand the project content. Feel free to ⭐ and clone this repo 😉

## Tech Stack

![Visual Studio Code](https://img.shields.io/badge/Visual%20Studio%20Code-0078d7.svg?style=for-the-badge&logo=visual-studio-code&logoColor=white)
![Jupyter Notebook](https://img.shields.io/badge/jupyter-%23FA0F00.svg?style=for-the-badge&logo=jupyter&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white)
![Matplotlib](https://img.shields.io/badge/Matplotlib-%23d9ead3.svg?style=for-the-badge&logo=Matplotlib&logoColor=black)
![scikit-learn](https://img.shields.io/badge/scikit--learn-%23F7931E.svg?style=for-the-badge&logo=scikit-learn&logoColor=white)
![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)
![MLflow](https://img.shields.io/badge/MLflow-0194E2.svg?style=for-the-badge&logo=MLflow&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
![Anaconda](https://img.shields.io/badge/Anaconda-%2344A833.svg?style=for-the-badge&logo=anaconda&logoColor=white)
![Linux](https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=white)
![AWS](https://img.shields.io/badge/AWS-%23FF9900.svg?style=for-the-badge&logo=amazon-aws&logoColor=white)
![Grafana](https://img.shields.io/badge/grafana-%23F46800.svg?style=for-the-badge&logo=grafana&logoColor=white)
![Git](https://img.shields.io/badge/git-%23F05033.svg?style=for-the-badge&logo=git&logoColor=white)

## Project Structure

The project has been structured with the following folders and files:

- `.github:` contains the CI/CD files (GitHub Actions)
- `data:` dataset and test sample for testing the model
- `integration_tests:` prediction integration test with docker-compose
- `lambda:` test of the lambda handler with and w/o docker
- `model:` full pipeline from preprocessing to prediction and monitoring using MLflow, Prefect, Grafana, Adminer, and docker-compose
- `notebooks:` EDA and Modeling performed at the beginning of the project to establish a baseline
- `tests:` unit tests
- `terraform:` IaC stream-based pipeline infrastructure in AWS using Terraform
- `Makefile:` set of execution tasks
- `pyproject.toml:` linting and formatting
- `setup.py:` project installation module
- `requirements.txt:` project requirements

## Project Description

The dataset was obtained from Kaggle and contains various columns with car details and prices. To prepare the data for modeling, an **Exploratory Data Analysis** was conducted to preprocess numerical and categorical features, and suitable scalers and encoders were chosen for the preprocessing pipeline. Subsequently, a **GridSearch** was performed to select the best regression models, with RandomForestRegressor and GradientBoostingRegressor being the top performers, achieving an R2 value of approximately 0.9.

<p align="center">
    <img src="/integration_tests/results_printouts/notebook.png"/>
    </p>
<p>
    <img src="/model/results_printouts/grafana_dashboard.png"/>
    </p>

Afterward, the models underwent testing, model registry, and deployment using **MLflow**, **Prefect**, and **Flask**. Monitoring of the models was established through **Grafana** and **Adminer** Database. Subsequently, a project infrastructure was set up in **Terraform**, utilizing **AWS** modules such as Kinesis Streams (Producer & Consumer), Lambda (Serving API), S3 Bucket (Model artifacts), and ECR (Image Registry).

<p>
    <img src="/model/results_printouts/Deployment Prefect UI.png"/>
    </p>
    <p>
    <img src="/terraform/results_printouts/manual_deploy_cloudwatch.png"/>
</p>

Finally, to streamline the development process, a fully automated **CI/CD** pipeline was created using GitHub Actions.

<p>
    <img src="/integration_tests/results_printouts/CICD.png"/>
    </p>
    
## Project Set Up

The Python version used for this project is Python 3.9.

1. Clone the repo (or download it as a zip file):

   ```bash
   git clone https://github.com/benitomartin/mlops-car-prices.git
   ```

2. Create the virtual environment named `main-env` using Conda with Python version 3.9:

   ```bash
   conda create -n main-env python=3.9
   conda activate main-env
   ```

3. Install `setuptools` and `wheel`:

    ```bash
    conda install setuptools wheel

4. Execute the `setup.py` script and install the project dependencies included in the requirements.txt:

    ```bash
    pip install .

    or
 
    make install
    ```

Each project folder contains a **README.md** file with instructions about how to run the code. I highly recommend creating a virtual environment for each one. Additionally, please note that an **AWS Account**, credentials, and proper policies with full access to EC2, S3, ECR, Lambda, and Kinesis are necessary for the projects to function correctly. Make sure to configure the appropriate credentials to interact with AWS services.


## Project Best Practices

The following best practices were implemented:

- :white_check_mark: **Problem description**: The project is well described and it's clear and understandable
- :white_check_mark: **Cloud**: The project is developed on the cloud and IaC tools are used for provisioning the infrastructure
- :white_check_mark: **Experiment tracking and model registry**: Both experiment tracking and model registry are used
- :white_check_mark: **Workflow orchestration**: Fully deployed workflow
- :white_check_mark: **Model deployment**: The model deployment code is containerized and can be deployed to the cloud
- :white_check_mark: **Model monitoring**: Basic model monitoring that calculates and reports metrics
- :white_check_mark: **Reproducibility**: Instructions are clear, it's easy to run the code, and it works. The versions for all the dependencies are specified.
- :white_check_mark:**Best practices**:
    * [X] There are unit tests
    * [X] There is an integration test
    * [X] Linter and code formatting are used
    * [X] There is a Makefile
    * [X] There is a CI/CD pipeline
