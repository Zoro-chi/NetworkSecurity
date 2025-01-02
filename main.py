import sys

from network_security.components.model_training import ModelTraining
from network_security.exception.exception import NetworkSecurityException
from network_security.logging.logger import logging
from network_security.components.data_ingestion import DataIngestion
from network_security.components.data_validation import DataValidation
from network_security.components.data_transformation import DataTransformation
from network_security.entity.config_entity import (
    DataIngestionConfig,
    DataValidationConfig,
    DataTransformationConfig,
    ModelTrainingConfig,
)
from network_security.entity.config_entity import TrainingPipelineConfig

if __name__ == "__main__":
    try:
        # DATA INGESTION
        logging.info("Data Ingestion Started")
        training_pipeline_config = TrainingPipelineConfig()
        data_ingestion_config = DataIngestionConfig(training_pipeline_config)
        data_ingestion = DataIngestion(data_ingestion_config)
        data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
        print(data_ingestion_artifact)
        logging.info("Data Ingestion Completed")

        # DATA VALIDATION
        logging.info("Data Validation Started")
        data_validation_config = DataValidationConfig(training_pipeline_config)
        data_validation = DataValidation(
            data_ingestion_artifact, data_validation_config
        )
        data_validation_artifact = data_validation.initiate_data_validation()
        print(data_validation_artifact)
        logging.info("Data Validation Completed")

        # DATA TRANSFORMATION
        logging.info("Data Transformation Started")
        data_transformation_config = DataTransformationConfig(training_pipeline_config)
        data_transformation = DataTransformation(
            data_validation_artifact=data_validation_artifact,
            data_transformation_config=data_transformation_config,
        )
        data_transformation_artifact = (
            data_transformation.initiate_data_transformation()
        )
        print(data_transformation_artifact)
        logging.info("Data Transformation Completed")

        # MODEL TRAINING
        logging.info("Model Training Started")
        model_training_config = ModelTrainingConfig(training_pipeline_config)
        model_training = ModelTraining(
            model_training_config, data_transformation_artifact
        )
        model_training_artifact = model_training.initiate_model_training()
        print(model_training_artifact)
        logging.info("Model Training Completed")

    except Exception as e:
        raise NetworkSecurityException(e, sys)
