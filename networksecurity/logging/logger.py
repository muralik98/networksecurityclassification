import logging 
from datetime import datetime
import os 


def logger_function(folder_name):
    logs_path = os.path.join(os.getcwd(), "logs", folder_name)
    os.makedirs(logs_path, exist_ok=True)
    log_file = f"{datetime.now().strftime('%d_%m_%Y_%H_%M_%S')}.log"
    log_file_path = os.path.join(logs_path, log_file)

    # Set up logging
    logging.basicConfig(
        filename=log_file_path,
        format="[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s",
        level=logging.INFO,
    )
    
    # Return a logger instance
    return logging.getLogger(__name__)

