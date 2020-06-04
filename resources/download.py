
from __future__ import print_function
import sys
import argparse
import os, uuid
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

import subprocess

# run to shell before code run
# export AZURE_STORAGE_CONNECTION_STRING="DefaultEndpointsProtocol=https;AccountName=adlskyowon;AccountKey=pXaPQKkHngsedsHPyoP9o47j61y3yMS0AVzieNNq05DnyIA/J7QPhnv5cF8XXnXyU2ZPH+8rscJRbyy4kAOwEA==;EndpointSuffix=core.windows.net"




def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_name',default=None)
    config = parser.parse_args()
    data_name=config.data_name
    

    try:
        connect_str = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
        blob_service_client = BlobServiceClient.from_connection_string(connect_str)

        container_name = "edu"
        container_client = blob_service_client.get_container_client(container_name)
        
        # path in azure
        blob_path = "/parentsvoice_conversion/resource/datasets/data_"+data_name+'/data/'
        print('blob_path',blob_path)
        
        blob_list  = container_client.list_blobs(blob_path)
        # resouces/
        pwd=os.getcwd()
        local_path_parent_folder=os.path.join(pwd,'datasets',data_name)
        local_path_folder=local_path_file= os.path.join(pwd,'datasets',data_name,'data')

        # datasets/data_name is not exists
        
        if not os.path.exists(local_path_parent_folder):
            print("making folder =" ,local_path_parent_folder)
            os.makedirs(os.path.join(pwd,'datasets',data_name))

        # datasets/data_name/data is not exists
        if not os.path.exists(local_path_folder):
            print("making folder =" ,local_path_folder )
            os.makedirs(local_path_folder)

        for blob in blob_list:
            # print('blob : ',blob)
            _, tail = os.path.split("{}".format(blob.name))
            file_path = blob_path  + tail
            # file info in azure
            blob_client = blob_service_client.get_blob_client(container=container_name, blob=file_path)
            # local path to save

            
        
            local_path_file= os.path.join(pwd,'datasets',data_name,'data',tail)
            print("\nDownloading blob to \n\t" + local_path_file)
        

            with open(local_path_file, "wb") as my_blob:
                download_stream = blob_client.download_blob()
                my_blob.write(download_stream.readall())
        
    except Exception as ex:
        print('Exception:')
        print(ex)



if __name__ == '__main__':
    main()
