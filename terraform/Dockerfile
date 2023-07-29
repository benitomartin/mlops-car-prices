FROM public.ecr.aws/lambda/python:3.9

RUN pip install -U pip

# Install dependencies from requirements.txt
COPY [ "requirements.txt", "./" ]
RUN pip install -r requirements.txt

# Copy the lambda function code and the .env file
COPY [ "lambda_function.py", "lambda_model.py", "./" ]
# COPY .env .

CMD [ "lambda_function.lambda_handler" ]
