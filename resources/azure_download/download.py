
from __future__ import print_function
import sys,os
import argparse
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

# run to shell before code run
'''
우분투 환경 기준
1. pip3 install azure-storage-blob
2. 
export AZURE_STORAGE_CONNECTION_STRING="DefaultEndpointsProtocol=https;AccountName=adlskyowon;AccountKey=pXaPQKkHngsedsHPyoP9o47j61y3yMS0AVzieNNq05DnyIA/J7QPhnv5cF8XXnXyU2ZPH+8rscJRbyy4kAOwEA==;EndpointSuffix=core.windows.net"
3. blob_path에 다운 받고자 하는 경로 직접 수정하고 python3 download.py 실행
4. 또는 python3 download.py --data_name=son_audio_full 실행

'''



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_name',default=None,required=False)
    config = parser.parse_args()
    data_name=config.data_name
    

    try:
        connect_str = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
        blob_service_client = BlobServiceClient.from_connection_string(connect_str)

        container_name = "edu"
        container_client = blob_service_client.get_container_client(container_name)
        
        # path in azure
        blob_path = "/parentsvoice_conversion/resource/datasets_for_analy/"+data_name+'/'
        print('blob_path',blob_path)
        
        blob_list  = container_client.list_blobs(blob_path)
        # resouces/
        pwd=os.getcwd()

        local_path_parent_folder=os.path.join(pwd,'datasets',data_name.split('/')[0])

        
        if 'audio' in data_name:
            local_path_folder= os.path.join(local_path_parent_folder,'audio')
        elif 'assets' in data_name:

            local_path_folder= os.path.join(local_path_parent_folder,'assets')
        else:
            local_path_folder= os.path.join(local_path_parent_folder,'data')


        # datasets/data_name is not exists
        
        if not os.path.exists(local_path_parent_folder):
            print("making folder =" ,local_path_parent_folder)
            os.makedirs(local_path_parent_folder)

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

            if (tail.endswith(".wav") or tail.endswith(".npz") or tail.endswith(".txt")):
                local_path_file= os.path.join(local_path_folder,tail)
                print("\nDownloading blob to \n\t" + local_path_file)

                with open(local_path_file, "wb") as my_blob:
                    download_stream = blob_client.download_blob()
                    my_blob.write(download_stream.readall())

            else:
                continue

        print("다운로드 완료.")
            
    except Exception as ex:
        print('Exception:')
        print(ex)



if __name__ == '__main__':
    main()
