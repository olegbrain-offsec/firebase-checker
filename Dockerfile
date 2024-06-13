ARG PYTHON_VERSION=3.12.3
FROM python:${PYTHON_VERSION}-slim as base


WORKDIR /app

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY . /app
RUN apt-get update -y
RUN apt-get install -y gcc python3-dev
# RUN apt-get install build-essential 
# RUN apt-get install gcc
RUN pip3 install -r requirements.txt

# Run the application.
ENTRYPOINT [ "python3", "firebase_api_key_checker.py" ]