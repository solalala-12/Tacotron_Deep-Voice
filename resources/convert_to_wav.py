


from glob import glob
import os
import argparse
import subprocess
from pydub import silence
from pydub import AudioSegment

def convert_to_wav (path,ext):
    '''
    * 특정 확장자 파일을 wav로 변환하는 코드
    
    path : ext 파일이 있는 폴더 
    ext : wav파일로 변환할 파일 확장자

    ext - > wav

    '''

    file_list=glob(os.path.join(path,'*.'+ext))
    for i in file_list:
        print(i)
        text='ffmpeg -i {} {}'.format(i,os.path.splitext(i)[0]+'.wav')
        print(text)
        subprocess.call(text,shell=True)
        os.remove(i)




if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument('--path',default=None)
    parser.add_argument('--ext',default="m4a")
    config=parser.parse_args()
    convert_to_wav(config.path,config.ext)

