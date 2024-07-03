#!/bin/bash

# Define variables
S3_ENDPOINT_URL="http://localhost:4566"
S3_BUCKET="nyc-duration"
SCRIPT_DIR="/workspaces/MLOps-zoomcamp-2024/06-best-practices-mlops/homework"
DATA_DIR="${SCRIPT_DIR}/data"
IN_DATA_FILE="2023-01.parquet"

# Step 1: Start LocalStack and Docker services if not already running
echo "Starting LocalStack and Docker services..."
docker-compose up -d

# Step 2: Create S3 bucket if it doesn't exist
echo "Creating S3 bucket '${S3_BUCKET}'..."
aws --endpoint-url=${S3_ENDPOINT_URL} s3 mb s3://${S3_BUCKET}

# Step 3: Upload input data to S3
echo "Uploading input data '${IN_DATA_FILE}' to S3..."
aws --endpoint-url=${S3_ENDPOINT_URL} s3 cp ${DATA_DIR}/${IN_DATA_FILE} s3://${S3_BUCKET}/in/${IN_DATA_FILE}

# Step 4: Run batch processing script
echo "Running batch processing script..."
python ${SCRIPT_DIR}/batch.py --input s3://${S3_BUCKET}/in/${IN_DATA_FILE} --output s3://${S3_BUCKET}/out/${IN_DATA_FILE}-results.parquet

# Step 5: Validate results (compute sum of predicted durations)
echo "Validating results..."
python ${SCRIPT_DIR}/integration_test.py

# Step 6: Clean up (optional)
# Uncomment the following lines if you want to clean up resources after testing
#echo "Cleaning up..."
#docker-compose down

echo "Integration test complete."
