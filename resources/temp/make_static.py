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
import numpy as np
from hparams import hparams
# 



'''
as_token 확인하기 ***************************************************************************************************
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

    data_name='son_own_slience_2'
    with open ('./datasets/'+data_name+'/alignment.json') as json_file:
        json_data=json.load(json_file)

    write_path='./datasets/'+data_name+'/meta_static_s2/'
    if not os.path.exists(write_path):
        os.mkdir(write_path)


    for key,value in tqdm(json_data.items()):

        
        good_name=os.path.basename(key)+'.json'
        if os.path.exists(write_path+good_name):
            continue
        if not value.endswith('.'):
            value+='.'

        npz_path=os.path.basename(key)[:-4]+'.npz'
        npz_path='./datasets/'+data_name+'/data_s2/'+npz_path
        # train에 쓰이지 않는 데이터라면 패스
        
        if not os.path.exists(npz_path):
            continue

        train_yn=True

        npz_=np.load(npz_path)
        min_n_frame = hparams.reduction_factor * hparams.min_iters
        max_n_frame = hparams.reduction_factor * hparams.max_iters - hparams.reduction_factor
        n_frame=npz_["linear"].shape[0]
        tokens=npz_["tokens"]
        if not (min_n_frame <= n_frame <= max_n_frame and len(tokens) >= hparams.min_tokens):
             train_yn=False

        
        jl=[]
        # 중성
        jv=[]
        # 종성
        jt=[]
        # 특수문자
        p=[]

   
        if train_yn:
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
                if str(i) in PUNC:
                    p.append(i)
    
            data = {
                '파일명': key,
                '문장': value,
                '데이터 가용': train_yn,
                '토큰 리스트': list(tokens),
                '상세 문장' : count_tokens(value),
                '토큰 총 갯수': len(list(tokens)),
                '토큰 별 갯수':count_tokens(tokens),
                '초성': count_tokens(jl),
                '중성': count_tokens(jv),
                '종성': count_tokens(jt),
                '특수문자':count_tokens(p),
                '프레임 크기':n_frame,
                

            }
            
            # print(key)
            # good_name=key.split('/')[-1][:11]+"("+key[key.find("(")+1:key.find(")")]+")"
            good_name=os.path.basename(key)+'.json'
            print(good_name)

            try:
                with open (write_path+good_name ,'w',encoding='utf-8') as f:
                    json.dump(data,f,indent='\t',ensure_ascii=False)
            except:
                print(write_path+good_name)
                pass






