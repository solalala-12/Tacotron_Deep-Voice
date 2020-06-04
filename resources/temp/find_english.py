

import re 
import json
    
with open ('./datasets/son_own/alignment.json') as json_file:
    json_data=json.load(json_file)


_data_split_log = open('./datasets/son_total/data_split_최종.log', 'a')


def detect_english(w):

  for i in w.split(' '):
    
    english_check=re.compile('[a-zA-Z]+')
    m=english_check.match(i)
    if m:
      return m.group()



_data_split_log.write('------------------영어가 감지된 파일-------------------\n')

for key,value in json_data.items():

    if detect_english(value) :
        _data_split_log.write(str([key,value])+'\n')


_data_split_log.close()