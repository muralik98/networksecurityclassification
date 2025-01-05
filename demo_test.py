import sys, os 
from networksecurity.exception.CustomException import NetworkSecurityException
from networksecurity.logging.logger import logger_function
from networksecurity.entity.config_entity import TrainingPipelineConfig, DataIngestionConfig,DataValidationConfig
from networksecurity.entity.artifacts_entity import DataIngestionArtifact
from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.data_validation import DataValidation

    
def test():
    try:
        # Step 1: Instantiate TrainingPipelineConfig
        training_pipeline_config = TrainingPipelineConfig()  # By default, it uses the current timestamp

        # Step 2: Instantiate DataIngestionConfig with the TrainingPipelineConfig instance
        data_ingestion_config = DataIngestionConfig(training_pipeline_config)
        data_validation_config = DataValidationConfig(training_pipeline_config)
        # Step 3: Instantiate DataIngestion with DataIngestionConfig
        data_ingestion = DataIngestion(data_ingestion_config)

        # Step 4: Call the initiate_data_ingestion method to start the process
        dataingestion_artifact = data_ingestion.initiate_data_ingestion()

        data_validation = DataValidation(data_validation_config, dataingestion_artifact)

        data_validation_artifact = data_validation.initiate_data_validation()
    except NetworkSecurityException as e:
        # Handling custom exceptions
       raise NetworkSecurityException(e,sys)

test()