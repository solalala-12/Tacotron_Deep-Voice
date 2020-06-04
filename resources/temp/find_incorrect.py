


import os 
import json
# recogniton 과 alignment를 비교해서 매핑이 되어있지 않은 문장 확인 
# alignment_old.json vs recognition.json
import os, sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from recognition.alignment import similarity




'''
def similarity(text_a, text_b):
    text_a = plain_text(text_a)
    text_b = plain_text(text_b)

    score = SequenceMatcher(None, text_a, text_b).ratio()
    return score

'''

wrong_list=open('./datasets/son_own_slience_2/wroing_list.txt','w',encoding='utf-8') 

with open ('./datasets/son_own_slience_2/alignment.json','r',encoding='utf-8') as alignmnet:
	texts_alignment=json.load(alignmnet)


with open ('./datasets/son_own_slience_2/recognition.json','r',encoding='utf-8') as recognition:
	texts_recognition=json.load(recognition)


# print(texts_recognition)
count=0
wrong_list.write('{} / {} /{} \n'.format('WAV','우리','API'))
for key,value in texts_alignment.items():

	try:
		score=similarity(value,texts_recognition[key])
		# print(score)
		if score<=0.5:
			count+=1
			wrong_list.write('{} / {} /{} \n'.format(key.split('/')[-1],value,texts_recognition[key]))

	except:
		pass
		
		
		
print(count)
wrong_list.close()