# Use an official Python runtime as a parent image
FROM python:3.9

# Set environment variables to prevent Python from writing .pyc files and buffering output
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Create and set the working directory
WORKDIR /app

# Install system dependencies for Django and face_recognition
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    gcc \
    pkg-config \
    cmake \
    libopenblas-dev \
    liblapack-dev \
    libx11-dev \
    && rm -rf /var/lib/apt/lists/*

# Install additional dependencies for face recognition
RUN pip install --no-cache-dir \
    numpy \
    dlib \
    face_recognition \
    scipy \
    pathlib \
    pickle-mixin

# Copy dependency list and install Python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip 
RUN pip install -r requirements.txt



# Copy the entire application into the container
COPY . /app/

# Expose port 8000 for Django
EXPOSE 8000

# Command to run the Django application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
