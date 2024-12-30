import sys

from network_security.exception.exception import NetworkSecurityException
from network_security.logging.logger import logging
from network_security.components.data_ingestion import DataIngestion
from network_security.components.data_validation import DataValidation
from network_security.entity.config_entity import (
    DataIngestionConfig,
    DataValidationConfig,
)
from network_security.entity.config_entity import TrainingPipelineConfig

if __name__ == "__main__":
    try:
        logging.info("Data Ingestion Started")
        training_pipeline_config = TrainingPipelineConfig()
        data_ingestion_config = DataIngestionConfig(training_pipeline_config)
        data_ingestion = DataIngestion(data_ingestion_config)
        data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
        logging.info("Data Ingestion Completed")
        print(data_ingestion_artifact)

        logging.info("Data Validation Started")
        data_validation_config = DataValidationConfig(training_pipeline_config)
        data_validation = DataValidation(
            data_ingestion_artifact, data_validation_config
        )
        data_validation_artifact = data_validation.initiate_data_validation()
        logging.info("Data Validation Completed")
        print(data_validation_artifact)

    except Exception as e:
        raise NetworkSecurityException(e, sys)
