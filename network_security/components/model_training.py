import os, sys
import mlflow
import dagshub

# Initialize dagshub
dagshub.init(repo_owner="Zoro-chi", repo_name="NetworkSecurity", mlflow=True)

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score, r2_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import (
    RandomForestClassifier,
    AdaBoostClassifier,
    GradientBoostingClassifier,
)


from network_security.constants import training_pipeline
from network_security.exception.exception import NetworkSecurityException
from network_security.logging.logger import logging
from network_security.entity.artifact_entity import (
    DataTransformationArtifact,
    ModelTrainingArtifact,
)
from network_security.entity.config_entity import ModelTrainingConfig
from network_security.utils.common import (
    save_object,
    load_object,
    load_numpy_array_data,
    evaluate_models,
)
from network_security.utils.ml_utils.metric.classification_metric import (
    get_classification_score,
)
from network_security.utils.ml_utils.model.estimator import NetworkModel


class ModelTraining:
    def __init__(
        self,
        model_training_config: ModelTrainingConfig,
        data_transformation_artifact: DataTransformationArtifact,
    ):
        try:
            self.model_training_config = model_training_config
            self.data_transformation_artifact = data_transformation_artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def track_mlflow(self, model, classification_metric):
        with mlflow.start_run():
            f1_score = classification_metric.f1_score
            recall_score = classification_metric.recall_score
            precision_score = classification_metric.precision_score

            mlflow.log_metric("f1_score", f1_score)
            mlflow.log_metric("recall_score", recall_score)
            mlflow.log_metric("precision_score", precision_score)
            mlflow.sklearn.log_model(model, "model")

    def train_model(self, x_train, y_train, x_test, y_test):
        models = {
            "Random Forest": RandomForestClassifier(verbose=1),
            "Decision Tree": DecisionTreeClassifier(),
            "Gradient Boosting": GradientBoostingClassifier(verbose=1),
            "Logistic Regression": LogisticRegression(verbose=1),
            "Ada Boost": AdaBoostClassifier(),
        }

        params = {
            "Decision Tree": {
                "criterion": ["gini", "entropy", "logloss"],
                # "splitter": ["best", "random"],
                # "max_features": ["sqrt", "log2"],
            },
            "Random Forest": {
                "n_estimators": [8, 16, 32, 64, 128, 256],
                # "criterion": ["gini", "entropy", "logloss"],
                # "max_features": ["sqrt", "log2", "None"],
            },
            "Gradient Boosting": {
                # "loss": ["logloss", "exponential"],
                "learning_rate": [0.1, 0.01, 0.05, 0.001],
                "subsample": [0.6, 0.7, 0.75, 0.8, 0.85, 0.9],
                # "criterion": ["friedman_mse", "squared_error"],
                # "max_features": ["sqrt", "log2", "auto"],
                "n_estimators": [8, 16, 32, 64, 128, 256],
            },
            "Logistic Regression": {},
            "AdaBoost": {
                "n_estimators": [8, 16, 32, 64, 128, 256],
                "learning_rate": [0.1, 0.01, 0.05, 0.001],
            },
        }

        model_report: dict = evaluate_models(
            x_train, y_train, x_test, y_test, models, params
        )

        # To get the best model score from the model report
        best_model_score = max(sorted(model_report.values()))
        # To get the best model name from the model report
        best_model_name = list(model_report.keys())[
            list(model_report.values()).index(best_model_score)
        ]
        # To get the best model from the model report
        best_model = models[best_model_name]

        y_train_pred = best_model.predict(x_train)
        classification_train_metric = get_classification_score(y_train, y_train_pred)
        # * TRACK EXPERIMENTS WITH MLFLOW
        # self.track_mlflow(best_model, classification_train_metric)

        y_test_pred = best_model.predict(x_test)
        classification_test_metric = get_classification_score(y_test, y_test_pred)
        # * TRACK EXPERIMENTS WITH MLFLOW
        self.track_mlflow(best_model, classification_test_metric)

        preprocessor = load_object(
            self.data_transformation_artifact.transformed_object_file_path
        )
        model_dir_path = os.path.join(
            self.model_training_config.trained_model_file_path
        )
        os.makedirs(model_dir_path, exist_ok=True)

        model_file_path = os.path.join(
            model_dir_path, training_pipeline.MODEL_FILE_NAME
        )
        Network_Model = NetworkModel(preprocessor, best_model)
        save_object(model_file_path, Network_Model)

        # Save final model to be used for predictions / Model Pusher
        save_object("final_model/model.pkl", best_model)

        # Model Training Artifact
        model_training_artifact = ModelTrainingArtifact(
            self.model_training_config.trained_model_file_path,
            classification_train_metric,
            classification_test_metric,
        )
        logging.info(f"Model training artifact: {model_training_artifact}")

        return model_training_artifact

    def initiate_model_training(self) -> ModelTrainingArtifact:
        try:
            train_file_path = (
                self.data_transformation_artifact.transformed_train_file_path
            )
            test_file_path = (
                self.data_transformation_artifact.transformed_test_file_path
            )

            # Load train and test arrays
            train_arr = load_numpy_array_data(train_file_path)
            test_arr = load_numpy_array_data(test_file_path)

            x_train, y_train, x_test, y_test = (
                train_arr[:, :-1],  # This takes all columns except the last one
                train_arr[:, -1],  # This takes only the last column
                test_arr[:, :-1],
                test_arr[:, -1],
            )

            model_training_artifact = self.train_model(x_train, y_train, x_test, y_test)

            return model_training_artifact

        except Exception as e:
            logging.error("Failed to train model.")
            raise NetworkSecurityException(e, sys)
