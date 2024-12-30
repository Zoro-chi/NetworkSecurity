from scipy.stats import ks_2samp
import pandas as pd
import os, sys

from network_security.entity.artifact_entity import (
    DataIngestionArtifact,
    DataValidationArtifact,
)
from network_security.constants.training_pipeline import SCHEMA_FILE_PATH
from network_security.entity.config_entity import DataValidationConfig
from network_security.exception.exception import NetworkSecurityException
from network_security.logging.logger import logging
from network_security.utils.common import read_yaml_file, write_yaml_file


class DataValidation:
    def __init__(
        self,
        data_ingestion_artifact: DataIngestionArtifact,
        data_validation_config: DataValidationConfig,
    ):
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config
            self.schema = read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    @staticmethod
    def read_data(file_path: str) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def validate_number_of_columns(self, dataframe: pd.DataFrame) -> bool:
        try:
            number_of_columns = len(self.schema["columns"])
            logging.info(f"Number of columns in schema: {number_of_columns}")
            logging.info(f"Number of columns in dataframe: {dataframe.columns}")

            if len(dataframe.columns) == number_of_columns:
                return True
            else:
                return False

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def detect_data_drift(self, base_df, current_df, threshold=0.05) -> bool:
        try:
            status = True
            report = {}
            for column in base_df.columns:
                d1 = base_df[column]
                d2 = current_df[column]
                is_same_dist = ks_2samp(d1, d2)
                if threshold <= is_same_dist.pvalue:
                    is_found = False
                else:
                    is_found = True
                    status = False
                report.update(
                    {
                        column: {
                            "p_value": float(is_same_dist.pvalue),
                            "drift_status": is_found,
                        }
                    }
                )

                drift_report_file_path = (
                    self.data_validation_config.drift_report_file_path
                )

                # Create directory if not exists
                dir_path = os.path.dirname(drift_report_file_path)
                os.makedirs(dir_path, exist_ok=True)

                write_yaml_file(drift_report_file_path, report, replace=True)

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def initiate_data_validation(self) -> DataValidationArtifact:
        try:
            train_file_path = self.data_ingestion_artifact.trained_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path

            # Read data from train and test files
            train_dataframe = DataValidation.read_data(train_file_path)
            test_dataframe = DataValidation.read_data(test_file_path)

            # Validate number of columns
            status = self.validate_number_of_columns(train_dataframe)
            if not status:
                error_message = (
                    "Train Dataframe does not have all the columns as per schema. \n"
                )
            status = self.validate_number_of_columns(test_dataframe)
            if not status:
                error_message = (
                    "Test Dataframe does not have all the columns as per schema. \n"
                )

            # Check for data drift
            status = self.detect_data_drift(train_dataframe, test_dataframe)
            dir_path = os.path.dirname(
                self.data_validation_config.valid_train_file_path
            )
            os.makedirs(dir_path, exist_ok=True)

            train_dataframe.to_csv(
                self.data_validation_config.valid_train_file_path,
                index=False,
                header=True,
            )

            test_dataframe.to_csv(
                self.data_validation_config.valid_test_file_path,
                index=False,
                header=True,
            )

            data_validation_artifact = DataValidationArtifact(
                validation_status=status,
                valid_train_file_path=self.data_ingestion_artifact.trained_file_path,
                valid_test_file_path=self.data_ingestion_artifact.test_file_path,
                invalid_train_file_path=None,
                invalid_test_file_path=None,
                drift_report_file_path=self.data_validation_config.drift_report_file_path,
            )

            return data_validation_artifact

        except Exception as e:
            raise NetworkSecurityException(e, sys)
