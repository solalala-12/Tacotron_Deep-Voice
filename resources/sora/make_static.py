'''

문장별로
NB12392349 (1).json

{
    '파일명':'',
    '전체 문장':'',
    'tokens' : [],
    '자음':{'ㄱ':123,'ㄴ':0},
    '모음':{'ㅏ':2},
    '받침':{'ㄱ':23, 'ㄲ':123},
    '문자':{'간':1},
    '특수문자':{'?':1,'!':3,',':1,'.':23}
}



'''

import json
import os, sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from text import sequence_to_text, text_to_sequence
from tqdm import tqdm
from text.korean import JAMO_LEADS,JAMO_VOWELS,JAMO_TAILS,PUNC

# 

'''dictionary에 정의되지 않은 영어는 symbols_id 에서 값을 찾지 못해 오디오와 매칭이 안되는 상황
'''


def count_tokens(tokens):

    count_token={}
    # 순서유지 LIST 중복 제거
    def OrderedSet(list):
        my_set = set()
        res = []
        for e in list:
            if e not in my_set:
                res.append(e)
                my_set.add(e)

        return res
    unique_tokens=OrderedSet(tokens)
    for i in unique_tokens:
        count_token[i]=tokens.count(i)

    return count_token

if __name__=="__main__":

    with open ('./datasets/son_own/alignment.json') as json_file:
        json_data=json.load(json_file)

    write_path='./datasets/son_own/meta_static/'
    if not os.path.exists(write_path):
        os.mkdir(write_path)



    # print(json_data.items())

    for key,value in tqdm(json_data.items()):

        jl=[]
        # 중성
        jv=[]
        # 종성
        jt=[]
        # 특수문자
        p=[]

   
        
        # 한 글자씩
        for j in value:
                 # 초성
     
            # 특수 문자
            one_lists=text_to_sequence(j)
            one_lists=one_lists[:-1]

            if (value in PUNC):
                p.append(i)
            if (len(one_lists)==2):
                one,two=one_lists[0],one_lists[1]
                jl.append(one)
                jv.append(two)
            elif (len(one_lists)==3):
                one,two,three=one_lists[0],one_lists[1],one_lists[2]
                jl.append(one)
                jv.append(two)
                jt.append(three)


        tokens=text_to_sequence(value)
     
        for i in tokens:
            if i in  PUNC:
                p.append(i)
                

        data = {
            '파일명': key,
            '문장': value,
            '상세 문장' : count_tokens(value),
            '토큰 총 갯수': len(tokens),
            '토큰 별 갯수':count_tokens(tokens),
            '초성': count_tokens(jl),
            '중성': count_tokens(jv),
            '종성': count_tokens(jt),
            '특수문자':count_tokens(p)
        }
        
        print(key)
        good_name=key.split('/')[-1][:11]+"("+key[key.find("(")+1:key.find(")")]+")"
        
        with open (write_path+good_name ,'w',encoding='utf-8') as f:
            json.dump(data,f,indent='\t',ensure_ascii=False)
        






