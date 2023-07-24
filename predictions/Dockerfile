# Use the official Python 3.9.16 slim base image
FROM python:3.9.16-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements.txt file and install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents (including the Flask app) into the container at /app
COPY . /app/

# Expose the port on which Gunicorn will run (you can change this if desired)
EXPOSE 8000


# Set the entrypoint to run Gunicorn with the Flask app
ENTRYPOINT ["gunicorn", "--bind", "0.0.0.0:8000", "predict:app"]

