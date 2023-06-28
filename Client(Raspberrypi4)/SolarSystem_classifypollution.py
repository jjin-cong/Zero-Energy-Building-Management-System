#!/usr/bin/env python
# coding: utf-8

# In[1]:
#capture by picamera
import picamera
import time
import datetime


with picamera.PiCamera() as camera:
    camera.resolution = (512,512)
    camera.start_preview()
    time.sleep(5)
    camera.stop_preview()
    camera.capture('capture.jpg')
#


import os  

folder_path = '/home/pi/Desktop/project/TCP_client/'

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


# In[9]:


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


model = load_model('/home/pi/Desktop/project/pollution_classify_model.h5')

#1 값이 not-polluted, 0이 polluted
def model_predict(model,x):
    pred_labels = []
    
    image_var = tf.Variable(x,dtype = float)
    pred = model(image_var)
    
    pred.numpy()
    
    pred = np.where(pred>0,0,1)
    
    for i in range(len(pred)):
        if pred[i] == 2:
            pred_labels.append('damaged')
        elif pred[i] == 1:
            pred_labels.append('polluted')
        else:
            pred_labels.append('clean')
    
    return pred, pred_labels

print('Image name :')

path = most_recent_file
img = PIL.Image.open(path)
img = img.resize((160,160))
img = np.asarray(img)

img = img.reshape(1,160,160,3)

print(model_predict(model,img))


# In[7]:


model_predict(model,img)[1]


# In[ ]:




