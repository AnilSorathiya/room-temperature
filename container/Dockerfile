# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Installing pre-requisites
RUN apt-get update && apt-get install -y curl gcc uwsgi-plugin-python3

# Copy the current directory contents into the container
WORKDIR /app

# room temperature
ADD ./src/ ./src/
ADD ./src/utils/ ./src/utils/
ADD requirements.txt .
ADD run_service.sh ./
ADD wsgi.ini ./
ADD routes.py ./

# Install any needed packages specified in requirements.txt
RUN python3 -m ensurepip
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

WORKDIR /app

# Run app.py when the container launches
CMD ["./run_service.sh"]
