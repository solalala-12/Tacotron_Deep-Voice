import os, uuid
import datetime
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
import argparse
import os, sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))



''
def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--file_name',default=None)
    config=parser.parse_args()

    
    try:
        connect_str = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
        blob_service_client = BlobServiceClient.from_connection_string(connect_str)

        container_name = "edu"
        container_client = blob_service_client.get_container_client(container_name)    

        # model.ckpt - most_recent


        #파일이 저장되어 있는 로컬 경로 
        local_path= './datasets/'+config.file_name

        print(local_path)

    
        try:

            
            upload_blob_path = "/parentsvoice_conversion/resource/datasets_for_analy/"+config.file_name
            print('upload_blob_path :',upload_blob_path)

            blob_client = blob_service_client.get_blob_client(container=container_name, blob=upload_blob_path)
            with open(local_path, "rb") as data:
                blob_client_re  = container_client.upload_blob(name=upload_blob_path,data = data, overwrite=True)  

        except Exception as ex:
            print('Exception:')
            print(ex)
    
        
        properties = blob_client_re.get_blob_properties()
        
        print(datetime.datetime.now())
        print(properties)



    except Exception as ex:
        print('Exception:')            



if __name__=='__main__':
    main()
