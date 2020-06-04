

import os 
import numpy as np
from tqdm import tqdm
import shutil
import json


basename='./datasets/moon_own/'
f=os.listdir(basename+'data/')
f3=open(basename+'long.txt','a')
with open(basename+'alignment.json') as w:
    jsons=json.load(w)


print(len(f))
count=0
for i in tqdm(f):
    npz_file=os.path.join(basename+'data/',i)
    data=np.load(npz_file)
    if len(data["tokens"])>=150:
        txt_name=os.path.basename(basename)+i.replace('.npz','.txt')
        wav_name=os.path.basename(basename)+i.replace('.npz','.wav')
        print('wav_name :',wav_name)
        print('txt_name :',txt_name)
        shutil.copy(basename+'audio/'+wav_name,basename+'work/'+wav_name)
        with open (basename+'work/'+txt_name,'a') as f2:
            f2.write(jsons[basename+'audio/'+i.replace('.npz','.wav')])

        f3.write(basename+'audio/'+wav_name+'\n')
        count+=1
print(count)

f3.close()