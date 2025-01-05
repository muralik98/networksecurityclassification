from networksecurity.logging.logger import logger_function  
from networksecurity.exception.CustomException import NetworkSecurityException  


import sys 
"""
lf = logger_function('exec')

lf.info('Hi Testing') 

try:
        lf.info("Enter the try block")
        a=1/0
        print("This will not be printed",a)
except Exception as e:
           lf.info(str(e))
           raise NetworkSecurityException(e,sys)

           """