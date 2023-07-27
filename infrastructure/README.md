conda install -c conda-forge terraform

After configuration of the main.tf and variables.tf in the main directory and module Kinesis

terraform init

terraform plan and enter value: ride-events-stg and accept with yes

(terraform) PS C:\Users\bmart\OneDrive\11_MLOps\mlops-car-prices\infrastructure> terraform plan
var.source_stream_name
  Enter a value: ride-events-stg

terraform plan and enter value: ride-events-stg

(terraform) PS C:\Users\bmart\OneDrive\11_MLOps\mlops-car-prices\infrastructure> terraform apply
var.source_stream_name
  Enter a value: ride-events-stg and accept with yes


After this, in AWS Kinesis the stream shall be visible ride-events-stg-mlops-zoomcamp




Now we configure S3 main and variables

We initializa again with terraform init. We shall see now our S3 Bucket

(terraform) PS C:\Users\bmart\OneDrive\11_MLOps\mlops-car-prices\infrastructure> terraform init

Initializing the backend...
Initializing modules...
- output_kinesis_stream in modules\kinesis
- s3_bucket in modules\S3

terraform plan and apply
and give a S3 Bucket name stg-mlflow-ride-model and output stream stg_ride_predictions and source stream stg_ride_events. By changing the stream name, we will see that the old stream created before will disappear


After this, in AWS Kinesis and S3 the stream and Bucket shall be visible 



Now we do ecr. For this we need the Dockerfile, model.py and lambda function.py

we will also create a stg.tfvars file to store the variables, so we do not need to type them again

terraform plan -var-file=C:\Users\bmart\OneDrive\11_MLOps\mlops-car-prices\infrastructure\vars\stg.tfvars

terraform apply -var-file=C:\Users\bmart\OneDrive\11_MLOps\mlops-car-prices\infrastructure\vars\stg.tfvars



We will see a new bucket for staging stg-mlflow-ride-model-mlops-zoomcamp

Psuh the image in advance if any error

docker build --no-cache -t lambda_image:latest .

As the model was built with scikit-learn 1.3.0, we check the requirements has been passed
docker run -it --rm --entrypoint="" lambda_image python -c "import sklearn; print(sklearn.__version__)"


aws ecr get-login-password --region eu-central-1 | docker login --username AWS --password-stdin 406468071577.dkr.ecr.eu-central-1.amazonaws.com

docker tag lambda_image:latest 406468071577.dkr.ecr.eu-central-1.amazonaws.com/stg_stream_model_duration_mlops-zoomcamp:latest

docker push 406468071577.dkr.ecr.eu-central-1.amazonaws.com/stg_stream_model_duration_mlops-zoomcamp:latest

To check if the image is there m you can pull also
docker pull 406468071577.dkr.ecr.eu-central-1.amazonaws.com/stg_stream_model_duration_mlops-zoomcamp:latest

And we can run again locally
docker run -it --rm --entrypoint="" 406468071577.dkr.ecr.eu-central-1.amazonaws.com/stg_stream_model_duration_mlops-zoomcamp:latest python -c "import sklearn; print(sklearn.__version__)"

docker run -it --rm --entrypoint="" lambda_image pip list


./deploy-manual.sh

It might take a couple fo minutes for the log to appear
aws kinesis put-record --stream-name stg_car_events-mlops-zoomcamp --partition-key 1 --cli-binary-format raw-in-base64-out --data '{\"car_ID\": 10, \"symboling\": 0, \"CarName\": \"audi 5000s (diesel)\", \"fueltype\": \"gas\", \"aspiration\": \"std\", \"doornumber\": \"two\", \"carbody\": \"hatchback\", \"drivewheel\": \"4wd\", \"enginelocation\": \"front\", \"wheelbase\": 99.5, \"carlength\": 178.2, \"carwidth\": 67.9, \"carheight\": 52, \"curbweight\": 3053, \"enginetype\": \"ohc\", \"cylindernumber\": \"five\", \"enginesize\": 131, \"fuelsystem\": \"mpfi\", \"boreratio\": 3.13, \"stroke\": 3.4, \"compressionratio\": 7, \"horsepower\": 160, \"peakrpm\": 5500, \"citympg\": 16, \"highwaympg\": 22, \"price\": 17859.17}'





aws lambda update-function-configuration --function-name stg_prediction_lambda_mlops-zoomcamp --environment "Variables={RUN_ID=aa806b4bc4044777a0a25d5b8a24d7d5}"


aws lambda list-event-source-mappings --function-name stg_prediction_lambda_mlops-zoomcamp

aws lambda delete-event-source-mapping --uuid aab89aae-5846-4907-ac4c-febfeaeebd63

terraform apply -var-file=C:\Users\bmart\OneDrive\11_MLOps\mlops-car-prices\infrastructure\vars\stg.tfvars

Check if it is enabled
aws lambda list-event-source-mappings --function-name stg_prediction_lambda_mlops-zoomcamp