# Code based on https://github.com/keithito/tacotron/blob/master/datasets/ljspeech.py
import os
import re
import sys
import json
import argparse
import numpy as np
from tqdm import tqdm
from glob import glob
from functools import partial

from collections import Counter, defaultdict
from concurrent.futures import ProcessPoolExecutor

import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt

from hparams import hparams
from text import text_to_sequence
from utils import makedirs, remove_file, warning
from audio import load_audio, spectrogram, melspectrogram, frames_to_hours

'''


 data = {
            "linear": linear_spectrogram.T,
            "mel": mel_spectrogram.T,
            "tokens": tokens,
            "loss_coeff": loss_coeff,
        }

npz를 만드는 과정

loss = linear_loss + mel_loss
'''

data_split_log= './datasets/son_total/data_split_최종.log'
bad_count=0
def one(x=None):
    return 1

def build_from_path(config):
    warning("Sampling rate: {}".format(hparams.sample_rate))

    executor = ProcessPoolExecutor(max_workers=config.num_workers)
    futures = []
    index = 1


    base_dir = os.path.dirname(config.metadata_path)
    # datasets/data
    data_dir = os.path.join(base_dir, config.data_dirname)
    makedirs(data_dir)

    # 일종의 dictionary
    # loss_codeff = 1로 고정 되어있으니 0.2 로 바뀌는 요소들은 recog_level 1,2 에서 짤림
    loss_coeff = defaultdict(one)
    # alignment.json
    with open(config.metadata_path,encoding='utf-8') as f:
        content = f.read()
            # print(content)
    info = json.loads(content)

    new_info = {}
    print(" 병합중")
    for path in tqdm(info.keys()):
        # print(path)
        if not os.path.exists(path):
            new_path = os.path.join(base_dir, path)
 
            if not os.path.exists(new_path):
                print(" [!] Audio not found: {}".format([path, new_path]))
                continue
        else:
            new_path = path

        
        # print(path)


        new_info[new_path] = info[path]

    info = new_info
    # info.keys= wav file
    '''

    for path in info.keys():
        if type(info[path]) == list:
            # level이 1이고 한줄일 경우, level 2 // recognition 무시 
            if (hparams.ignore_recognition_level == 1 and len(info[path]) == 1) or \
                    hparams.ignore_recognition_level == 2:
                    loss_coeff[path] = hparams.recognition_loss_coeff
            if(len(info[path])!=1 and hparams.ignore_recognition_level == 1 ):
                loss_coeff[path] = hparams.recognition_loss_coeff
                # print(info[path])
    '''
    ignore_description = {
        0: "use all",
        1: "ignore only unmatched_alignment",
        2: "fully ignore recognition",
    }


    print(" [!] Skip recognition level: {} ({})". \
            format(hparams.ignore_recognition_level,
                   ignore_description[hparams.ignore_recognition_level]))

    for audio_path, text in info.items():
        
        # text -> stt api output
        # print("audio_path = {} , text = {}".format(audio_path,text))
        # loss_coeff가 0.2가 나오는 이유는 hparams의 기본값이 나오는 것.
        # print('loss_coeff[audio_path]',loss_coeff[audio_path])

        # 탈락 될 recognition
        if hparams.ignore_recognition_level > 0 and loss_coeff[audio_path] != 1:

            continue

    

        if base_dir not in audio_path:
            audio_path = os.path.join(base_dir, audio_path)



        try:

            # text는 tokens의 정보 집합으로 들어간다.
            # char to id
            tokens = text_to_sequence(text)
            
        except:
            continue


        fn = partial(
                _process_utterance,
                audio_path, data_dir, tokens, loss_coeff[audio_path])
        futures.append(executor.submit(fn))
        

    n_frames = [future.result() for future in tqdm(futures)]
    n_frames = [n_frame for n_frame in n_frames if n_frame is not None]

    hours = frames_to_hours(n_frames)
    
    print(' [*] Loaded metadata for {} examples ({:.2f} hours)'.format(len(n_frames), hours))
    print(' [*] Max length: {}'.format(max(n_frames)))
    print(' [*] Min length: {}'.format(min(n_frames)))
    
    
    '''
    plot_n_frames(n_frames, os.path.join(
            base_dir, "n_frames_before_filter.png"))

    min_n_frame = hparams.reduction_factor * hparams.min_iters
    max_n_frame = hparams.reduction_factor * hparams.max_iters - hparams.reduction_factor

    n_frames = [n for n in n_frames if min_n_frame <= n <= max_n_frame]
    hours = frames_to_hours(n_frames)


    

    print(' [*] After filtered: {} examples ({:.2f} hours)'.format(len(n_frames), hours))
    print(' [*] Max length: {}'.format(max(n_frames)))
    print(' [*] Min length: {}'.format(min(n_frames)))

    plot_n_frames(n_frames, os.path.join(
            base_dir, "n_frames_after_filter.png"))

    '''
    

def plot_n_frames(n_frames, path):
    labels, values = list(zip(*Counter(n_frames).most_common()))

    values = [v for _, v in sorted(zip(labels, values))]
    labels = sorted(labels)

    indexes = np.arange(len(labels))
    width = 1

    fig, ax = plt.subplots(figsize=(len(labels) / 2, 5))

    plt.bar(indexes, values, width)
    plt.xticks(indexes + width * 0.5, labels)

    plt.tight_layout()
    plt.savefig(path)


def _process_utterance(audio_path, data_dir, tokens, loss_coeff):
    audio_name = os.path.basename(audio_path)

    filename = audio_name.rsplit('.', 1)[0] + ".npz"
    numpy_path = os.path.join(data_dir, filename)

    if not os.path.exists(numpy_path):
        wav = load_audio(audio_path)

        # wav파일을 spectrogram으로 만듦 
        try:
            linear_spectrogram = spectrogram(wav).astype(np.float32)
            mel_spectrogram = melspectrogram(wav).astype(np.float32)

        except:
            print('error with : ',audio_path)
            return None
        # .으로 끝나지 않으면
        if tokens[-2]!=75:
            tokens=np.append(tokens,[75])

        # audio data와 token저장
        data = {
            "linear": linear_spectrogram.T,
            "mel": mel_spectrogram.T,
            "tokens": tokens,
            "loss_coeff": loss_coeff,
        }

        n_frame = linear_spectrogram.shape[1]

        min_n_frame = hparams.reduction_factor * hparams.min_iters
        max_n_frame = hparams.reduction_factor * hparams.max_iters - hparams.reduction_factor

        # print(min_n_frame,max_n_frame)

        # 오디오 길이가 짧고 길거나, tokens가 적거나 둘 다 거나




        if not (min_n_frame <= n_frame <= max_n_frame and len(tokens) >= hparams.min_tokens):
            _data_split_log = open(data_split_log,'a')
            _data_split_log.write(str([audio_path,data["linear"].shape[0],len(tokens)]))
            _data_split_log.write('\n')
            _data_split_log.close()
                


        # 트레인에 사용되는 data만 npz파일로 저장한다.
        else:
            pass
        
        np.savez(numpy_path, **data, allow_pickle=False)
    else:
        try:
            data = np.load(numpy_path)
            n_frame = data["linear"].shape[0]
        except:
            remove_file(numpy_path)
            return _process_utterance(audio_path, data_dir, tokens, loss_coeff)

    return n_frame

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='spectrogram')

    parser.add_argument('metadata_path', type=str)
    parser.add_argument('--data_dirname', type=str, default="data_s2")
    parser.add_argument('--num_workers', type=int, default=None)

    config = parser.parse_args()
    build_from_path(config)
    
    print(config.data_dirname)
