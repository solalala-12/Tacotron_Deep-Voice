#-*-Encoding: UTF-8-*-#
#google API로 인식해서 recognition.json에 저장하는 파일
import io
import os
import json
import argparse
import numpy as np
from glob import glob
from functools import partial
import requests
from utils import parallel_run, remove_file, backup_file, write_json
from audio import load_audio, save_audio, resample_audio, get_duration
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types


def text_recognition(path, config):

    # data/1.wav -> data/1 .wav
    root, _ = os.path.splitext(path)
    # 저장될 path
    txt_path = root + '.txt'
    
    # file이 있는 경우 (코드 처음 실행이 아닐 시)
    if os.path.exists(txt_path):
        with open(txt_path) as f:
            # txt파일 json으로 load 
            out = json.loads(open(txt_path,encoding='utf-8').read())
            return out
    

    

    out = {}
    error_count = 0

    # temp_file 
    tmp_path = os.path.splitext(path)[0] + ".tmp.wav"
    
    while True:

        try:
            client = speech.SpeechClient()

            content = load_audio(
                    path, pre_silence_length=config.pre_silence_length,
                    post_silence_length=config.post_silence_length)

            max_duration = config.max_duration - \
                    config.pre_silence_length - config.post_silence_length
            audio_duration = get_duration(content)

            if audio_duration >= max_duration:
                print(" [!] Skip {} because of duration: {} > {}". \
                        format(path, audio_duration, max_duration))
                return {}

            # audio 파일 재구성 // resampling , .wav-->.tmp.wav
            content = resample_audio(content, config.sample_rate)
            save_audio(content, tmp_path, config.sample_rate)

            
            # audio file open
            with io.open(tmp_path, 'rb') as f:
                audio = types.RecognitionAudio(content=f.read())

            config = types.RecognitionConfig(
                    encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
                    sample_rate_hertz=config.sample_rate,
                    language_code='ko-KR')

            # stt 결과물
            response = client.recognize(config, audio)
            if len(response.results) > 0:
                alternatives = response.results[0].alternatives

                results = [alternative.transcript for alternative in alternatives]
                assert len(results) == 1, "More than 1 results: {}".format(results)
                # encode binary file
                #print("result--------------",results[0].encode('utf8'))
                out = { path: "" if len(results) == 0 else results[0] }
                # 저장은 한글파일로 돼야함.
                print(path, results[0].encode('utf8')) 
                break


            break
        except Exception as err:
            raise Exception("OS error: {0}".format(err))

            error_count += 1
            print("Skip warning for {} for {} times". \
                    format(path, error_count))

            if error_count > 5:
                break
            else:
                continue

    remove_file(tmp_path)
    # 존재하지 않을때만 // 
    if not os.path.exists(txt_path):

        with open(txt_path, 'w',encoding='utf-8') as f:
            json.dump(out, f, indent=2, ensure_ascii=False)
    
    return out

def text_recognition_batch(paths, config):
    paths.sort()

    # 결과를 저장할 dictionary
    results = {}

    # 한 파일식 text_recogniton 실행 
    items = parallel_run(
            partial(text_recognition, config=config), paths,
            desc="text_recognition_batch", parallel=True)
    for item in items:
        results.update(item)
    return results


if __name__ == '__main__':

    
    parser = argparse.ArgumentParser()
    parser.add_argument('--audio_pattern', required=True)
    # audio- script 쌍이 저장될 json파일
    parser.add_argument('--recognition_filename', default="recognition.json")
    parser.add_argument('--sample_rate', default=16000, type=int)
    parser.add_argument('--pre_silence_length', default=1, type=int)
    parser.add_argument('--post_silence_length', default=1, type=int)
    # The Audio duration property is used for returning the length of an audio.
    parser.add_argument('--max_duration', default=60, type=int)
    # parse 정보 
    config, unparsed = parser.parse_known_args()

    audio_dir = os.path.dirname(config.audio_pattern)

    # 첫 실행시 지워지지 않음
    for tmp_path in glob(os.path.join(audio_dir, "*.tmp.*")):
        remove_file(tmp_path)
    
    # raw autio file path 
    paths = glob(config.audio_pattern) # --audio_pattern "./datasets/son/audio/*.*.wav"
    results = text_recognition_batch(paths, config)

    base_dir = os.path.dirname(audio_dir)
    recognition_path = \
            os.path.join(base_dir, config.recognition_filename)

    if os.path.exists(recognition_path):
        backup_file(recognition_path)

    # recognition.json write
    write_json(recognition_path, results)
