# code based with https://k4keye.tistory.com/111

'''
0. 이전 동작 되돌리기 , 저장하기, 불러오기 추가
1. 코드 클리닝
'''

import pyautogui as m 
import time 
import sys 
import os
import numpy as np

Choice_arr = []
Mouse_L_X = [] 
Mouse_L_Y =[]
Mouse_time = []

# time.sleep() 설정
tmp=1

def Mouse_in(): 
    time_cnt = 3 
    while time_cnt: 
        print(str(time_cnt)+ '초 후에 원하는 구역의 좌표를 저장합니다.') 
        time_cnt -= 1 
        time.sleep(1) 
        
    x,y =m.position() 
    
    print('좌표 x : {} , y : {}'. format(x,y)) 
    Mouse_L_X.append(int(x)) 
    Mouse_L_Y.append(int(y)) 
    
    Mouse_time.append(tmp)

def Mouse_out(M_time_cnt): 
    i = Mouse_time[M_time_cnt] 
    time_cnt =0 
    
    time.sleep(i) 
    m.moveTo(Mouse_L_X[M_time_cnt],Mouse_L_Y[M_time_cnt])
    m.doubleClick() 
    time_cnt+=1 
    time.sleep(1) 
    return 0

def start(): 
    while True: 
        M_time_cnt = -1 
        
        for i in Choice_arr: 
            # 마우스 이동이였다면
            if i == '1' : 
                M_time_cnt += 1 
                Mouse_out(M_time_cnt) 
            else: break
        break
    return 

def main(): 
    global Choice_arr
    global Mouse_L_X
    global Mouse_L_Y
    global Mouse_time
    

    while True: 
        print(' ** 현재까지 {} 개의 동작 '.format(len(Choice_arr)))
        Choice = input("1.마우스 이동/클릭 2.시작 3.이전 동작 되돌리기 4. 저장하기 5. 불러오기 6. 종료 : ") 
        print(Choice) 
   

        Choice_arr.append(Choice)
        if Choice == '1' :
            Mouse_in() 

        elif Choice == '2' : 
            print( ' {} 개의 동작' .format(len(Mouse_L_X)))
            print("start!!")
            start()
            continue

        # 이전 동작 되돌리기 
        elif Choice == '3':
            Mouse_L_X.pop()
            Mouse_L_Y.pop()
            Choice_arr.pop()

        # 현재까지의 history를 numpy로 저장합니다.
        elif Choice == '4':
            np.savez('history',Choice_arr,Mouse_L_X,Mouse_L_Y,Mouse_time)

        # 저장된 history를 로드하여 매크로를 실행합니다.
        elif Choice == '5':
            Choice_arr = np.load('history.npz')['arr_0']
            Mouse_L_X = np.load('history.npz')['arr_1']
            Mouse_L_Y = np.load('history.npz')['arr_2']
            Mouse_time = np.load('history.npz')['arr_3']
            print( '{} 개의 동작' .format(len(Mouse_L_X)))
            print("start!!")
            start()

        elif Choice == '6':
            print('종료합니다.')
            break
            



if __name__ == '__main__' : 
    main()