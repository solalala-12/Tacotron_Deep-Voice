import os, uuid
import datetime
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

'''
window 환경 기준
1. 패키지 설치: pip install azure-storage-blob
2. 엑세스 키 연결: setx AZURE_STORAGE_CONNECTION_STRING "DefaultEndpointsProtocol=https;AccountName=adlskyowon;AccountKey=pXaPQKkHngsedsHPyoP9o47j61y3yMS0AVzieNNq05DnyIA/J7QPhnv5cF8XXnXyU2ZPH+8rscJRbyy4kAOwEA==;EndpointSuffix=core.windows.net"
3. 업로드 할 파일이 있는 local상 경로 설정: local_path 수정
4. azure 위치 설정: upload_blob_path 수정
'''

try:
    connect_str = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
    blob_service_client = BlobServiceClient.from_connection_string(connect_str)

    container_name = "edu"
    container_client = blob_service_client.get_container_client(container_name)    


    #local path
    local_path= 'D:/hjtest/audio'
    file_list=os.listdir(local_path)

    for file_name in file_list:

        local_file_name = file_name
        upload_file_path = os.path.join(local_path, local_file_name)
        
        ##azure path
        upload_blob_path = "/parentsvoice_conversion/resource/datasets/audio/" + local_file_name

        blob_client = blob_service_client.get_blob_client(container=container_name, blob=upload_blob_path)

        print(datetime.datetime.now())
        with open(upload_file_path, "rb") as data:
            blob_client_re  = container_client.upload_blob(name=upload_blob_path, data = data, overwrite =False)  
    
    properties = blob_client_re.get_blob_properties()
    
    print(datetime.datetime.now())
    print(properties)

except Exception as ex:
    print('Exception:')
    print(ex)            