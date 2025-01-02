import os
import sys
import pandas as pd
import numpy as np

"""
DEFININING COMMON CONSTANT VARIABLES
"""
TARGET_COLUMN: str = "Result"
PIPELINE_NAME: str = "NetworkSecurity"
ARTIFACT_DIR: str = "artifacts"
FILE_NAME: str = "phisingData.csv"
TRAIN_FILE_NAME: str = "train.csv"
TEST_FILE_NAME: str = "test.csv"
SCHEMA_FILE_PATH = os.path.join("data_schema", "schema.yaml")
PRERPOCESSING_OBJECT_FILE_NAME: str = "preprocessing.pkl"
SAVED_MODEL_DIR = os.path.join("saved_models")
MODEL_FILE_NAME: str = "model.pkl"


"""
DATA INGESTION RELATED CONSTANTS START WITH 'DATA_INGESTION' PREFIX
"""
DATA_INGESTION_COLLECTION_NAME: str = "NetworkData"
DATA_INGESTION_DATABASE_NAME: str = "Phising_Data_Science"
DATA_INGESTION_DIR_NAME: str = "data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR: str = "feature_store"
DATA_INGESTION_INGESTED_DIR: str = "ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO: float = 0.2

"""
DATA VALIDATION RELATED CONSTANTS START WITH 'DATA_VALIDATION' PREFIX
"""
DATA_VALIDATION_DIR_NAME: str = "data_validation"
DATA_VALIDATION_VALID_DIR: str = "valid"
DATA_VALIDATION_INVALID_DIR: str = "invalid"
DATA_VALIDATION_DRIFT_REPORT_DIR: str = "drift_report"
DATA_VALIDATION_DRIFT_REPORT_FILE_NAME: str = "report.yaml"

"""
DATA TRANSFORMATION RELATED CONSTANTS START WITH 'DATA_TRANSFORMATION' PREFIX
"""
DATA_TRANSFORMATION_DIR_NAME: str = "data_transformation"
DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR: str = "transformed"
DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR: str = "transformed_object"

# * KNN Imputer to replace nan values
DATA_TRANSFORMATION_INPUTTER_PARAMS: dict = {
    "missing_values": np.nan,
    "n_neighbors": 3,
    "weights": "uniform",
}

"""
MODEL TRAINING RELATED CONSTANTS START WITH 'MODEL_TRAINING' PREFIX
"""
MODEL_TRAINING_DIR_NAME: str = "model_training"
MODEL_TRAINING_TRAINED_MODEL_DIR: str = "trained_model"
MODEL_TRAINING_SCORE: float = 0.6
MODEL_TRAINING_OVERFITTING_UNDERFITTING_THRESHOLD: float = 0.05
