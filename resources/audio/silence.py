import os
import re
import sys
import json
import librosa
import argparse
import numpy as np
from tqdm import tqdm
from glob import glob
from pydub import silence
from pydub import AudioSegment
from functools import partial

from hparams import hparams
from utils import parallel_run, add_postfix
from audio import load_audio, save_audio, get_duration, get_silence

def abs_mean(x):
    return abs(x).mean()


def read_audio(audio_path):
    return AudioSegment.from_file(audio_path)

def split_on_silence_with_pydub(
        audio_path, skip_idx=0, out_ext="wav",
        silence_thresh=-40, min_silence_len=400,
        silence_chunk_len=100, keep_silence=100):

    filename = os.path.basename(audio_path)
    # print('filename :',filename)
    target_audio_path='./datasets/moon_own/rs/'+filename
    if os.path.exists(target_audio_path):
        return None
        

    audio = read_audio(audio_path)
    not_silence_ranges = silence.detect_nonsilent(
        audio, min_silence_len=silence_chunk_len,
        silence_thresh=silence_thresh)

    try:
        edges = [not_silence_ranges[0]]


        for idx in range(1, len(not_silence_ranges)):
            cur_start = not_silence_ranges[idx][0]
            prev_end = edges[-1][1]

            if cur_start - prev_end < min_silence_len:
                edges[-1][1] = not_silence_ranges[idx][1]
            else:
                edges.append(not_silence_ranges[idx])

        print(edges)
       

        
        segment=0
        for idx, (start_idx, end_idx) in enumerate(edges[skip_idx:]):
            start_idx = max(0, start_idx - keep_silence)
            end_idx += keep_silence

        

            # segment+=audio[start_idx:end_idx]

            segment+=audio[start_idx:end_idx]
            

        segment.export(target_audio_path, out_ext)  # for soundsegment

    except:
        pass

    return None

def split_on_silence_batch(audio_paths, method, **kargv):
    audio_paths.sort()
    method = method.lower()


    if method == "pydub":
        fn = partial(split_on_silence_with_pydub, **kargv)

    parallel_run(fn, audio_paths,
            desc="Split on silence", parallel=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--audio_pattern', required=True)
    parser.add_argument('--out_ext', default='wav')
    config = parser.parse_args()

    audio_paths = glob(config.audio_pattern)

    split_on_silence_batch(
            audio_paths, 'pydub',
            out_ext=config.out_ext,
    )

# "권한는 공유하되 책임은 당대표가 혼자 지는 이런 기형적 구조가 결국 최근 4년 동안의 임기 2년의 야당 지도부 교체를 숫자를 늘려서 무려 10번이나 교체됐습니다.",