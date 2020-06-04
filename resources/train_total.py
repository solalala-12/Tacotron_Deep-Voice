import glob
import os
import numpy as np
from utils import write_json

'''
path = "./datasets/son_audio_full/audio/*"
file_list = glob.glob(path)
file_list_wav = [file for file in file_list if file.endswith(".wav")]

dicts={}
for i in file_list_wav:
    ext=os.path.splitext(i)[0]
    name=ext.split('/')[-1]
    print(name)
    myfile=name+'.txt'

    with open('./datasets/son_assets_full/assets/'+myfile) as f:
        dicts[i]=f.read()


write_json('./datasets/son_audio_full/alignment.json',dicts)

'''

a=np.load('./datasets/son_audio_full/data/NB10587175.npz')
#a=np.load('./datasets/son/data/NB10584578.0001.npz')
lst = a.files
for item in lst:
    print(item)
    print(a[item])
print(len(a['tokens']))
