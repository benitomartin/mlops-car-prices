Run in Git Bash





### Putting everything to Docker

```bash

docker build --no-cache -t my-lambda-prediction .


docker run -it --rm -p 8080:8080 -e PREDICTIONS_STREAM_NAME="car_events" my-lambda-prediction


python .\test_lambda.py