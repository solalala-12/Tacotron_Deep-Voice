


import shutil
import os



paths='./datasets/moon_own/work/'

lists=os.listdir(paths)

for i in lists:
    wav=i.replace('.txt','.wav')
    shutil.copy('./datasets/moon_own/rs/'+wav, paths+wav)