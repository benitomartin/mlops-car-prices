# Integration Tests

The integration tests can be run in 2 ways:

- Using Dockerfile
- Using docker-compose.yml

This folder contains a `requirements.txt` file that will help to build the image within this folder. Additionally copy the `.env` file from the root directory, so that the files can access the AWS credentials and other environmental variables needed to run the test in the Dockerfile

Additionally, the model is accessed from the S3 Bucket. The following environment variables must be available in the `.env` file after training a model.

```bash
RUN_ID = os.getenv("RUN_ID")
BUCKET_NAME = os.getenv("BUCKET_NAME")
EXPERIMENT_ID = os.getenv("EXPERIMENT_ID")

logged_model = f's3://{BUCKET_NAME}/{EXPERIMENT_ID}/{RUN_ID}/artifacts/models_mlflow'
```

## With Dockerfile

- Open Docker Desktop and build the image:

    ```bash
    docker build -t my-app .
    ```

- Run the container in a terminal:

    ```bash
    docker run --rm -p 9696:9696 -v ${BASE_DIR}\data:/app/data --name my-app my-app
    ```

- Run the integration test in another terminal (the prediction will be logged in the other terminal):

    ```bash
    docker exec -it my-app pytest test_integration.py
    ```

- To stop the container run:

    ```bash
    docker stop my-app
    ```

## With docker-compose.yml

1) **Option 1**

- Open Docker Desktop and build the image:

    ```bash
    docker-compose up -d or docker-compose up --build
    ```

- Check the container name in Docker Desktop (for example: integration_tests-my-app-1)

- Run the integration test with the container name (the prediction will be logged in the other terminal):

    ```bash
    docker exec -it integration_tests-my-app-1 pytest test_integration.py
    ```

- Run the prediction test in another terminal:

    ```bash
    docker exec -it my-app pytest test_integration.py
    ```

- To stop the container run:

    ```bash
    docker-compose down
    ```

2) **Option 2**

- To activate the  script

    ```bash
    icacls .\run.sh /grant Everyone:RX
    ```

- Run the script. You can uncomment the last line of the script so that the bash window won't close automatically. However, for the CI/CD test, the line must be commented:

    ```bash
    .\run.sh
    ```
