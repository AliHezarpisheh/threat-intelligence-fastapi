FROM python:3.13-slim

# Set the working directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set Python path to the working directory
ENV PYTHONPATH=app

# Install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the project files into the Docker container
COPY . .
