# Use an official Python runtime as the base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install system dependencies required for librosa, numpy, and h5py
RUN apt-get update && apt-get install -y \
    libsndfile1 \
    libblas3 \
    liblapack3 \
    libatlas-base-dev \
    gfortran \
    pkg-config \
    libhdf5-dev \
    && rm -rf /var/lib/apt/lists/*

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Explicitly install resampy
RUN pip install resampy

# Copy the current directory contents into the container
COPY . .

# Make sure the model file is present
RUN test -f ICO_model.h5 || (echo "ICO_model.h5 is missing" && exit 1)

# Create the dataset directory
RUN mkdir -p dataset

# Make port 10000 available to the world outside this container
EXPOSE 10000

# Run the application
CMD ["python", "app.py"]