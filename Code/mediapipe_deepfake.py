# -*- coding: utf-8 -*-
"""MediaPipe-DeepFake.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1JEyaEdXcT7nrJCXZhhF0HTQqRMevu_jN
"""

!pip install mediapipe

import pandas as pd
import numpy as np
import PIL
from PIL import Image
import mediapipe as mp
import cv2
import os

from matplotlib import pyplot as plt

from google.colab.patches import cv2_imshow

import dlib
from skimage import io
import matplotlib.pyplot as plt
from numpy import asarray

from google.colab import drive
drive.mount('/content/drive')

imgPath=[]
resize= 1
frame_count_real = []
frame_count_fake = []


# Function to extract frames
def FrameCapture(path,globalCount,type_dataset,label):
    frame_count=[]
    imgPath = []
    temp = 0
    v_cap = cv2.VideoCapture(path)
    v_len = int(v_cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    # Pick 'n_frames' evenly spaced frames to sample
    sample = np.linspace(0, v_len - 1, n_frames).astype(int) #Index in sample array are the frames which will be extracted.

    # Loop through frames
    
    frames = []
    for j in range(v_len):
        success = v_cap.grab()
        if j in sample:
            # Load frame
            success, frame = v_cap.read()
            if not success:
                
                continue
           
            frame = Image.fromarray(frame)
            
            # Resize frame to desired size
            if resize is not None:
                frame = frame.resize([int(d * resize) for d in frame.size])
                frame = np.asarray(frame)
            frames.append(frame)
    
    # Used as counter variable
  
    # checks whether frames were extracted
    count = globalCount
    currentCount = 0
    success = 1
  
    while success and currentCount<min(n_frames,len(frames)):
  

        cv2.imwrite("All_Images/" + str(type_dataset) + "_"+ str(label) + "_frame%d.jpg" % (count//n_frames),frames[int(currentCount)])

        imgPath.append("All_Images/" + str(type_dataset) + "_"+ str(label) + "_frame%d.jpg"%(count//n_frames))
  
        count += n_frames
        currentCount += 1
      
    if(type_dataset!="Train"):
      frame_count.append(currentCount)

    return imgPath,count,frame_count

import os


n_frames = 32
resize= 1

def captureFrame(type_dataset,label):
  imgPath = []
  frame_count = []
  count = 0
  video_label=[]
  temp = True
  if temp:
    for file in os.listdir("/content/drive/MyDrive/Deepfake_Mix/"+str(type_dataset)+"/"+str(label)):
        path=os.path.join("/content/drive/MyDrive/Deepfake_Mix/"+str(type_dataset)+"/"+str(label), file)
        temp , count ,x= FrameCapture(path,count,type_dataset,label)
        imgPath = imgPath +  temp
        if (type_dataset != 'Train'):
          frame_count.append(x[0])
          if label=='Fake':
            video_label.append(0)
          else:
            video_label.append(1)
  else:
    for file in os.listdir("/content/drive/MyDrive/Deepfake_Mix_Half/"+str(type_dataset)+"/"+str(label)):
        path=os.path.join("/content/drive/MyDrive/Deepfake_Mix_Half/"+str(type_dataset)+"/"+str(label), file)
        temp , count ,x= FrameCapture(path,count,type_dataset,label)
        imgPath = imgPath +  temp
        if (type_dataset != 'Train'):
          frame_count.append(x[0])
          if label=='Fake':
            video_label.append(0)
          else:
            video_label.append(1)
  return imgPath,frame_count,video_label

imgPath_train_fake,  frame_count_train_fake, _= captureFrame("Train","Fake")
imgPath_train_real,  frame_count_train_real, _= captureFrame("Train","Real")
imgPath_val_fake,  frame_count_val_fake, video_label_val_fake= captureFrame("Val","Fake")
imgPath_val_real,  frame_count_val_real, video_label_val_real= captureFrame("Val","Real")
imgPath_test_fake,  frame_count_test_fake, video_label_test_fake= captureFrame("Test","Fake")
imgPath_test_real,  frame_count_test_real, video_label_test_real= captureFrame("Test","Real")

print(imgPath_train_fake)
print(imgPath_train_real)
print(imgPath_val_fake)
print(imgPath_val_real)
print(imgPath_test_fake)
print(imgPath_test_real)

"""# MediaPipe"""

mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils

mp_face_detection

def faceDetect_MediaPipe(type_dataset,label,imgPath,frame):
  # For static images:
  count=0
  processedImagePath_mediapipe=[]

  j = 0
  k = 0


  with mp_face_detection.FaceDetection(
      min_detection_confidence=0.5) as face_detection:

    for i in range(len(imgPath)):

      if(type_dataset != "Train"):
         if(j > frame[k]):
           k += 1
           j = 0

      file = imgPath[i]

      image = PIL.Image.open(file)
      d1, d2 = image.size
      
      image = cv2.imread(file)
      

      # Convert the BGR image to RGB and process it with MediaPipe Face Detection.
      results = face_detection.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

      # Draw face detections of each face.
      if not results.detections:
        if(type_dataset != "Train"):
            frame[k] -=1
        continue
      annotated_image = image.copy()
      
      for detection in results.detections:
        
        
        
        x,y,w,h = detection.location_data.relative_bounding_box.xmin,detection.location_data.relative_bounding_box.ymin,detection.location_data.relative_bounding_box.width,detection.location_data.relative_bounding_box.height
        x,y,w,h = int(x*d1),int(y*d2),int(w*d1),int(h*d2)
        crop_img = annotated_image[y:y+h, x:x+w]
        resize_face = cv2.resize(crop_img,(64, 64), interpolation=cv2.INTER_CUBIC)
        

        info = mp_face_detection.FaceDetection()
        x = info.process(image=image)
        

        
        cv2.imwrite("MediaPipe" + "_" + str(type_dataset) + "_" + str(label) + "/mediapipe%d.jpg" % count,resize_face)
        
        processedImagePath_mediapipe.append("MediaPipe" + "_" + str(type_dataset) + "_" + str(label) + "/mediapipe%d.jpg"%count)
        count+=1

        j+=1

        

  return processedImagePath_mediapipe,frame

processedImagePath_Train_Fake_mediapipe , _ = faceDetect_MediaPipe("Train","Fake",imgPath_train_fake,[])

processedImagePath_Train_Real_mediapipe , _ = faceDetect_MediaPipe("Train","Real",imgPath_train_real,[])

print(processedImagePath_Train_Fake_mediapipe)
print(processedImagePath_Train_Real_mediapipe)

processedImagePath_Test_Fake_mediapipe , frame_count_test_fake = faceDetect_MediaPipe("Test","Fake",imgPath_test_fake,frame_count_test_fake)

processedImagePath_Test_Real_mediapipe , frame_count_test_real = faceDetect_MediaPipe("Test","Real",imgPath_test_real , frame_count_test_real)

print(processedImagePath_Test_Fake_mediapipe)
print(processedImagePath_Test_Real_mediapipe)

print(len(processedImagePath_Test_Fake_mediapipe))
print(len(processedImagePath_Test_Real_mediapipe))
print(sum(frame_count_test_fake),sum(frame_count_test_real))

processedImagePath_Val_Fake_mediapipe , frame_count_val_fake = faceDetect_MediaPipe("Val","Fake",imgPath_val_fake,frame_count_val_fake)

processedImagePath_Val_Real_mediapipe , frame_count_val_real = faceDetect_MediaPipe("Val","Real",imgPath_val_real,frame_count_val_real)

"""#Data Augmentation"""

from torchvision import datasets
from torch.utils.data import DataLoader
from torchvision.utils import save_image
from skimage.util import random_noise
import numpy as np
import torch
import matplotlib.pyplot as plt
import torchvision.transforms as transforms
import argparse

import numpy as np
import os
import cv2

def noisy(noise_typ,image):
  if noise_typ == "gauss":
    mean = 0
    var = 100
    sigma = var ** 0.5
    row, col, _ = image.shape
    gaussian = np.random.normal(mean, sigma, (row, col)) 

    noisy = np.zeros(image.shape, np.float32)

    if len(image.shape) == 2:
        noisy = image + gaussian
    else:
        noisy[:, :, 0] = image[:, :, 0] + gaussian
        noisy[:, :, 1] = image[:, :, 1] + gaussian
        noisy[:, :, 2] = image[:, :, 2] + gaussian

    cv2.normalize(noisy, noisy, 0, 255, cv2.NORM_MINMAX, dtype=-1)
    noisy = noisy.astype(np.uint8)
    return noisy
  elif noise_typ == "s&p":
    row,col,ch = image.shape
    s_vs_p = 0.5
    amount = 0.05
    out = np.copy(image)
    # Salt mode
    num_salt = np.ceil(amount * image.size * s_vs_p)
    coords = [np.random.randint(0, i - 1, int(num_salt)) for i in image.shape]
    out[coords] = 1

    # Pepper mode
    num_pepper = np.ceil(amount* image.size * (1. - s_vs_p))
    coords = [np.random.randint(0, i - 1, int(num_pepper)) for i in image.shape]
    out[coords] = 0
    return out

  
  
  elif noise_typ =="speckle":
    row,col,ch = image.shape
    gauss = np.random.randn(row,col,ch)
    gauss = gauss.reshape(row,col,ch)
    noisy = image + image * gauss
    return noisy

def create_noisy_img(face_detector,face_detector_arr,type_dataset,label):
    arr=[]
    for i in range(len(face_detector_arr)):
        img=cv2.imread(face_detector_arr[i])
        if face_detector!="MediaPipe":
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        noisy_img = noisy("gauss", img)
        noisy_img = cv2.resize(noisy_img, (64, 64))
        
        cv2.imwrite("/content/MediaPipe_"+type_dataset+"_"+label+"_Noise/mediapipe_noise%d.jpg" % i,noisy_img)
        arr.append("/content/MediaPipe_"+type_dataset+"_"+label+"_Noise/mediapipe_noise%d.jpg"%i)
    return arr

processedImagePath_Train_Fake_mediapipe_noise=create_noisy_img("MediaPipe",processedImagePath_Train_Fake_mediapipe,"Train","Fake")

processedImagePath_Train_Real_mediapipe_noise=create_noisy_img("MediaPipe",processedImagePath_Train_Real_mediapipe,"Train","Real")

"""# Training"""

from sklearn.metrics import accuracy_score
from sklearn.metrics import f1_score
from sklearn.metrics import log_loss
from skimage.color import rgb2grey
from skimage.feature import hog

def create_features(img):
    
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    features=[]
    for i in gray:
      for j in i:
        features.append(j)
    
    return features

def createFeatureDatabase(real_list, fake_list):
  train=[]
  label = []

  

  for i in range(len(fake_list)):
    img = cv2.imread(fake_list[i])
    tmp_features = create_features(img)
    train.append(tmp_features)
    label.append(0)

  for i in range(len(real_list)):
    img = cv2.imread(real_list[i])
    tmp_features = create_features(img)
    train.append(tmp_features)
    label.append(1)

  
  return train,label

train_data,label_data = createFeatureDatabase(processedImagePath_Train_Real_mediapipe,processedImagePath_Train_Fake_mediapipe)

len(train_data)

test_data, test_label = createFeatureDatabase(processedImagePath_Test_Real_mediapipe,processedImagePath_Test_Fake_mediapipe)

train_data_noise,label_data_noise = createFeatureDatabase(processedImagePath_Train_Real_mediapipe_noise,processedImagePath_Train_Fake_mediapipe_noise)

len(label_data_noise)

len(label_data)

"""## Standard Scaler"""

from sklearn.preprocessing import StandardScaler  
scaler = StandardScaler()  

scaler.fit(train_data)  
train_data_ss = scaler.transform(train_data)  

test_data_ss = scaler.transform(test_data)

from sklearn.preprocessing import StandardScaler  
scaler = StandardScaler()  

scaler.fit(train_data_noise)  
train_data_ss_noise = scaler.transform(train_data_noise)  

test_data_ss = scaler.transform(test_data)

"""## LDA"""

from sklearn.discriminant_analysis import LinearDiscriminantAnalysis

lda = LinearDiscriminantAnalysis()
lda_train_data = lda.fit_transform(train_data_ss, label_data)

lda_test_data=lda.transform(test_data_ss)

lda.explained_variance_ratio_

lda_train_data

len(lda_train_data[0])

"""## PCA"""

from sklearn.decomposition import PCA
pca = PCA(0.99)
pca_train_data=pca.fit_transform(train_data_ss)

pca_train_data

len(pca_train_data)

pca_train_data_noise=pca.transform(train_data_ss_noise)

len(pca_train_data_noise)

pca_test_data=pca.transform(test_data_ss)

pca.explained_variance_ratio_

pca_train_data_noise

"""# DeepFake Result"""

def predictDeepFakeResult(predicted_test,frame_count_test):
  k=0
  prediction=[]
  len1=len(predicted_test)
  for i in frame_count_test:
    real_count=0
    fake_count=0
    
    for j in range(i):
      if predicted_test[k]==1:
        real_count+=1
      else:
        fake_count+=1
      k+=1
    if real_count>fake_count:
      prediction.append(1)
    else:
      prediction.append(0)
  return prediction

actual_test_label=video_label_test_fake+video_label_test_real

"""## SVC"""

from sklearn.svm import SVC
from sklearn.model_selection import cross_val_score

def trainSVC(train_data, label_data, test_data,test_label):
  model = SVC()
  
  model.fit(train_data,label_data)
  print(model.score(test_data,test_label))
  cvs = cross_val_score(model, train_data, label_data, cv=5)
  print(cvs)
  
  predicted_test = model.predict(test_data)
  return predicted_test,cvs

"""## SVC_LDA"""

predicted_test_SVC_lda,cvs_SVC_lda=trainSVC(lda_train_data,label_data,lda_test_data,test_label)
predicted_test_SVC_lda

print(len(predicted_test_SVC_lda))

pred_SVC_lda=predictDeepFakeResult(predicted_test_SVC_lda,frame_count_test_fake+frame_count_test_real)
print(pred_SVC_lda)

accuracy_score(actual_test_label, pred_SVC_lda)

f1_score(actual_test_label, pred_SVC_lda)

log_loss(actual_test_label,pred_SVC_lda)

"""## SVC_PCA"""

predicted_test_SVC_pca,cvs_SVC_pca=trainSVC(pca_train_data,label_data,pca_test_data,test_label)
predicted_test_SVC_pca

pred_SVC_pca=predictDeepFakeResult(predicted_test_SVC_pca,frame_count_test_fake+frame_count_test_real)
print(pred_SVC_pca)

accuracy_score(actual_test_label, pred_SVC_pca)

f1_score(actual_test_label, pred_SVC_pca)

log_loss(actual_test_label,pred_SVC_pca)

pca_train_add=[]
for i in pca_train_data:
  pca_train_add.append(i)
for i in pca_train_data_noise:
  pca_train_add.append(i)

predicted_test_SVC_pca_noise,_=trainSVC(pca_train_add,label_data+label_data_noise,pca_test_data,test_label)
predicted_test_SVC_pca_noise

pred_SVC_pca_noise=predictDeepFakeResult(predicted_test_SVC_pca_noise,frame_count_test_fake+frame_count_test_real)
print(pred_SVC_pca_noise)

accuracy_score(actual_test_label, pred_SVC_pca_noise)

f1_score(actual_test_label, pred_SVC_pca_noise)

log_loss(actual_test_label,pred_SVC_pca_noise)

"""##SVC_Normal"""

predicted_test_SVC_normal,cvs_SVC_normal=trainSVC(train_data,label_data,test_data,test_label)
predicted_test_SVC_normal

pred_SVC_normal=predictDeepFakeResult(predicted_test_SVC_normal,frame_count_test_fake+frame_count_test_real)
print(pred_SVC_normal)

accuracy_score(actual_test_label, pred_SVC_normal)

f1_score(actual_test_label, pred_SVC_normal)

log_loss(actual_test_label,pred_SVC_normal)

train_data_add=[]
for i in train_data:
  train_data_add.append(i)
for i in train_data_noise:
  train_data_add.append(i)

predicted_test_SVC_normal_noise,_=trainSVC(train_data_add,label_data+label_data_noise,test_data,test_label)
predicted_test_SVC_normal_noise

pred_SVC_normal_noise=predictDeepFakeResult(predicted_test_SVC_normal_noise,frame_count_test_fake+frame_count_test_real)
print(pred_SVC_normal_noise)

accuracy_score(actual_test_label, pred_SVC_normal_noise)

f1_score(actual_test_label, pred_SVC_normal_noise)

log_loss(actual_test_label,pred_SVC_normal_noise)

"""##Comparison"""

#BoxPlot for cross validation scores

data_SVC = [cvs_SVC_lda, cvs_SVC_pca, cvs_SVC_normal]

fig_SVC = plt.figure(figsize =(10, 7))
  
# Creating axes instance
ax_SVC = fig_SVC.add_axes([0, 0, 1, 1])
  
# Creating plot
bp_SVC = ax_SVC.boxplot(data_SVC)
  
# show plot
plt.show()

"""## MLP"""

from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import cross_val_score

def trainMLP(train_data, label_data, test_data,test_label):
  clf = MLPClassifier()
  clf=clf.fit(train_data,label_data)
  print(clf.score(test_data,test_label))
  cvs = cross_val_score(clf, train_data, label_data, cv=5)
  print(cvs)
  
  predicted_test = clf.predict(test_data)
  return predicted_test,cvs

"""## MLP_LDA"""

predicted_test_MLP_lda,cvs_MLP_lda=trainMLP(lda_train_data,label_data,lda_test_data,test_label)
predicted_test_MLP_lda

pred_MLP_lda=predictDeepFakeResult(predicted_test_MLP_lda,frame_count_test_fake+frame_count_test_real)
print(pred_MLP_lda)

accuracy_score(actual_test_label, pred_MLP_lda)

f1_score(actual_test_label, pred_MLP_lda)

log_loss(actual_test_label,pred_MLP_lda)

"""## MLP_PCA"""

predicted_test_MLP_pca,cvs_MLP_pca=trainMLP(pca_train_data,label_data,pca_test_data,test_label)
predicted_test_MLP_pca

pred_MLP_pca=predictDeepFakeResult(predicted_test_MLP_pca,frame_count_test_fake+frame_count_test_real)
print(pred_MLP_pca)

accuracy_score(actual_test_label, pred_MLP_pca)

f1_score(actual_test_label, pred_MLP_pca)

log_loss(actual_test_label,pred_MLP_pca)

predicted_test_MLP_pca_noise,_=trainMLP(pca_train_data_noise,label_data_noise,pca_test_data,test_label)
predicted_test_MLP_pca_noise

pred_MLP_pca_noise=predictDeepFakeResult(predicted_test_MLP_pca_noise,frame_count_test_fake+frame_count_test_real)
print(pred_MLP_pca_noise)

accuracy_score(actual_test_label, pred_MLP_pca_noise)

f1_score(actual_test_label, pred_MLP_pca_noise)

log_loss(actual_test_label,pred_MLP_pca_noise)

"""##MLP_Normal"""

predicted_test_MLP_normal,cvs_MLP_normal=trainMLP(train_data,label_data,test_data,test_label)
predicted_test_MLP_normal

pred_MLP_normal=predictDeepFakeResult(predicted_test_MLP_normal,frame_count_test_fake+frame_count_test_real)
print(pred_MLP_normal)

accuracy_score(actual_test_label, pred_MLP_normal)

f1_score(actual_test_label, pred_MLP_normal)

log_loss(actual_test_label,pred_MLP_normal)

"""##Comaprison"""

#BoxPlot for cross validation scores

data_MLP = [cvs_MLP_lda, cvs_MLP_pca, cvs_MLP_normal]

fig_MLP = plt.figure(figsize =(10, 7))
  
# Creating axes instance
ax_MLP = fig_MLP.add_axes([0, 0, 1, 1])
  
# Creating plot
bp_MLP = ax_MLP.boxplot(data_MLP)
  
# show plot
plt.show()

"""## KNN"""

from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import cross_val_score
def trainKNN(train_data, label_data, test_data,test_label):
  clf = KNeighborsClassifier(n_neighbors=3)
  clf.fit(train_data,label_data)
  print(clf.score(test_data,test_label))
  cvs = cross_val_score(clf, train_data, label_data, cv=5)
  print(cvs)
  
  predicted_test = clf.predict(test_data)
  return predicted_test,cvs

"""## KNN_LDA"""

predicted_test_KNN_lda,cvs_KNN_lda=trainKNN(lda_train_data,label_data,lda_test_data,test_label)
predicted_test_KNN_lda

pred_KNN_lda=predictDeepFakeResult(predicted_test_KNN_lda,frame_count_test_fake+frame_count_test_real)
print(pred_KNN_lda)

accuracy_score(actual_test_label, pred_KNN_lda)

f1_score(actual_test_label, pred_KNN_lda)

log_loss(actual_test_label,pred_KNN_lda)

"""## KNN_PCA"""

predicted_test_KNN_pca,cvs_KNN_pca=trainKNN(pca_train_data,label_data,pca_test_data,test_label)
predicted_test_KNN_pca

pred_KNN_pca=predictDeepFakeResult(predicted_test_KNN_pca,frame_count_test_fake+frame_count_test_real)
print(pred_KNN_pca)

accuracy_score(actual_test_label, pred_KNN_pca)

f1_score(actual_test_label, pred_KNN_pca)

log_loss(actual_test_label,pred_KNN_pca)

"""##KNN_Normal"""

predicted_test_KNN_normal,cvs_KNN_normal=trainKNN(train_data,label_data,test_data,test_label)
predicted_test_KNN_normal

pred_KNN_normal=predictDeepFakeResult(predicted_test_KNN_normal,frame_count_test_fake+frame_count_test_real)
print(pred_KNN_normal)

from sklearn.metrics import accuracy_score
accuracy_score(actual_test_label, pred_KNN_normal)

from sklearn.metrics import f1_score
f1_score(actual_test_label, pred_KNN_normal)

from sklearn.metrics import log_loss
log_loss(actual_test_label,pred_KNN_normal)

"""##Comaprison"""

#BoxPlot for cross validation scores

data_KNN = [cvs_KNN_lda, cvs_KNN_pca, cvs_KNN_normal]

fig_KNN = plt.figure(figsize =(10, 7))
  
# Creating axes instance
ax_KNN = fig_KNN.add_axes([0, 0, 1, 1])
  
# Creating plot
bp_KNN = ax_KNN.boxplot(data_KNN)
  
# show plot
plt.show()

"""##Comaprison for LDAs"""

#BoxPlot for cross validation scores

data_LDA = [cvs_SVC_lda, cvs_MLP_lda, cvs_KNN_lda]

fig_LDA = plt.figure(figsize =(10, 7))
  
# Creating axes instance
ax_LDA = fig_LDA.add_axes([0, 0, 1, 1])
  
# Creating plot
bp_LDA = ax_LDA.boxplot(data_LDA)
  
# show plot
plt.show()

"""##Comparison for PCAs"""

#BoxPlot for cross validation scores

data_PCA = [cvs_SVC_pca, cvs_MLP_pca, cvs_KNN_pca]

fig_PCA = plt.figure(figsize =(10, 7))
  
# Creating axes instance
ax_PCA = fig_PCA.add_axes([0, 0, 1, 1])
  
# Creating plot
bp_PCA = ax_PCA.boxplot(data_PCA)
  
# show plot
plt.show()

"""##Comparison for Normals """

#BoxPlot for cross validation scores

data_NORMAL = [cvs_SVC_normal, cvs_MLP_normal, cvs_KNN_normal]

fig_NORMAL = plt.figure(figsize =(10, 7))
  
# Creating axes instance
ax_NORMAL = fig_NORMAL.add_axes([0, 0, 1, 1])
  
# Creating plot
bp_NORMAL = ax_NORMAL.boxplot(data_NORMAL)
  
# show plot
plt.show()

"""##InceptionResnetV2"""

from tensorflow.keras.applications import InceptionResNetV2
from tensorflow.keras.layers import Conv2D
from tensorflow.keras.layers import MaxPooling2D
from tensorflow.keras.layers import Flatten
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import Dropout
from tensorflow.keras.layers import InputLayer
from tensorflow.keras.layers import GlobalAveragePooling2D
from tensorflow.keras.models import Sequential
from tensorflow.keras.models import Model
from tensorflow.keras import optimizers
from tensorflow.keras.callbacks import ReduceLROnPlateau, EarlyStopping
from tensorflow.keras.utils import to_categorical

def resizingImages(img_list):
  newImgList=[]
  for i in img_list:
    img = cv2.resize(i,(128, 128), interpolation=cv2.INTER_CUBIC)
    newImgList.append(img)
  return np.array(newImgList)

train_Resizedimages_mediapipe_label = [0]*len(processedImagePath_Train_Fake_mediapipe) + [1]*len(processedImagePath_Train_Real_mediapipe)
train_Resizedimages_mediapipe_label = to_categorical(train_Resizedimages_mediapipe_label,2)
val_Resizedimages_mediapipe_label = [0]*len(processedImagePath_Val_Fake_mediapipe) + [1]*len(processedImagePath_Val_Real_mediapipe)
val_Resizedimages_mediapipe_label = to_categorical(val_Resizedimages_mediapipe_label,2)
test_Resizedimages_mediapipe_label = [0]*len(processedImagePath_Test_Fake_mediapipe) + [1]*len(processedImagePath_Test_Real_mediapipe)
test_Resizedimages_mediapipe_label = to_categorical(test_Resizedimages_mediapipe_label,2)
# train_images_mediapipe_label_CNN = [[1,0] for i in range(len(processedImagePath_Train_Fake_mediapipe))] + [[0,1] for i in range(len(processedImagePath_Train_Real_mediapipe))]
# val_images_mediapipe_label_CNN = [[1,0] for i in range(len(processedImagePath_Val_Fake_mediapipe))] + [[0,1] for i in range(len(processedImagePath_Val_Real_mediapipe))]
# print(train_images_mediapipe_label_CNN)

train_Resizedimages_mediapipe_label_noise = [0]*len(processedImagePath_Train_Fake_mediapipe_noise) + [1]*len(processedImagePath_Train_Real_mediapipe_noise)
train_Resizedimages_mediapipe_label_noise = to_categorical(train_Resizedimages_mediapipe_label_noise,2)

print(train_Resizedimages_mediapipe_label)

def createImageArray(path_list):
  img_list = []
  for path in path_list:
    img = cv2.imread(path)
    img_list.append(img)
  return img_list

train_images_mediapipe_CNN = createImageArray(processedImagePath_Train_Fake_mediapipe + processedImagePath_Train_Real_mediapipe)

train_images_mediapipe_CNN_noise = createImageArray(processedImagePath_Train_Fake_mediapipe_noise + processedImagePath_Train_Real_mediapipe_noise)

val_images_mediapipe_CNN = createImageArray(processedImagePath_Val_Fake_mediapipe + processedImagePath_Val_Real_mediapipe)

test_images_mediapipe_CNN = createImageArray(processedImagePath_Test_Fake_mediapipe + processedImagePath_Test_Real_mediapipe)

print(val_images_mediapipe_CNN)

train_Resizedimages_mediapipe = resizingImages(train_images_mediapipe_CNN)
# train_Resizedimages_mediapipe_label = np.array(train_images_mediapipe_label_CNN)
val_Resizedimages_mediapipe = resizingImages(val_images_mediapipe_CNN)
# val_Resizedimages_mediapipe_label = np.array(val_images_mediapipe_label_CNN )

train_Resizedimages_mediapipe_noise = resizingImages(train_images_mediapipe_CNN_noise)

# test_images_mediapipe_label_CNN = [[1,0] for i in range(len(processedImagePath_Test_Fake_mediapipe))] + [[0,1] for i in range(len(processedImagePath_Test_Real_mediapipe))]
test_Resizedimages_mediapipe = resizingImages(test_images_mediapipe_CNN)
# test_Resizedimages_mediapipe_label  = np.array(test_images_mediapipe_label_CNN )

train_Resizedimages_mediapipe = train_Resizedimages_mediapipe.astype('float32')
val_Resizedimages_mediapipe = val_Resizedimages_mediapipe.astype('float32')
train_Resizedimages_mediapipe  = train_Resizedimages_mediapipe  / 255.
val_Resizedimages_mediapipe = val_Resizedimages_mediapipe / 255.

train_Resizedimages_mediapipe_noise = train_Resizedimages_mediapipe_noise.astype('float32')
train_Resizedimages_mediapipe_noise = train_Resizedimages_mediapipe_noise / 255

test_Resizedimages_mediapipe = test_Resizedimages_mediapipe.astype('float32')
test_Resizedimages_mediapipe = test_Resizedimages_mediapipe / 255

googleNet_model = InceptionResNetV2(include_top=False, weights='imagenet', input_shape=(128,128,3))
googleNet_model.trainable = True
model = Sequential()
model.add(googleNet_model)
model.add(GlobalAveragePooling2D())
model.add(Dense(units=2, activation='softmax'))
model.compile(loss='binary_crossentropy',
              optimizer=optimizers.Adam(lr=1e-5, beta_1=0.9, beta_2=0.999, epsilon=None, decay=0.0, amsgrad=False),
              metrics=['accuracy'])
model.summary()

EPOCHS = 20
BATCH_SIZE = 50

history = model.fit(train_Resizedimages_mediapipe, train_Resizedimages_mediapipe_label, batch_size = BATCH_SIZE, epochs = EPOCHS, validation_data = (val_Resizedimages_mediapipe, val_Resizedimages_mediapipe_label), verbose = 1)

predicted_test_Inception= model.predict_classes(test_Resizedimages_mediapipe)

print(predicted_test_Inception)

a=0
b=0
for i in predicted_test_Inception:
  if i==0:
    a+=1
  else:
    b+=1
print(a,b)

def predictDeepFakeResultInception(predicted_test,frame_count_test):
  k=0
  prediction=[]
  len1=len(predicted_test)
  for i in frame_count_test:
    real_count=0
    fake_count=0
    # if i+k>=len1:
    #   break
    for j in range(i):
      if predicted_test[k]>0.5:
        real_count+=1
      else:
        fake_count+=1
      k+=1
    if real_count/(real_count+fake_count)>=0.5:
      prediction.append(1)
    else:
      prediction.append(0)
  return prediction

pred_Inception_mediapipe = predictDeepFakeResultInception(predicted_test_Inception,frame_count_test_fake+frame_count_test_real)
print(pred_Inception_mediapipe)

from sklearn.metrics import accuracy_score
accuracy_score(actual_test_label, pred_Inception_mediapipe)

from sklearn.metrics import f1_score
f1_score(actual_test_label, pred_Inception_mediapipe)

from sklearn.metrics import log_loss
log_loss(actual_test_label, pred_Inception_mediapipe)

"""## CNN"""

def createImageArray(path_list):
  img_list = []
  for path in path_list:
    img = cv2.imread(path)
    img_list.append(img)
  return img_list

train_images_mediapipe_CNN = createImageArray(processedImagePath_Train_Fake_mediapipe + processedImagePath_Train_Real_mediapipe)

train_images_mediapipe_label_CNN = [0]*len(processedImagePath_Train_Fake_mediapipe) + [1]*len(processedImagePath_Train_Real_mediapipe)

val_images_mediapipe_CNN = createImageArray(processedImagePath_Val_Fake_mediapipe + processedImagePath_Val_Real_mediapipe)

val_images_mediapipe_label_CNN = [0]*len(processedImagePath_Val_Fake_mediapipe) + [1]*len(processedImagePath_Val_Real_mediapipe)

test_images_mediapipe_CNN = createImageArray(processedImagePath_Test_Fake_mediapipe + processedImagePath_Test_Real_mediapipe)

test_images_mediapipe_label_CNN = [0]*len(processedImagePath_Test_Fake_mediapipe) + [1]*len(processedImagePath_Test_Real_mediapipe)

train_images_mediapipe_CNN = np.array(train_images_mediapipe_CNN)
train_images_mediapipe_label_CNN = np.array(train_images_mediapipe_label_CNN)
val_images_mediapipe_CNN = np.array(val_images_mediapipe_CNN)
val_images_mediapipe_label_CNN  = np.array(val_images_mediapipe_label_CNN )
test_images_mediapipe_CNN = np.array(test_images_mediapipe_CNN)
test_images_mediapipe_label_CNN  = np.array(test_images_mediapipe_label_CNN )

train_images_mediapipe_CNN = train_images_mediapipe_CNN.astype('float32')
val_images_mediapipe_CNN = val_images_mediapipe_CNN.astype('float32')
train_images_mediapipe_CNN  = train_images_mediapipe_CNN  / 255
val_images_mediapipe_CNN = val_images_mediapipe_CNN / 255
test_images_mediapipe_CNN = test_images_mediapipe_CNN.astype('float32')
test_images_mediapipe_CNN  = test_images_mediapipe_CNN  / 255

import keras
from keras.models import Sequential,Input,Model
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras.layers.normalization import BatchNormalization
from keras.layers.advanced_activations import LeakyReLU

batch_size = 32
epochs = 10
num_classes = 2

# from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
# custom_callbacks = [
#     EarlyStopping(
#         monitor = 'val_loss',
#         mode = 'min',
#         patience = 5,
#         verbose = 1
#     ),
#     ModelCheckpoint(
#         filepath = os.path.join(checkpoint_filepath, 'best_model.h5'),
#         monitor = 'val_loss',
#         mode = 'min',
#         verbose = 1,
#         save_best_only = True
#     )
# ]

classifier = Sequential()
classifier.add(Conv2D(32, (3, 3), input_shape = (128, 128, 3), activation = 'relu'))
classifier.add(MaxPooling2D(pool_size = (2, 2)))
classifier.add(Dropout(0.25))

classifier.add(Conv2D(64, (3, 3), activation='linear',padding='same'))
classifier.add(MaxPooling2D((2, 2),padding='same'))
classifier.add(Dropout(0.25))

classifier.add(LeakyReLU(alpha=0.1)) 
classifier.add(Conv2D(128, (3, 3), activation='linear',padding='same'))
classifier.add(Dropout(0.4))

 
classifier.add(Flatten())
classifier.add(Dense(units = 128, activation = 'relu'))
# classifier.add(Dense(units = 1, activation = 'sigmoid'))
classifier.compile(optimizer = 'adam', loss = 'binary_crossentropy', metrics = ['accuracy'])

!pip install efficientnet

from efficientnet.tfkeras import EfficientNetB0 
from keras.regularizers import l2
efficient_net = EfficientNetB0(
    weights = 'imagenet',
    input_shape = (128, 128, 3),
    include_top = False,
    pooling = 'max'
)

model = Sequential()
model.add(efficient_net)
model.add(Dense(units = 512, activation = 'relu'))
model.add(Dropout(0.5))
model.add(Dense(units = 128, activation = 'relu'))
model.add(Dense(units = 1, activation = 'sigmoid',kernel_regularizer=l2(0.01), bias_regularizer=l2(0.01)))
model.summary()

# cnn.summary()
# classifier.summary()
from tensorflow.keras.optimizers import Adam
model.compile(optimizer = Adam(lr=0.0001), loss='binary_crossentropy', metrics=['accuracy'])

x = []
for i in range(len(train_Resizedimages_mediapipe_label)):
  if(train_Resizedimages_mediapipe_label[i][0]==1):
    x.append(0)
  else:
    x.append(1)

y = []
for i in range(len(val_Resizedimages_mediapipe_label)):
  if(val_Resizedimages_mediapipe_label[i][0]==1):
    y.append(0)
  else:
    y.append(1)

# train_cnn = cnn.fit(train_images_dlib_CNN, train_images_dlib_label_CNN, batch_size=batch_size,epochs=epochs,verbose=1,validation_data=(val_images_dlib_CNN, val_images_dlib_label_CNN))
train_cnn = model.fit(train_Resizedimages_mediapipe, np.array(x),epochs=epochs,verbose=1,validation_data=(val_Resizedimages_mediapipe, np.array(y)),validation_steps = 100 )

predicted_test_CNN= model.predict(test_Resizedimages_mediapipe)

pred_CNN_mediapipe = predictDeepFakeResult(predicted_test_CNN,frame_count_test_fake+frame_count_test_real)

# print(pred_CNN_mediapipe)
print(predicted_test_CNN)

from sklearn.metrics import accuracy_score
accuracy_score(actual_test_label, pred_CNN_mediapipe)

from sklearn.metrics import f1_score
f1_score(actual_test_label, pred_CNN_mediapipe)

from sklearn.metrics import log_loss
log_loss(actual_test_label, pred_CNN_mediapipe)