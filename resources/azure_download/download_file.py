
from __future__ import print_function
import sys,os
import argparse
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--file_name',default=None,required=False)
    config = parser.parse_args()
    file_name=config.file_name
    

    try:
        connect_str = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
        blob_service_client = BlobServiceClient.from_connection_string(connect_str)

        container_name = "edu"
        
        # path in azure
        blob_path = "/parentsvoice_conversion/resource/datasets_for_analy/"+file_name
        print('blob_path',blob_path)
        pwd=os.getcwd()
        local_path_file=os.path.join(pwd,'datasets',file_name)
        '''
        blob_list  = container_client.list_blobs(blob_path)
        # resouces/
        

        

        

        _, tail = os.path.split("{}".format(blob_list.name))
        
        file_path = blob_path  + tail
        '''
        # file info in azure
        blob_client = blob_service_client.get_blob_client(container=container_name, blob = "/parentsvoice_conversion/resource/datasets_for_analy/"+file_name)
        # local path to save

        with open(local_path_file, "wb") as my_blob:
            download_stream = blob_client.download_blob()
            my_blob.write(download_stream.readall())

        print("다운로드 완료.")
            
    except Exception as ex:
        print('Exception:')
        print(ex)



if __name__ == '__main__':
    main()
