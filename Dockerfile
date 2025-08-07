
# Pull base image
FROM python:3.11

# Set environment variables
ENV PYTHONUNBUFFERED 1

# Set work directory
RUN mkdir /code
WORKDIR /code/

# Upgrade pip
RUN pip install --upgrade pip

# Install requirements
COPY . requirements.txt /code/
RUN pip install -r requirements.txt

# Copy project
COPY . /code/
