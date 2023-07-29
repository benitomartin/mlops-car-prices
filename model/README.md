# Modeling

This folder contains all files and folders to train, deploy, monitor the model, and make predictions:

- `preprocess.py`: the functions to preprocess the data
- `prefect_s3_bucket_block.py`: the functions to create a block in prefect UI
- `create_db.py`: the functions to create the DB in Grafana and Adminer:
- `train.py`: the functions to train the model with AWS, Prefect and MLflow, and to monitor with Grafana and Adminer

  - **Adminer**: This service is based on the Adminer Docker image, which provides a web-based database management tool

  - **Grafana**: This service is based on the grafana/grafana Docker image, which sets up the Grafana monitoring and visualization platform

- `trained_models`: this folder contains the models trained after running `train.py`
- `config`: this folder contains the file `grafana_datasources.yaml` to access the data and `grafana_dashboards.yaml` to save dashboards
- `dashboards`: use this folder to save the dashboards created in Grafana
- `docker-compose.yml`: the Docker set-up for monitoring
- `predict.py`: the functions to run the Flask App
- `test.py`: the functions to predict using the selected model
- `results_printouts`: a folder with some print outs of the results

## Set Up

### AWS

- Create a EC2 Instance, a S3 Bucker and a RDS Instance. Follow this video for the set up [link](https://www.youtube.com/watch?v=1ykg4YmbFVA&list=PL3MmuxUbc_hIUISrluw_A7wDSmfOhErJK&index=16&t=1383s). The configuration data for the RDS will be later used to run MLflow

- Create a IAM user and access key. This must be saved in your local computer in the credentials file. This is normally located here C:\\Users\\username\\~.aws

- Add to the IAM user the following policy **AmazonS3FullAccess**

### Deployment

The model will be deployed in Prefect.

- `prefect_s3_bucket_block.py`: run this file to create a block in prefect UI (Make sure to run before `prefect server start`):

    ```bash
    python prefect_s3_bucket_block.py
    ```

- See the available blocks running this in the terminal:

    ```bash
    prefect block ls
    ```

- If you want to see the blocks available on the prefect server you can run:

    ```bash
    prefect block type ls
    ```

- Push the blocks to the server, so we can use them:

    ```bash
    prefect block register -m prefect_aws
    ```

- Initialilze your prefect project. This will create the following files: `.prefectignore`, `prefect.yaml`, `.prefect/`

    ```bash
    prefect project init
    ```

- Change the `prefect.yaml` and make sure it has this structure:

    ```bash
    name: model
    prefect-version: 2.10.21

    # build section allows you to manage and build docker images
    build:

    # push section allows you to manage if and how this project is uploaded to remote locations
    push:

    # pull section allows you to provide instructions for cloning this project in remote locations
    pull:
    - prefect.projects.steps.set_working_directory:
        directory: C:\Users\path\to\mlops-car-prices\model
    ```

- Create a Work Pool in Prefect UI (any name and save the name in `.env`) and select "Local Subprocess"

- Start your AWS EC2 instance and connect to the AWS CLI. Add your aws credentials before running aws configure and run this code using the database credentials created during the AWS set up. You can add the data in the `.env` file:

   ```bash
    mlflow server -h 0.0.0.0 -p 5000 --backend-store-uri postgresql://${DB_USER}:${DB_PASSWORD}@${DB_ENDPOINT}:5432/${DB_NAME} --default-artifact-root s3://${BUCKET_NAME}
    ```

Make sure to have in the `.env` the Public IPv4 DNS of your instance (each time you stop and restart the instance again, the DNS changes). It shall be something like this (add the 5000 and copy it in the browser). You shall be able to see the MLflow UI:

   ```bash
   AWS_URI=http://ec2-44-174-44-227.compute-1.amazonaws.com:5000/
   ```

- Start Prefect in a terminal:

   ```bash
   perfect server start
    ```

- Start Docker Desktop and build the image (to stop it use  `docker-compose down`):

   ```bash
   docker-compose up --build
   ```

- Train and deploy the model, giving a name for the run (any name) and the created Work Pool. Look for the run in the Prrefect UI:

   ```bash
    prefect deploy train.py:main_flow -n any-name -p ${WORK_POOL}
    ```

- Start the worker in a new terminal::

    ```bash
     prefect worker start -p ${WORK_POOL} -t process
    ```

- To run the deployment, go to the Prefect UI and under the run click **quick run**. In the terminal, you will be asked to give an experiment name and if you want to replace or append the database (if already exists).The deployment will be shown in the prefect UI and in the terminal

- Once the training has finished, you will see some print outs with the results in the terminal.

- In MLFlow and Prefect UI you can check the model and all the logs

- For monitoring, login in Grafana and Adminer to see the results there and create visualizations: 

  - Grafana  http://localhost:3000/: you need to login the first time with "admin" as username and password.

  - Adminer http://localhost:8080/. Login with:
    - System: `PostgreSQL`
    - Server: db
    - Username: the user in `grafana_datasources.yaml`
    - Password: the password in `grafana_datasources.yaml`
    - Database: the database in `grafana_datasources.yaml`

Make sure in Grafana, under Data Sources, that you add PostgreSQL. Then click in create a dashboard/visualization and select PostgreSQL. The created table shall be visible there.

Once you create a visualization, save it there and copy the corresponding JSON file in the dashboard folder. If you stop the image (`docker-compose down`) and run again`docker-compose up`, after login in Grafana, you should be able to see the dashboard again.

### Prediction

To run a prediction make sure the following variables after training the model are available in the `.env` file.

```bash
RUN_ID = os.getenv("RUN_ID")
BUCKET_NAME = os.getenv("BUCKET_NAME")
EXPERIMENT_ID = os.getenv("EXPERIMENT_ID")

logged_model = f's3://{BUCKET_NAME}/{EXPERIMENT_ID}/{RUN_ID}/artifacts/models_mlflow'
```

After that run in one terminal:

```bash
 python .\predict.py
```

And in another terminal:

```bash
 python .\test.py
 ```

 The predictions will be shown in these last terminal. The folder integration test, contains the predictions integrated in Dockerfile and docker-compose.yml.
