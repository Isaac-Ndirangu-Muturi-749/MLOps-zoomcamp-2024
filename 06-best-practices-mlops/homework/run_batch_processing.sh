#!/bin/bash

# Start LocalStack in a Docker container
docker run -d --rm \
  --name localstack \
  -e SERVICES=s3 \
  -e DEBUG=1 \
  -p 4566:4566 \
  localstack/localstack

# Wait for LocalStack to initialize (adjust sleep time as needed)
echo "Waiting for LocalStack to start..."
sleep 10

# Create an S3 bucket using the AWS CLI
aws --endpoint-url=http://localhost:4566 s3 mb s3://nyc-duration

# Set environment variables for batch_s3.py
export INPUT_FILE_PATTERN="s3://nyc-duration/in/{year:04d}-{month:02d}.parquet"
export OUTPUT_FILE_PATTERN="s3://nyc-duration/out/{year:04d}-{month:02d}.parquet"
export S3_ENDPOINT_URL="http://localhost:4566"

# Run batch_s3.py with year and month arguments
python batch_s3.py 2024 03

# Stop LocalStack container after processing
docker stop localstack
