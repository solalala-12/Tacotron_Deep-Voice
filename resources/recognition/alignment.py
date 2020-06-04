# -*- coding: utf-8 -*-
import os
import string
import argparse
import operator
from functools import partial
from difflib import SequenceMatcher

from audio.get_duration import get_durations
from text import remove_puncuations, text_to_sequence
from utils import load_json, write_json, parallel_run, remove_postfix, backup_file

'''

한문장씩 자른 단어들을 원래 asset에서 가장 유사한 문장을 찾아내고 score로 거른다.
일정 score이상으로 추출된 text들이 -> found_text

found_text와 recognition_text를 비교하며 최적의 text를 return 한다.

recog : 돼지 젖 차에 갑자기 돌 이름 두 글자로 사용하는 단어는 흔히 저녁에 강하다는 의미를 오시죠
found =>  돼지 저 자에 갑자기 돌 자를 사용하는 이 단어는 흔히 추진력이 강하다는 의미로 쓰이죠. // 전체 script에서 받아온 원본
optimal ==> 돼지 저 자에 갑자기 돌 자를 사용하는 이 단어는 흔히 추진력이 강하다는 의미로 쓰이죠.



'''

def plain_text(text):
    return "".join(remove_puncuations(text.strip()).split())
    #join: 리스트를 특정 구분자를 포함해 문자열로 변환
    #remove_puncuations: 문장부호 제거
    #plain_text: 그 대사들에서 문장부호 제거하고 문자열로 바꿔주는 플레인한 텍스트 얻어내는 부분//? 
def add_punctuation(text):
    if text.endswith('다'): #특정 문자열로 끝나는거 찾음.
        return text + "." # '다'로 끝나면 text뒤에다가 점 붙여주는 부분
    else:
        return text

def similarity(text_a, text_b):
    text_a = plain_text(text_a)
    text_b = plain_text(text_b)

    score = SequenceMatcher(None, text_a, text_b).ratio()
    return score

def first_word_combined_words(text):
    words = text.split()
    if len(words) > 1:
        first_words = [words[0], words[0]+words[1]]
    else:
        first_words = [words[0]]
    return first_words

def first_word_combined_texts(text): #문장의 처음인지를 알아내려고 하는 부분...?
    words = text.split() #split() 문자형 분할.
    if len(words) > 1:
        # 단어가 2개 이상이면 
        if len(words) > 2:
            # 앞의 두 단단어만 붙이고 나머지 정상 유지 
            text2 = " ".join([words[0]+words[1]] + words[2:])
        else:
            text2 = words[0]+words[1]
        texts = [text, text2]
    else:
        texts = [text]
    return texts

# 단어들만 비교하는 알고리즘 // stt output 앞/뒤 단어가 found에 있으면 found / 없으면 stt 쓰겠다. 
# 찾는 과정에서 단어가 계속 인식이 안되면 found를 줄여나가며 탐색

def search_optimal(found_text, recognition_text):
    # 1. found_text is usually more accurate
    # 2. recognition_text can have more or less word


    #  print('found_text, recognition_text',found_text, recognition_text)
    optimal = None
    # 아예 두 문장이 같거나 recogition_text가 found_text에 포함되면
    if plain_text(recognition_text) in plain_text(found_text):
        optimal = recognition_text

    # optimal = found_text
    else:
        found = False
        for tmp_text in first_word_combined_texts(found_text):
            print("tmp_text :",tmp_text)
            # first_word_combined_words / [아버지],[아버지가방]
            for recognition_first_word in first_word_combined_words(recognition_text):
                # print('recognition_first_word : ',recognition_first_word)
                # print('found :',found)
                # found text에 recogntion 첫글자가 있다면
                if recognition_first_word in tmp_text:
                    start_idx = tmp_text.find(recognition_first_word)
                    # print('start_idx :',start_idx)
                    if tmp_text != found_text:
                        # 앞에꺼 자름 맞는 단어 찾아 갈 때 까지 ! 
                        # print('found_text',found_text)
                        found_text = found_text[max(0, start_idx-1):].strip()
                        print('found_text2',found_text)
                        
                    else:
                        
                        found_text = found_text[start_idx:].strip()
                    found = True
                    break
                # print('found_text', found_text)

            if found:
                break

        recognition_last_word = recognition_text.split()[-1] # 문자열 분할한거에서 가장 뒤에 것 -> 가장 마지막 word
        if recognition_last_word in found_text:
            end_idx = found_text.find(recognition_last_word)
            # print('recognition_last_word :',recognition_last_word)
            # print('end_idx :',end_idx)
            punctuation = ""
            # found_text길이가 더 길면 
            if len(found_text) > end_idx + len(recognition_last_word):
                # 남은 부분 공백으로 채워넣겠다.
                punctuation = found_text[end_idx + len(recognition_last_word)]
                if punctuation not in string.punctuation:
                    punctuation = ""

            print(found_text[:end_idx] + recognition_last_word + punctuation)
            found_text = found_text[:end_idx] + recognition_last_word + punctuation
            found = True

        if found:
            optimal = found_text
        
        print('optimal',optimal)

    return optimal


def align_text_fn(
        item, score_threshold, debug=False):

    # item / path , regonition 결과물 

    audio_path, recognition_text = item

    audio_dir = os.path.dirname(audio_path)
    base_dir = os.path.dirname(audio_dir)

    news_path = remove_postfix(audio_path.replace("audio", "assets")) 
    news_path = os.path.splitext(news_path)[0] + ".txt"
    # ./datasets/son/assets/NB10584578.txt
    strip_fn = lambda line: line.strip().replace('"', '').replace("'", "")
    candidates = [strip_fn(line) for line in open(news_path, encoding='utf-8').readlines()]
    # assets file 1개에 있는 모든 문장 
    # print('candidate : ',candidates)
    # print('recognition_text :' ,recognition_text)


    scores = { candidate: similarity(candidate, recognition_text) \
                    for candidate in candidates}

  

    # 가장 score가 높은 문장 sort
 
    sorted_scores = sorted(scores.items(), key=operator.itemgetter(1))[::-1]

    first, second = sorted_scores[0], sorted_scores[1]
    # print('recognition_text first, second',recognition_text,first, second)
    '''
    recognition_text first, second 잠시 후에 문희상 비대위원장을 수지에서 만나게 ('잠시 뒤 문희상 비대위원장을 스튜디오에서 만나겠습니다.', 0.6818181818181818) ('난파 직전의 새정치연합을 책임 
    지게 된 문희상 비대위원장이 이런 말을 했습니다.', 0.33962264150943394)
    '''

    # 문장의 유사도가 score_threshold보다 높으면 
    if first[1] > second[1] and first[1] >= score_threshold:

        found_text, score = first
        aligned_text = search_optimal(found_text, recognition_text)

        if debug:
            print("   ", audio_path)
            print("   ", recognition_text)
            print("=> ", found_text)
            print("==>", aligned_text)
            print("="*30)

        if aligned_text is not None:
            result = { audio_path: add_punctuation(aligned_text) }
            # 둘 차이가 너무 크면 
        elif abs(len(text_to_sequence(found_text)) - len(text_to_sequence(recognition_text))) > 10:
            result = {}
        else:
            # 두개 다 넣음.
            result = { audio_path: [add_punctuation(found_text), recognition_text] }
    else:
        result = {}

    
    # script 와 recognition의 차이가 크거나, 유사도 높은 문장을 원본에서 못 찾았다면.
    if len(result) == 0:
        result = { audio_path: [recognition_text] }

    return result

def align_text_batch(config):
    align_text = partial(align_text_fn,
            score_threshold=config.score_threshold)

    results = {}
    data = load_json(config.recognition_path, encoding=config.recognition_encoding)

    items = parallel_run(
            align_text, data.items(), # data.items() = google stt 결과물
            desc="align_text_batch", parallel=True)

    for item in items:
        results.update(item)

    # results 의 values값이 String인 형태만 count
    found_count = sum([type(value) == str for value in results.values()])
    # results / data -> 살아남은 문장들 / 원래 문장
    print(" [*] # found: {:.5f}% ({}/{})".format(
            len(results)/len(data), len(results), len(data)))
    print(" [*] # exact match: {:.5f}% ({}/{})".format(
            found_count/len(items), found_count, len(items)))

    return results

if __name__ == '__main__':
    parser = argparse.ArgumentParser() #파이썬 인자값 추가하기
    # recognition.json
    parser.add_argument('--recognition_path', required=True)
    # alignment.json (생성될 파일)
    parser.add_argument('--alignment_filename', default="alignment.json")
    parser.add_argument('--score_threshold', default=0.4, type=float)
    parser.add_argument('--recognition_encoding', default='utf8')
    config, unparsed = parser.parse_known_args()

    results = align_text_batch(config)

    base_dir = os.path.dirname(config.recognition_path)
    alignment_path = \
            os.path.join(base_dir, config.alignment_filename)

    if os.path.exists(alignment_path):
        backup_file(alignment_path)

    write_json(alignment_path, results)
    duration = get_durations(results.keys(), print_detail=False)
