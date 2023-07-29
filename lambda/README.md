# Lambda Function

This folder contains the predictions using AWS Lambda and Kinesis:

- `lambda_function.py`: the lambda function
- `test_lambda.py`: the test check w/o Dockerfile
- `test_docker.py`: the test check with Dockerfile
- `Dockerfile`: to test the lambda function with Docker
- `requirements.txt`: the requirements for the Dockerfile

I also included a .env file in the compilation of the Dockerfile. It is needed to add the credentials AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY.


## Lambda Prediction

To get the prediction w/o Dockerfile, just run:

```bash
python .\test_lambda.py
```

To get the prediction with Dockerfile, you need to create a Lambda Function and Kinesis Stream in AWS:

- Lambda: car-model-prediction
- Kinesis: car_events

The run in one terminal:

```bash
docker build --no-cache -t my-lambda-prediction .
```

```bash
docker run -it --rm -p 8080:8080 -e PREDICTIONS_STREAM_NAME="car_events" my-lambda-prediction
```

Finally in a separate terminal:

```bash
python .\test_lambda.py
```