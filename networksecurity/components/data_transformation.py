import os,sys 
sys.path.append('../Proj-networksecurity')
from networksecurity.exception.CustomException import NetworkSecurityException
from networksecurity.logging.logger import logger_function
from networksecurity.constants.train_constants import TARGET_COLUMN , DATA_TRANSFORMATION_IMPUTER_PARAMS 
from networksecurity.entity.artifacts_entity import DataValidationArtifact, DataTransformationArtifcat 
from networksecurity.entity.config_entity import DataTransformationConfig
from networksecurity.utils.main_utils.code_utils import save_numpyarray_data, save_object 
import numpy as np
import pandas as pd 
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline

logging = logger_function("data_transformation")
class DataTransformation:

    def __init__(self, data_validation_artifact:DataValidationArtifact, data_transfromation_config:DataTransformationConfig):
        
        try:
            self.data_validation_artifact:DataValidationArtifact=data_validation_artifact
            self.data_transfromation_config:DataTransformationConfig = data_transfromation_config
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    @staticmethod
    def read_data(file_path)->pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def get_data_transformer_objects(cls)->Pipeline:

        logging.info("Performing get_data_transformer_objects")

        try:
            imputer:KNNImputer=KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS)
            logging.info(f"KNN Inputer Initialized with {DATA_TRANSFORMATION_IMPUTER_PARAMS}")
            
            transform_pipe:Pipeline=Pipeline([("imputer", imputer)])
            return transform_pipe
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def initiate_data_transformation(self)->DataTransformationArtifcat:
        logging.info("Data Transformation Initiated")
        try:
            train_df = DataTransformation.read_data(self.data_validation_artifact.valid_train_file_path)
            test_df = DataTransformation.read_data(self.data_validation_artifact.valid_train_file_path)
            
            # Train Data 
            input_feature_train_df = train_df.drop(columns=[TARGET_COLUMN],axis=1)
            target_feature_train_df = train_df[TARGET_COLUMN].replace(-1,0)

            # Test Data 
            input_feature_test_df = train_df.drop(columns=[TARGET_COLUMN],axis=1)
            target_feature_test_df = train_df[TARGET_COLUMN].replace(-1,0)  
            
            transform_pipe = self.get_data_transformer_objects()

            preprocess_pipe = transform_pipe.fit(input_feature_train_df)
            transformed_input_train_feature = preprocess_pipe.transform(input_feature_train_df)
            transformed_input_test_feature  = preprocess_pipe.transform(input_feature_test_df)

            train_arr = np.c_[transformed_input_train_feature, np.array(target_feature_train_df)] 
            test_arr = np.c_[transformed_input_test_feature, np.array(target_feature_test_df)] 

            # Save Train and Test as numpy data 

            save_numpyarray_data(self.data_transfromation_config.transformed_train_file_path, array=train_arr)
            save_numpyarray_data(self.data_transfromation_config.transformed_test_file_path, array=test_arr)
            save_object(self.data_transfromation_config.transformed_object_file_path, preprocess_pipe)

            save_object("final_model/preprocessor.pkl", preprocess_pipe)


            data_transformation_artifact = DataTransformationArtifcat(
                transformed_object_file_path=self.data_transformation_config.transformed_object_file_path,
                transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path=self.data_transformation_config.transformed_test_file_path

            )

            return data_transformation_artifact
        
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        