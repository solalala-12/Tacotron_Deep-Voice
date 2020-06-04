import os, uuid
import datetime
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
import argparse
from models import get_most_recent_checkpoint


# run to shell before code run
'''
export AZURE_STORAGE_CONNECTION_STRING="DefaultEndpointsProtocol=https;AccountName=adlskyowon;AccountKey=pXaPQKkHngsedsHPyoP9o47j61y3yMS0AVzieNNq05DnyIA/J7QPhnv5cF8XXnXyU2ZPH+8rscJRbyy4kAOwEA==;EndpointSuffix=core.windows.net"
'''
def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--folder_name',default=None)
    parser.add_argument('--rm_log',default='True')
    config=parser.parse_args()


    

    try:
        connect_str = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
        blob_service_client = BlobServiceClient.from_connection_string(connect_str)

        container_name = "edu"
        container_client = blob_service_client.get_container_client(container_name)    

        # model.ckpt - most_recent


        #파일이 저장되어 있는 로컬 경로 
        local_path= './'+config.folder_name

        print(local_path)

        if ( 'logs' in config.folder_name):

            if (config.rm_log=='True'):
                print("이전 로그 파일을 삭제하고 업로드 하시겠습니까? (y/n)")
                an=input()
                if(an=='y'):

                    lastest_checkpoint=get_most_recent_checkpoint(local_path).split('/')[-1]
                    do_not_remove=['train.log','hparams.py','params.json','checkpoint',lastest_checkpoint+'.index',lastest_checkpoint+'.meta',lastest_checkpoint+'.index',lastest_checkpoint+'.data-00000-of-00001']
                    file_list = os.listdir(local_path)
                    # print(file_list)
                    # file_list_py = [file for file in file_list if file.endswith(".wav")]

                    for i in file_list:
                        # print(i)
                        _,ext=os.path.splitext(i)
                        # wav file 이 아니고 지워야하는 대상에 없으면
                        if( (ext != ".wav" and ext !='.png')  and  i not in do_not_remove):
                            print( "remove :",local_path+'/'+i)
                            os.remove(local_path+'/'+i)
                    print('파일 삭제 완료')

            else:
                print('삭제하지 않고 업로드합니다.')


        
        print( ' local_path  ',local_path)
        file_list=os.listdir(local_path)
        

        #여러개의 파일 한번에 업로드 하기
        for file_name in file_list:

            local_file_name = file_name
            upload_file_path = os.path.join(local_path, local_file_name)
            #업로드할 경로 설정
            upload_blob_path = os.path.join("/parentsvoice_conversion/resource/datasets",config.folder_name ,local_file_name)
           
            # upload_blob_path = "/parentsvoice_conversion/resource/datasets/logs/logs_"+config.log_name +'/'+ local_file_name

            blob_client = blob_service_client.get_blob_client(container=container_name, blob=upload_blob_path)
            print(file_name)
            with open(upload_file_path, "rb") as data:
                blob_client_re  = container_client.upload_blob(name=upload_blob_path,data = data, overwrite=True)  
        
        
        properties = blob_client_re.get_blob_properties()
        
        print(datetime.datetime.now())
        print(properties)
        print('upload 완료')



    except Exception as ex:
        print('Exception:')            



if __name__=='__main__':
    main()
