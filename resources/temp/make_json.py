
# 폴더 내 파일을 읽어와 txt파일 한줄 - audio 파일 하나 mapping


import os 
import atexit
import shutil
import os, sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from utils import write_json
from tqdm import tqdm

parents_dir='./datasets/son_total'


file_count=0
al_json={}



alignment_json = './datasets/moon_own/alignment.json'
data_split_log= './datasets/moon_own/data_split.log'
name_folder_list=[i for i in os.listdir(parents_dir) if not(i.endswith('.log'))]
print(name_folder_list)
for i in name_folder_list:
    if i != 'moon_split':
        continue

    # datasets/son_total/lee
    each_folder_path = os.path.join(parents_dir,i)
    # datasets/son_total/lee/NB~
    each_folders=os.listdir(each_folder_path)
    
    print(' {}의 폴더 갯수 : {}'.format(i,len(each_folders)))
    # datasets/son_total/lee/NB
    for j in tqdm(each_folders):
        
        each_file_path=os.path.join(each_folder_path,j)
        each_split_files=[i for i in os.listdir(each_file_path) if i.endswith(".wav")]
        # (1),(2) 순으로 정렬
        each_split_files.sort(key = lambda i : int(i[i.find("(")+1:i.find(")")]))


        _alignment_json = open(alignment_json, 'a')
        _data_split_log = open(data_split_log,'a')
        try:
            txt_file=open(each_file_path+'/'+j+'.txt','r',encoding='utf-8')

        except FileNotFoundError:
            _data_split_log.write('{}의 {}의 txt파일을 찾지 못함 \n'.format(i,j))
        
        # scripts
        texts=txt_file.readlines()
        # audio 파일과 text의 문장길이가 같은지 확인 
        if (len(texts) != len(os.listdir(os.path.join(each_folder_path,j)))-1):
           
            _data_split_log.write('{}의 {}가 갯수가 맞지 않음. \n'.format(i,j))
            continue

        # 파일 하나씩 접근
        
        
        for idx, z in enumerate(each_split_files):
            file_count+=1
            
            # print(z)
            text_json=texts[idx].strip('' ',\n')
            if not text_json.endswith('.'):
                text_json+='.'

            each_wav_path=(os.path.join(each_file_path,z))
            if not (os.path.exists(os.path.join('./datasets/moon_own/audio/',each_wav_path))):
                shutil.copy(each_wav_path,'./datasets/moon_own/audio/')
            al_json['./datasets/moon_own/audio/'+z]=text_json
        
            
            
        
write_json(alignment_json,al_json)    
_data_split_log.write('총 {}개의 문장 \n'.format(file_count))
        
_alignment_json.close()
_data_split_log.close()
