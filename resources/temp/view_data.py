

import os 
import glob
import numpy as np


a=np.load('D:/parentsvoice_1.13.1/resources/datasets/son_own_slience_2/data_s2/NB10620453 (1).npz')
print(a['tokens'])
'''

lists_own=glob.glob('./datasets/son_own/audio/*.wav')
lists_data=glob.glob('./datasets/son_own/data_/*.npz')


lists_owns=[os.path.basename(i)[:-4] for i in lists_own]
print(len(lists_owns))
lists_datas=[os.path.basename(i)[:-4]for i in lists_data]
print(len(lists_datas))


s = set(lists_datas)
temp3 = [x for x in lists_owns if x not in s] #순서 보존됨

print(len(temp3))
for i in temp3:
    print(i)
    os.remove('./datasets/son_own/audio/'+i+'.wav')

'''