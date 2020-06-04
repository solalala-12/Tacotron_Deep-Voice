'''



나눔 글꼴 설치
apt-get 명령으로 나눔글꼴(fonts-nanum)을 설치하고, fc-cache 명령으로 폰트 캐시 삭제

$ sudo apt-get install fonts-nanum*
$ sudo fc-cache -fv
만일 다른 ttf 폰트를 가져왔다면 다음과 같이 복사하고, fc-cache 명령으로 폰트 캐시 삭제

$ sudo cp new_font.ttf /usr/share/fonts/
$ sudo fc-cache -fv
matplotlib 나눔 글꼴을 추가
나눔 글꼴을 matplotlib 에 복사하고, matplotlib의 폰트 캐시를 삭제

$ sudo cp /usr/share/fonts/truetype/nanum/Nanum* /usr/local/lib/python3.6/dist-packages/matplotlib/mpl-data/fonts/ttf/
$ rm -rf /home/ubuntu/.cache/matplotlib/*


$ sudo apt-get install python3-tk
'''


import tkinter
from matplotlib import font_manager, rc

font_fname = '/usr/share/fonts/truetype/nanum/NanumGothic.ttf'
font_name = font_manager.FontProperties(fname=font_fname).get_name()

rc('font', family=font_name)
print(font_name)

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


import numpy as np

data = np.random.randint(-100, 100, 50).cumsum()
data

plt.rcParams["font.family"] = 'NanumGothic'
plt.rcParams["font.size"] = 12
plt.rcParams['xtick.labelsize'] = 12.
plt.rcParams['ytick.labelsize'] = 12.
plt.rcParams["figure.figsize"] = (14,4)
plt.rcParams['axes.grid'] = True 
plt.rcParams['axes.unicode_minus'] = False

plt.title('가격의 변화')
plt.plot(range(50), data, 'r')
plt.show()