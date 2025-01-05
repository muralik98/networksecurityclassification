from google.cloud import storage
from dotenv import load_dotenv
import os
import re 
# Load environment variables from .env file
load_dotenv()

# Retrieve the Google credentials file path from environment variables
google_credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
storage_client = storage.Client()
# Ensure the environment variable is set
if not google_credentials_path:
    raise ValueError("The GOOGLE_APPLICATION_CREDENTIALS environment variable is not set correctly.")


def download_and_move_files(bucket_name, source_folder, destination_folder, pattern, local_download_dir):
    # Get the bucket
    bucket = storage_client.bucket(bucket_name)
    
    # List blobs (files) in the source folder
    # blobs = bucket.list_blobs(prefix=source_folder)
    
    # List blobs (files) in the source folder
    blobs = list(bucket.list_blobs(prefix=source_folder))

    print(blobs)
    if len(blobs) == 0:
        return 'No File'
    # Loop through each blob in the source folder
    for blob in blobs:
        # Match files based on the pattern (e.g., data_*.csv)
        if re.match(pattern, blob.name):
            # Define the local path where the file will be downloaded
            destination_local_path = os.path.join(local_download_dir, os.path.basename(blob.name))
            
            # Download the blob (file) to the local machine
            blob.download_to_filename(destination_local_path)
            print(f"Downloaded {blob.name} to {destination_local_path}")
            
            # Move the file to the new folder in GCS (after download)
            new_blob_name = os.path.join(destination_folder, os.path.basename(blob.name))
            new_blob = bucket.blob(new_blob_name)
            bucket.copy_blob(blob, bucket, new_blob_name) 
            blob.delete()  # Optionally, delete the original file
            print(f"Moved {blob.name} to {new_blob_name}")


if __name__=='__main__':
    bucket_name = "network_security_project"
    source_folder = "new_data/"  # Assuming 'new_data' is the blob name or file path
    destination_folder = "archieve/"  # New folder where files should be moved
    pattern = r".*\.csv"  # Regex pattern to match the file names
    local_download_dir = "./ETL/"  # Local path where you want to save the file

download_and_move_files(bucket_name, source_folder, destination_folder, pattern, local_download_dir)
