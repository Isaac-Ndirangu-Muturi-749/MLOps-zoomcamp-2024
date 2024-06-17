FROM agrigorev/zoomcamp-model:mlops-2024-3.10.13-slim

# Set environment variables to ensure pipenv runs in non-interactive mode
ENV PIPENV_VENV_IN_PROJECT=true \
    PIPENV_IGNORE_VIRTUALENVS=1

# Install pipenv
RUN pip install pipenv

# Copy your Pipfile and Pipfile.lock into the container
COPY Pipfile Pipfile.lock ./

# Install dependencies using pipenv
RUN pipenv install --deploy --system

# Copy your script into the container
COPY homework_04_deployment.py .

# Run the script for May 2023
CMD ["python", "homework_04_deployment.py", "--year", "2023", "--month", "5"]
