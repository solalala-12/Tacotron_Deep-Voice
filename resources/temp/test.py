

import os 
import numpy as np
import json
import shutil
from tqdm import tqdm

# txt파일을 읽어와 이름과 audio 파일 매칭
folder_name='./datasets/moon_own/work/clear/'

list_files=[ i for i in os.listdir(folder_name) if i.endswith('.txt')]

alignment_json= './datasets/moon_own/alignment1.json'

def write_json(path, data):
    with open(path, 'w',encoding='utf-8') as f:
        json.dump(data, f, indent=4, sort_keys=True, ensure_ascii=False)


data={}

for i in tqdm(list_files):
	wav_file_name=i[:-4]+'.wav'
	with open('./datasets/moon_own/work/clear/'+i,"r",encoding='utf-8') as f:
		text=f.readline()
		data['./datasets/moon_own/audio/'+wav_file_name]=text



write_json(alignment_json,data)


'''

for i in list_files:

	data=np.load(os.path.join(folder_name),i)
	if data["tokens"]>125:
		_data_split_log = open(data_split_log,'a')
		_data_split_log.write(i)


_data_split_log.close()
'''