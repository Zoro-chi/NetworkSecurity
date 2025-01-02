import os, sys

from network_security.components import data_ingestion
from network_security.exception.exception import NetworkSecurityException
from network_security.logging.logger import logging

from network_security.components.data_ingestion import DataIngestion
from network_security.components.data_validation import DataValidation
from network_security.components.data_transformation import DataTransformation
from network_security.components.model_training import ModelTraining

from network_security.entity.config_entity import (
    TrainingPipelineConfig,
    DataIngestionConfig,
    DataValidationConfig,
    DataTransformationConfig,
    ModelTrainingConfig,
)

from network_security.entity.artifact_entity import (
    DataIngestionArtifact,
    DataValidationArtifact,
    DataTransformationArtifact,
    ModelTrainingArtifact,
)


class TrainingPipeline:
    def __init__(self):
        self.training_pipeline_config = TrainingPipelineConfig()

    def start_data_ingestion(self):
        try:
            self.data_ingestion_config = DataIngestionConfig(
                self.training_pipeline_config
            )
            logging.info("Data Ingestion Started")
            data_ingestion = DataIngestion(self.data_ingestion_config)
            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
            logging.info(f"Data Ingestion Completed: {data_ingestion_artifact}")
            print("Data Ingestion Completed", data_ingestion_artifact)
            return data_ingestion_artifact

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def start_data_validation(self, data_ingestion_artifact: DataIngestionArtifact):
        try:
            self.data_validation_config = DataValidationConfig(
                self.training_pipeline_config
            )
            logging.info("Data Validation Started")
            data_validation = DataValidation(
                data_ingestion_artifact, self.data_validation_config
            )
            data_validation_artifact = data_validation.initiate_data_validation()
            logging.info(f"Data Validation Completed: {data_validation_artifact}")
            print("Data Validation Completed", data_validation_artifact)
            return data_validation_artifact

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def start_data_transformation(
        self, data_validation_artifact: DataValidationArtifact
    ):
        try:
            self.data_transformation_config = DataTransformationConfig(
                self.training_pipeline_config
            )
            logging.info("Data Transformation Started")
            data_transformation = DataTransformation(
                data_validation_artifact=data_validation_artifact,
                data_transformation_config=self.data_transformation_config,
            )
            data_transformation_artifact = (
                data_transformation.initiate_data_transformation()
            )

            logging.info(
                f"Data Transformation Completed: {data_transformation_artifact}"
            )
            print("Data Transformation Completed", data_transformation_artifact)
            return data_transformation_artifact

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def start_model_training(
        self, data_transformation_artifact: DataTransformationArtifact
    ) -> ModelTrainingArtifact:
        try:
            self.model_training_config = ModelTrainingConfig(
                self.training_pipeline_config
            )
            logging.info("Model Training Started")
            model_training = ModelTraining(
                self.model_training_config, data_transformation_artifact
            )
            model_training_artifact = model_training.initiate_model_training()
            logging.info(f"Model Training Completed: {model_training_artifact}")
            print("Model Training Completed", model_training_artifact)
            return model_training_artifact

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def run_pipeline(self):
        try:
            data_ingestion_artifact = self.start_data_ingestion()
            data_validation_artifact = self.start_data_validation(
                data_ingestion_artifact
            )
            data_transformation_artifact = self.start_data_transformation(
                data_validation_artifact
            )
            model_training_artifact = self.start_model_training(
                data_transformation_artifact
            )
            return model_training_artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys)
