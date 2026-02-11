import sys
from dataclasses import dataclass
from typing import Optional

import pandas as pd
from sklearn.metrics import f1_score

from src.constants import TARGET_COLUMN
from src.entity import (
    DataIngestionArtifact,
    ModelEvaluationArtifact,
    ModelEvaluationConfig,
    ModelTrainerArtifact,
    Proj_Estimator,
)
from src.exception import MyException
from src.logger import logger
from src.utils import load_object


@dataclass
class EvaluateModelResponse:
    trained_model_f1_score: float
    best_model_f1_score: float
    is_model_accepted: bool
    difference: float


class ModelEvaluation:

    def __init__(
        self,
        model_eval_config: ModelEvaluationConfig,
        data_ingestion_artifact: DataIngestionArtifact,
        model_trainer_artifact: ModelTrainerArtifact,
    ):
        try:
            self.model_eval_config = model_eval_config
            self.data_ingestion_artifact = data_ingestion_artifact
            self.model_trainer_artifact = model_trainer_artifact
        except Exception as e:
            raise MyException(e, sys) from e

    def get_best_model(self) -> Optional[Proj_Estimator]:
        """
        Method Name :   get_best_model
        Description :   This function is used to get model from production stage.

        Output      :   Returns model object if available in s3 storage
        On Failure  :   Write an exception log and then raise an exception
        """
        try:
            bucket_name = self.model_eval_config.bucket_name
            model_path = self.model_eval_config.s3_model_key_path
            proj1_estimator = Proj_Estimator(
                bucket_name=bucket_name, model_path=model_path
            )

            if proj1_estimator.is_model_present(model_path=model_path):
                return proj1_estimator
            return None
        except Exception as e:
            raise MyException(e, sys)

    def _map_gender_column(self, df):
        """Map Gender column to 0 for Female and 1 for Male."""
        logger.info("Mapping 'Gender' column to binary values")
        df["Gender"] = df["Gender"].map({"Female": 0, "Male": 1}).astype(int)
        return df

    def _create_dummy_columns(self, df):
        """Create dummy variables for categorical features."""
        logger.info("Creating dummy variables for categorical features")
        df = pd.get_dummies(df, drop_first=True)
        return df

    def _rename_columns(self, df):
        """Rename specific columns and ensure integer types for dummy columns."""
        logger.info("Renaming specific columns and casting to int")
        df = df.rename(
            columns={
                "Vehicle_Age_< 1 Year": "Vehicle_Age_lt_1_Year",
                "Vehicle_Age_> 2 Years": "Vehicle_Age_gt_2_Years",
            }
        )
        for col in [
            "Vehicle_Age_lt_1_Year",
            "Vehicle_Age_gt_2_Years",
            "Vehicle_Damage_Yes",
        ]:
            if col in df.columns:
                df[col] = df[col].astype("int")
        return df

    def _drop_id_column(self, df):
        """Drop the 'id' column if it exists."""
        logger.info("Dropping 'id' column")
        if "_id" in df.columns:
            df = df.drop("_id", axis=1)
        return df

    def evaluate_model(self) -> EvaluateModelResponse:
        """
        Method Name :   evaluate_model
        Description :   This function is used to evaluate trained model
                        with production model and choose best model

        Output      :   Returns bool value based on validation results
        On Failure  :   Write an exception log and then raise an exception
        """
        try:
            test_df = pd.read_csv(self.data_ingestion_artifact.test_file_path)
            x, y = (
                test_df.drop(columns=TARGET_COLUMN, errors="raise"),
                test_df[TARGET_COLUMN],
            )

            logger.info("Test data loaded and now transforming it for prediction...")

            x = self._map_gender_column(x)
            x = self._drop_id_column(x)
            x = self._create_dummy_columns(x)
            x = self._rename_columns(x)

            trained_model = load_object(
                file_path=self.model_trainer_artifact.trained_model_file_path
            )
            logger.info("Trained model loaded/exists.")
            trained_model_f1_score = (
                self.model_trainer_artifact.metric_artifact.f1_score
            )
            logger.info(f"F1_Score for this model: {trained_model_f1_score}")

            best_model_f1_score: Optional[float] = None
            best_model = self.get_best_model()
            if best_model is not None:
                logger.info("Computing F1_Score for production model..")
                y_hat_best_model = best_model.predict(x)
                best_model_f1_score = f1_score(y, y_hat_best_model)
                logger.info(
                    f"F1_Score-Production Model: {best_model_f1_score}, F1_Score-New Trained Model: {trained_model_f1_score}"
                )

            tmp_best_model_score = (
                0 if best_model_f1_score is None else best_model_f1_score
            )
            result = EvaluateModelResponse(
                trained_model_f1_score=trained_model_f1_score,
                best_model_f1_score=best_model_f1_score,
                is_model_accepted=trained_model_f1_score > tmp_best_model_score,
                difference=trained_model_f1_score - tmp_best_model_score,
            )
            logger.info(f"Result: {result}")
            return result

        except Exception as e:
            raise MyException(e, sys)

    def initiate_model_evaluation(self) -> ModelEvaluationArtifact:
        """
        Method Name :   initiate_model_evaluation
        Description :   This function is used to initiate all steps of the model evaluation

        Output      :   Returns model evaluation artifact
        On Failure  :   Write an exception log and then raise an exception
        """
        try:
            print(
                "------------------------------------------------------------------------------------------------"
            )
            logger.info("Initialized Model Evaluation Component.")
            evaluate_model_response = self.evaluate_model()
            s3_model_path = self.model_eval_config.s3_model_key_path

            model_evaluation_artifact = ModelEvaluationArtifact(
                is_model_accepted=evaluate_model_response.is_model_accepted,
                s3_model_path=s3_model_path,
                trained_model_path=self.model_trainer_artifact.trained_model_file_path,
                changed_accuracy=evaluate_model_response.difference,
            )

            logger.info(f"Model evaluation artifact: {model_evaluation_artifact}")
            return model_evaluation_artifact
        except Exception as e:
            raise MyException(e, sys) from e
