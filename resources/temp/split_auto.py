import os
import subprocess

class Data(object):
    def __init__(
            self, file_path, start_point, end_time, text):
        self.file_path = file_path
        self.start_point = start_point
        self.end_point = end_time
        self.text =text

def read_txt(path):
    # print(path)
    with open(path,'r',encoding='utf-8') as f:
        data = []
        for line in f:
            split_list=line.split('|')
            file_path, start_point, end_point=split_list[0:3]
            text=split_list[3]
            data.append(Data(file_path, start_point, end_point, text))
        return data


def split_audio(data):

    for idx, d in enumerate(data):
        original_path=d.file_path
        # 01.0001.wav
        fname, ext = os.path.splitext(d.file_path)
        out_path_audio=(fname + '.{}.wav').format("%04d" % idx)
        out_path_assets=(fname  + '.{}.txt').format("%04d" % idx)
       

        # mp3 file에서 원하는 만큼 자르고 wav파일로 저장
        #  ffmpeg -i test.mp3 -ss 00:00:00 -to 00:00:30  temp.wav

        texts='ffmpeg -i {} -ss {} -to {}  {}'.format(original_path,
        "%02d:%02d:%02d" % (0, int(d.start_point.split(':')[0]), int(d.start_point.split(':')[1])),"%02d:%02d:%02d" % (0, int(d.end_point.split(':')[0]), int(d.end_point.split(':')[1])),out_path_audio)
        # print(texts)
        subprocess.call(texts,shell=True)
        f = open(out_path_assets, 'w')
        f.write(d.text)
        f.close()
        # remove_file(original_path)


if __name__ == '__main__':

    base_dir='./temp'
    data = read_txt(os.path.join(base_dir, "temp.txt"))
    split_audio(data)