import os, uuid
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

'''
window 환경 기준
1. 패키지 설치: pip install azure-storage-blob
2. 엑세스 키 연결: setx AZURE_STORAGE_CONNECTION_STRING "DefaultEndpointsProtocol=https;AccountName=adlskyowon;AccountKey=pXaPQKkHngsedsHPyoP9o47j61y3yMS0AVzieNNq05DnyIA/J7QPhnv5cF8XXnXyU2ZPH+8rscJRbyy4kAOwEA==;EndpointSuffix=core.windows.net"
3. 다운 받을 파일이 있는 azure상 경로 설정: blob_path 수정
4. local상 경로 및 디렉토리 설정: local_path, local_dir_path 수정
'''


try:
    connect_str = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
    blob_service_client = BlobServiceClient.from_connection_string(connect_str)

    container_name = "edu"
    container_client = blob_service_client.get_container_client(container_name)
    
    #azure path
    blob_path = "/parentsvoice_conversion/resource/datasets_for_analy/test/"
    blob_list  = container_client.list_blobs(blob_path)

    #local path
    local_path = 'D:/hjtest'
    local_dir_path = local_path +'/' + 'datasets_audio'
    os.makedirs(local_dir_path)    
 
    for blob in blob_list:
        
        #os.path.split(path): seperate to dir, file
        _, tail = os.path.split("{}".format(blob.name))

        file_path = blob_path  + tail
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=file_path)

        local_file_path = local_dir_path + '/' + tail

        print("\nDownloading blob to \n\t" + local_file_path)

        with open(local_file_path, "wb") as my_blob:
            download_stream = blob_client.download_blob()
            my_blob.write(download_stream.readall())
        
except Exception as ex:
    print('Exception:')
    print(ex)