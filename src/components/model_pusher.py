import sys

from src.cloud_storage import SimpleStorageService
from src.entity import (
    ModelEvaluationArtifact,
    ModelPusherArtifact,
    ModelPusherConfig,
    Proj_Estimator,
)
from src.exception import MyException
from src.logger import logger


class ModelPusher:
    def __init__(
        self,
        model_evaluation_artifact: ModelEvaluationArtifact,
        model_pusher_config: ModelPusherConfig,
    ):
        """
        :param model_evaluation_artifact: Output reference of data evaluation artifact stage
        :param model_pusher_config: Configuration for model pusher
        """
        self.s3 = SimpleStorageService()
        self.model_evaluation_artifact = model_evaluation_artifact
        self.model_pusher_config = model_pusher_config
        self.proj1_estimator = Proj_Estimator(
            bucket_name=model_pusher_config.bucket_name,
            model_path=model_pusher_config.s3_model_key_path,
        )

    def initiate_model_pusher(self) -> ModelPusherArtifact:
        """
        Method Name :   initiate_model_evaluation
        Description :   This function is used to initiate all steps of the model pusher

        Output      :   Returns model evaluation artifact
        On Failure  :   Write an exception log and then raise an exception
        """
        logger.info("Entered initiate_model_pusher method of ModelTrainer class")

        try:
            print(
                "------------------------------------------------------------------------------------------------"
            )
            logger.info("Uploading artifacts folder to s3 bucket")

            logger.info("Uploading new model to S3 bucket....")
            self.proj1_estimator.save_model(
                from_file=self.model_evaluation_artifact.trained_model_path
            )
            model_pusher_artifact = ModelPusherArtifact(
                bucket_name=self.model_pusher_config.bucket_name,
                s3_model_path=self.model_pusher_config.s3_model_key_path,
            )

            logger.info("Uploaded artifacts folder to s3 bucket")
            logger.info(f"Model pusher artifact: [{model_pusher_artifact}]")
            logger.info("Exited initiate_model_pusher method of ModelTrainer class")

            return model_pusher_artifact
        except Exception as e:
            raise MyException(e, sys) from e
