# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set environment variables to prevent python from writing .pyc files and buffering output
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Create and set the working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/

# Install system dependencies for Django and PostgreSQL (if you use PostgreSQL)
RUN apt-get update && \
    apt-get install -y libpq-dev && \
    pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy the entire application into the container
COPY . /app/

# Expose port 8000 to access the application
EXPOSE 8000

# Command to run the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
