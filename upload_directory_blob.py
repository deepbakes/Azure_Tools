import argparse


import argparse
import glob
import os
from azure.storage.blob import BlobClient



def upload_directory_blob(target_dir, account_url, container_name, credentials):

    """A function which takes images from a target directory tree and returns stratified
    training and testing datasets.

    Args:
        target_dir (str): The target directory where files are located.
        account_url (str): The URL to the Azure container.
        container_name (str): The name of the container to store data.
        credentials (str): The Azure storage credentials.

    Returns:
        message (str)

    """

    file_list = glob.glob(f'{target_dir}/*') # Evaluate all files within target directory.
    print(f'Uploading {len(file_list)} Files.')

    for file in file_list[:1]:
        file_basename = os.path.basename(file) # Evaluate file base name.
        print(f'Starting Upload: {file_basename}')

        blob_url = f'{account_url}/{container_name}/{file_basename}' # Create Azure blob URL string.

        blob_client = BlobClient.from_blob_url(blob_url=blob_url, credential=credentials) # Connect to Azure Blob.

        try:
            with open(file, 'rb') as f:
                blob_client.upload_blob(f) # Upload files recursively.
                print(f'{file_basename} Uploaded Successfully.')

        except Exception as e:
            print(e)

    message = 'Successfully Uploaded Directory.'
    return message


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--target_dir', type=str, help='Target directory.')
    parser.add_argument('--account_url', type=str, help='Container URL.')
    parser.add_argument('--container_name', type=str, help='Container Name.')
    parser.add_argument('--credentials', type=str, help='Azure credentials.')
    args = parser.parse_args()

    upload_directory_blob(target_dir=args.target_dir, account_url=args.account_url,
                          container_name=args.container_name, credentials=args.credentials)
