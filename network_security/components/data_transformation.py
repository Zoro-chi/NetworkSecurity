import sys, os
import pandas as pd
import numpy as np
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline

from network_security.constants.training_pipeline import TARGET_COLUMN
from network_security.constants.training_pipeline import (
    DATA_TRANSFORMATION_INPUTTER_PARAMS,
)
from network_security.entity.artifact_entity import (
    DataTransformationArtifact,
    DataValidationArtifact,
)
from network_security.entity.config_entity import DataTransformationConfig
from network_security.logging.logger import logging
from network_security.exception.exception import NetworkSecurityException
from network_security.utils.common import save_object, save_numpy_array_data


class DataTransformation:
    def __init__(
        self,
        data_validation_artifact: DataValidationArtifact,
        data_transformation_config: DataTransformationConfig,
    ):
        try:
            self.data_validation_artifact: DataValidationArtifact = (
                data_validation_artifact
            )
            self.data_transformation_config: DataTransformationConfig = (
                data_transformation_config
            )
        except Exception as e:
            raise NetworkSecurityException(e, sys) from e

    # A Static Method is a method that doesn't require an instance of the class to be created.
    @staticmethod
    def read_data(file_path: str) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e, sys) from e

    def get_data_transformer_object(cls) -> Pipeline:
        # * KNNImputer is a class that provides imputation for filling in missing values using the k-Nearest Neighbors approach.
        """
        Initialize a KNNImputer object with the given parameters
        and returns a Pipeline object with the KNNImputer object as the first step.
        """
        logging.info("In get_data_transformer_object method of DataTransformation")
        try:
            imputer: KNNImputer = KNNImputer(**DATA_TRANSFORMATION_INPUTTER_PARAMS)
            logging.info(
                f"Initalized KNNImputer object with params: {DATA_TRANSFORMATION_INPUTTER_PARAMS}"
            )
            processor: Pipeline = Pipeline([("imputer", imputer)])
            return processor
        except Exception as e:
            raise NetworkSecurityException(e, sys) from e

    def initiate_data_transformation(self) -> DataTransformationArtifact:
        try:
            logging.info("Initiating data transformation")
            train_data = DataTransformation.read_data(
                self.data_validation_artifact.valid_train_file_path
            )
            test_data = DataTransformation.read_data(
                self.data_validation_artifact.valid_test_file_path
            )

            # Training data transformation
            input_feature_train_data = train_data.drop(columns=[TARGET_COLUMN], axis=1)
            target_feature_train_data = train_data[TARGET_COLUMN]
            target_feature_train_data = target_feature_train_data.replace(-1, 0)

            # Testing data transformation
            input_feature_test_data = test_data.drop(columns=[TARGET_COLUMN], axis=1)
            target_feature_test_data = test_data[TARGET_COLUMN]
            target_feature_test_data = target_feature_test_data.replace(-1, 0)

            preprocessor = self.get_data_transformer_object()
            preprocessor_object = preprocessor.fit(input_feature_train_data)
            transformed_input_train_features = preprocessor_object.transform(
                input_feature_train_data
            )
            transformed_input_test_features = preprocessor_object.transform(
                input_feature_test_data
            )

            train_arr = np.c_[
                transformed_input_train_features, np.array(target_feature_train_data)
            ]
            test_arr = np.c_[
                transformed_input_test_features, np.array(target_feature_test_data)
            ]

            # Save transformed data
            save_numpy_array_data(
                self.data_transformation_config.transformed_train_file_path, train_arr
            )
            save_numpy_array_data(
                self.data_transformation_config.transformed_test_file_path, test_arr
            )
            save_object(
                self.data_transformation_config.transformed_object_file_path,
                preprocessor_object,
            )

            # Preparing DataTransformationArtifact object
            data_transformation_artifact = DataTransformationArtifact(
                transformed_object_file_path=self.data_transformation_config.transformed_object_file_path,
                transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path=self.data_transformation_config.transformed_test_file_path,
            )

            return data_transformation_artifact

        except Exception as e:
            raise NetworkSecurityException(e, sys) from e
