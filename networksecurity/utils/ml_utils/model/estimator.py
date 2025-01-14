from networksecurity.constants.train_constants import SAVED_MODEL_DIR,MODEL_FILE_NAME

import os
import sys

from networksecurity.exception.CustomException import NetworkSecurityException
from networksecurity.logging.logger import logger_function 

logging = logger_function("Model_Trainer")

class NetworkModel:
    def __init__(self,preprocessor,model):
        try:
            self.preprocessor = preprocessor
            self.model = model
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    def predict(self,x):
        try:
            x_transform = self.preprocessor.transform(x)
            y_hat = self.model.predict(x_transform)
            return y_hat
        except Exception as e:
            raise NetworkSecurityException(e,sys)