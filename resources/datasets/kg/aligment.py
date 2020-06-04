import os
import sys

from utils import parallel_run, remove_file, backup_file, write_json


dicts={}
with open ('transcript.v.1.3.txt','r',encoding='utf-8') as f:
    while(True):
        line=f.readline()
        if not line:
            break

        texts=line.split('|')[:2]
        dicts['./datasets/kg/audio/'+texts[0]]=texts[1]
        

write_json('./datasets/kg/alignment.json', dicts)


