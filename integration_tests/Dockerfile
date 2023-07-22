# Use the official Python 3.9.16 slim base image
FROM python:3.9.16-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements.txt file and install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents (including the Flask app) into the container at /app
COPY . /app/

# Copy the integration test file into the container at /app
COPY test_integration.py /app/

# Expose the port on which Gunicorn will rsun (you can change this if desired)
EXPOSE 9696

# Set the entrypoint to run Gunicorn with the Flask app
ENTRYPOINT ["gunicorn", "--bind", "0.0.0.0:9696", "predict:app"]



