# Network Security Project for Phishing Detection

This project focuses on network security by leveraging machine learning and data science techniques to detect phishing attacks. The project involves data ingestion, validation, transformation, and model training to build a robust phishing detection system.

## Table of Contents

- [Project Overview](#project-overview)
- [Directory Structure](#directory-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Data Ingestion](#data-ingestion)
- [Data Validation](#data-validation)
- [Data Transformation](#data-transformation)
- [Model Training](#model-training)
- [API Endpoints](#api-endpoints)
- [Syncing Artifacts to S3](#syncing-artifacts-to-s3)
- [Docker](#docker)
- [GitHub Actions Workflow](#github-actions-workflow)
- [Results](#results)

## Project Overview

This project focuses on network security by leveraging machine learning and data science techniques to detect phishing attacks. The project involves data ingestion, validation, transformation, and model training to build a robust phishing detection system.

## Directory Structure

```plaintext
NetworkSecurity/
├── artifacts/
├── data_schema/
├── network_security/
│   ├── components/
│   ├── entity/
│   ├── exception/
│   ├── logging/
│   ├── utils/
├── saved_models/
├── templates/
├── venv/
├── .gitignore
├── app.py
├── main.py
├── requirements.txt
├── Dockerfile
├── .github/
│   └── workflows/
│       └── network-security-workflow.yml
└── README.md
```

## Prerequisites

- Python 3.7 or higher
- MongoDB
- Git

## Installation

1. Clone the repository:

   ```sh
   git clone https://github.com/Zoro-chi/NetworkSecurity.git
   cd NetworkSecurity
   ```

2. Create a virtual environment:

   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the dependencies:

   ```sh
   pip install -r requirements.txt
   ```

## Usage

1. Ensure you have the necessary environment variables set up. You can use a .env file for this purpose.

2. Run the main script:

   ```sh
   python main.py
   ```

3. Run FastAPI application:

   ```sh
   uvicorn app:app --reload
   ```

## Configuration

Configuration settings are defined in the `network_security/constants/training_pipeline.py` file. You can adjust the settings for data ingestion, validation, transformation, and model training as needed.

## Data Ingestion

The data ingestion component reads data from a MongoDB collection and exports it as a DataFrame. The data is then split into training and testing sets.

## Data Validation

The data validation component checks the number of columns and detects data drift between the training and testing datasets. It generates a drift report saved in the `artifacts` directory.

## Data Transformation

The data transformation component handles missing values using KNN imputation and transforms the data into a suitable format for model training.

## Model Training

The model training component trains a machine learning model using the transformed data. The trained model is saved in the `artifacts` directory.

## API Endpoints

The project includes a FastAPI application with the following endpoints:

- GET /: Redirects to the API documentation.
- GET /train: Runs the training pipeline.
- POST /predict: Accepts a CSV file and returns predictions.

  ### Example Usage

  1.  Train the model:

      ```sh
      curl -X GET "http://localhost:8000/train"
      ```

  2.  Make predictions using the model:

      ```sh
      curl -X POST "http://localhost:8000/predict" -F "file=@path_to_your_csv_file"
      ```

      #### Note: Replace `path_to_your_csv_file` with the path to your CSV file.

## Syncing Artifacts to S3

The project includes functionality to sync local artifacts and saved models to an S3 bucket.

### Sync Local Artifacts to S3

```python
def sync_artifacts_dir_to_s3(self):
try:
aws_bucket_url = f"s3://{training_pipeline.S3_TRAINING_BUCKET_NAME}/artifacts/{self.training_pipeline_config.timestamp}"
S3Sync.sync_folder_to_s3(
self=S3Sync,
folder=self.training_pipeline_config.artifact_dir,
aws_bucket_url=aws_bucket_url,
)
except Exception as e:
raise NetworkSecurityException(e, sys)
```

### Sync Saved Models to S3

```python
def sync_saved_model_dir_to_s3(self):
    try:
        aws_bucket_url = f"s3://{training_pipeline.S3_TRAINING_BUCKET_NAME}/final_model/{self.training_pipeline_config.timestamp}"
        S3Sync.sync_folder_to_s3(
            self=S3Sync,
            folder=self.training_pipeline_config.model_dir,
            aws_bucket_url=aws_bucket_url,
        )
    except Exception as e:
        raise NetworkSecurityException(e, sys)
```

### S3Sync Class

```python
class S3Sync:
    def sync_folder_to_s3(self, folder: str, aws_bucket_url: str):
        command = f"aws s3 sync {folder} {aws_bucket_url} "
        os.system(command)

    def sync_folder_from_s3(self, aws_bucket_url: str, folder: str):
        command = f"aws s3 sync {aws_bucket_url} {folder} "
        os.system(command)
```

## Docker

The project uses Docker to containerize the application. The Docker image is built and pushed to Amazon ECR (Elastic Container Registry).

### Build and Run Docker Container

1. Build the Docker image:

```sh
  docker build -t network-security:latest .
```

2. Run the Docker container:

```sh
  docker run -p 8000:8000 network-security:latest
```

## GitHub Actions Workflow

The project includes a GitHub Actions workflow for continuous integration and continuous delivery. The workflow builds the Docker image and pushes it to Amazon ECR.

## Results

The results of the data ingestion, validation, transformation, and model training processes are saved in the artifacts directory. You can review the generated reports and trained models.
