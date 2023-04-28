# 🤓👉*HOW TO RUN !* 


# 1. Docker 실행

## 1-1. Google STT API 가입 (Speech API Key 받기)

API key ) https://webnautes.tistory.com/1247 <br>

Google cloud sdk / Ubuntu OS용 설치 ) https://cloud.google.com/sdk/docs/quickstart-debian-ubuntu

# 2. Google STT API 사용을 위한 환경변수 설정

```Bash
export GOOGLE_APPLICATION_CREDENTIALS="YOUR-GOOGLE.CREDENTIALS.json"
```
# 3. Install packages

```Bash
python3 -c "import nltk; nltk.download('punkt')"
```
- matplot관련 library설치
```
sudo apt-get install python3-tk
```

# 4. Data Download from Azure

- shell 에서 다음 명령어 실행 / Azure key

```
export AZURE_STORAGE_CONNECTION_STRING="DefaultEndpointsProtocol=https;AccountName={AccountName};AccountKey={AccountKey}==;EndpointSuffix=core.windows.net"

```

- download할 데이터 명 argparse에 정의
```
python3 download.py --data_name=kg
```


# 5. Train data Download

- 손석희 데이터의 경우 video에서 audio, script가 쌍으로 받아와짐 (Crawling)

-   Script XML 예시 ) http://nsvc.jtbc.joins.com/API/News/Newapp/Default.aspx/?NJC=NJC400&NID=NB11515152&CD=A0100

```Bash
python3 -m datasets.son.download
```

# 6. Data Preprocessing

- python pydub 라이브러리를 이용한 무음 기준으로 데이터 분할 (40 데시벨 이하)

```Bash
python3 -m audio.silence --audio_pattern "./datasets/son/audio/*.wav" 
```
- wav-script 쌍 json파일 형식 <br>

    ex) "./datasets/YOUR_DATASET/audio/001.mp3": "My name is Taehoon Kim.",
```Bash
python3 -m recognition.google --audio_pattern "./datasets/son/audio/*.*.wav"
```

- STT API 결과물과 실제 Script를 비교하여 accuracy score가 높은 문장만 선택

```Bash
python3 -m recognition.alignment --recognition_path "./datasets/son/recognition.json" --score_threshold=0.5
```
- Train에 사용될 데이터 생성(변환) / .npz파일 생성 
```Bash
python3 -m datasets.generate_data ./datasets/YOUR_DATASET/alignment.json
```

# 7. Training Model
`hparams.py` -> 모델 파라미터 저장된 곳

1) Single speaker
```
python3 train.py --data_path=datasets/son
```

2) multi speaker 
```
# after change `model_type` in `hparams.py` to `deepvoice` or `simple`
python3 train.py --data_path=datasets/son,datasets/moon,datasets/park

python3 train.py --data_path=datasets/son_own_slience
```

* 모델 이어서 학습시 train log 지정  <br>


```
python3 train.py --data_path=datasets/son --load_path logs/son-20171015 
```

# 8. Synthesize audio (Griffin-Lim reconstruction)

You can train your own models with:

```
python3 app.py --load_path logs/son-20171015 --num_speakers=1

```

or generate audio directly with:

```

python3 synthesizer.py --load_path logs/son_own_slience_2_40_2020-05-28_17-42-56 --text "완벽하게 정의롭진 않지만 거친 현장의 밑바닥을 치열하게 지켜내는 모습에."
python3 synthesizer.py --load_path logs/son+moon+park_2020-03-04_17-35-03 --text "이거 실화냐?" --num_speakers=3 --speaker_id=1  
```
# 9. Files in folder upload to Azure and remove
- Azure에 업로드와 동시에 현재 경로에서 파일 삭제
- 삭제를 원하지 않을 땐 --rm_log=False로 수정

```
python3 upload.py --folder_name=logs/son_jin --rm_log==True (default)
```




#### code with
- [Sora](https://github.com/solalala-12)
- [hizzang](https://github.com/hizzang920)
- [YooSungHyun](https://github.com/YooSungHyun)
- [jimjimi](https://github.com/jimjimi)
