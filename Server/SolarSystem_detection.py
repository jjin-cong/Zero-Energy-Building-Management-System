#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
import os
import time
import random
import matplotlib.pyplot as plt 
import seaborn as sns
import PIL
import cv2
import pickle
import numpy as np
import matplotlib.pyplot as plt
import numpy as np
import os
import tensorflow as tf
import tensorflow.keras.layers as tfl

from tensorflow.keras.preprocessing import image_dataset_from_directory
from tensorflow.keras.layers.experimental.preprocessing import RandomFlip, RandomRotation

from keras.models import load_model

import socket
import sys
import os

import pymysql

from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True

def model_predict(model,x):
    pred_labels = []
    
    image_var = tf.Variable(x,dtype = float)
    pred = model(image_var)
    
    pred = np.argmax(pred,axis =1)
    
    for i in range(len(pred)):
        if pred[i] == 2:
            pred_labels.append('damaged')
        elif pred[i] == 1:
            pred_labels.append('polluted')
        else:
            pred_labels.append('No problem')
    
    return pred, pred_labels

def classify_pollution(model_path,most_recent_file,file_name):
    model = load_model(model_path + '/pollution_classify_model.h5')
    
    path = most_recent_file
    img = PIL.Image.open(path)
    img = img.resize((160,160))
    img = np.asarray(img)

    img = img.reshape(1,160,160,3)
    
    classify_result = model_predict(model,img)[-1]
    
    print(model_predict(model,img)[-1])
    
    return classify_result[0]

def detect_pollution(darknet_path,file_name):
    os.chdir(darknet_path)
    os.system(darknet_path + 'darknet detector test data/obj.data testcfg/yolov3.cfg backup/yolov3_final.weights backup/' + file_name + ' -show imShow(preditions.jpg)')
    print('bounding img created !')


# In[2]:


def capture(filename,port):
    
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('', port))       # ip주소, 포트번호 지정
    server_socket.listen(0)                          # 클라이언트의 연결요청을 기다리는 상태

    client_socket, addr = server_socket.accept()     # 연결 요청을 수락함. 그러면 아이피주소, 포트등 데이터를 return

    print('연결 시작')

    client_socket.send(filename.encode())

    print('파일 이름 전송 완료')

    data = client_socket.recv(1024)                 # 클라이언트로 부터 데이터를 받음. 출력되는 버퍼 사이즈. (만약 2할 경우, 2개의 데이터만 전송됨)

    data_transferred = 0

    if not data:
        print('파일 %s 가 서버에 존재하지 않음' %filename)
        sys.exit()

    nowdir = os.getcwd()

    with open('C:/darknet-master/build/darknet/x64/backup/'+filename, 'wb') as f: #현재dir에 filename으로 파일을 받는다
        try:
            #client_socket.settimeout(3)
            while True: #데이터가 있을 때까지
                f.write(data) #1024바이트 쓴다

                data = client_socket.recv(1024) #1024바이트를 받아 온다

                if not data:
                    break        
            
        except Exception as ex:
            print(ex)

    print('파일 %s 받기 완료.' %(filename))

    server_socket.close()


# In[3]:


print('Problem ? : ')
problem_power_generation = int(input())


# In[4]:


if problem_power_generation == 1:
    capture('capture.jpg',8888)
    
    folder_path = 'C:/darknet-master/build/darknet/x64/backup/'
    
    # each_file_path_and_gen_time: 각 file의 경로와, 생성 시간을 저장함
    each_file_path_and_gen_time = []
    for each_file_name in os.listdir(folder_path):
        # getctime: 입력받은 경로에 대한 생성 시간을 리턴
        each_file_path = folder_path + each_file_name
        each_file_gen_time = os.path.getctime(each_file_path)
        each_file_path_and_gen_time.append(
            (each_file_path, each_file_gen_time)
        )

    # 가장 생성시각이 큰(가장 최근인) 파일을 리턴 
    most_recent_file = max(each_file_path_and_gen_time, key=lambda x: x[1])[0]
    file_name = most_recent_file.split('/')[-1]
    
    print(file_name)
    
    model_path = 'C:/Users/jlee0/Desktop/KYU/hanim ict/탄소중립 항만/개발'
    most_recent_file = most_recent_file
    file_name = file_name
    
    classify_result = classify_pollution(model_path,most_recent_file,file_name)
    
    #DB로 패널 상태 전송
    con = pymysql.connect(host='jtlee-home.iptime.org', port = 10122, user='inventist', password='bems',
                       db='mysql', charset='utf8')
    cur = con.cursor()
    cur.execute("INSERT INTO BEMS(panel_mal) VALUE (%s)",(classify_result))
    con.commit()
    # STEP 5: DB 연결 종료
    con.close()
    
    if classify_result == 'polluted':
        darknet_path = 'C:/darknet-master/build/darknet/x64/'
        file_name = file_name
        detect_pollution(darknet_path,file_name) 
        #darknet_path 경로에 predictions.jpg가 생성되었다.
    elif classify_result == 'damaged':
        darknet_path = 'C:/darknet-master/build/darknet/x64/'
        file_name = file_name
        detect_pollution(darknet_path,file_name) 
        #darknet_path 경로에 predictions.jpg가 생성되었다.
    else:
        print('Temporary problem')
else:
    print('Power generator is fine')


# In[ ]:





# In[ ]:




