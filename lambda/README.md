# Lambda Function

This folder contains the predictions using AWS Lambda and Kinesis:

- `lambda_function.py`: the lambda function
- `test_lambda.py`: the test check w/o Dockerfile
- `test_docker.py`: the test check with Dockerfile
- `Dockerfile`: to test the lambda function with Docker
- `requirements.txt`: the requirements for the Dockerfile
- `results_printouts`: some print outs of the prediction

I also included a .env file in the compilation of the Dockerfile. It is needed to add the credentials AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_DEFAULT_REGION in case it is not locally saved.

## Lambda Prediction

The `test_lambda.py` file contains the following variables. You can either add yours there and export them and use os.getenv, or add them in the Lambda Function in AWS. Otherwise the prediction with Dockerfile won't work.

```bash
BUCKET_NAME="mlflow-tracking-remote"
RUN_ID="aa806b4bc4044777a0a25d5b8a24d7d5"
EXPERIMENT_ID=29
```

To get the prediction w/o Dockerfile, just run:

```bash
python .\test_lambda.py
```

To get the prediction with Dockerfile, you need to create a Lambda Function and Kinesis Stream in AWS and to have the necessary credentials and permissions:

- Lambda: car-model-prediction
- Kinesis: car_events

The run in one terminal:

```bash
docker build --no-cache -t my-lambda-prediction .
```

```bash
docker run -it --rm -p 8080:8080 -e PREDICTIONS_STREAM_NAME="car_events" -e TEST_RUN="True" -e AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID} -e AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY} -e AWS_DEFAULT_REGION=${AWS_DEFAULT_REGION} my-lambda-prediction
```

Finally in a separate terminal:

```bash
python .\test_docker.py
```
