# -*- coding: utf-8 -*-
"""single_caption.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1i_3KjNCpUunS2inK-Z84yzSj7SqfvzDc
"""


## import all the required library

import tensorflow as tf
tf.compat.v1.disable_eager_execution()
import re
import collections
import io
import pandas as pd
import numpy as np
from keras.applications.resnet50 import ResNet50,preprocess_input,decode_predictions
from keras.models import Model,load_model
from time import time
from keras.preprocessing import image
from keras.preprocessing.sequence import pad_sequences
from keras.utils import to_categorical
from keras.layers import *
from keras.layers.merge import add
from keras.utils import generic_utils
import segmentation_models as sm
import matplotlib.pyplot as plt
from google.colab import files
import pickle


## Read the encoding file 
with open('idx_to_word.pkl','rb') as i2w:
  idx_to_word = pickle.load(i2w)

with open('word_to_idx.pkl','rb') as w2i:
  word_to_idx = pickle.load(w2i)

## Load the model saved early
model = load_model('/content/model_19.h5')
model._make_predict_function()

model_temp = ResNet50(weights='imagenet',input_shape=(224,224,3))


model_resnet = Model(model_temp.input,model_temp.layers[-2].output)
model_resnet._make_predict_function()
## preprocess image
def preprocess_img(img):
  img = image.load_img(img,target_size=(224,224)) ## load image
  img = image.img_to_array(img)
  img = np.expand_dims(img,axis=0) ## it converts image in shape of a batch

  ## normalization
  img = preprocess_input(img)
  return img

def encode_img(img):
  img = preprocess_img(img)
  pred_vec = model_resnet.predict(img)
  pred_vec = pred_vec.reshape((1,pred_vec.shape[1])) 
  return pred_vec

## define pred function for a image 

def pred(photo):
  in_text = 'startseq'
  max_len=35

  for i in range(max_len):
    sequence = [word_to_idx[w] for w in in_text.split() if w in word_to_idx]
    sequence = pad_sequences([sequence],maxlen=max_len,padding='post')

    ypred = model.predict([photo,sequence])
    ypred = ypred.argmax()
    word = idx_to_word[ypred]
    in_text += (' '+word)

    if word == 'endseq':
      break
  final_cap = in_text.split()[1:-1]
  final_cap = ' '.join(final_cap)
  return final_cap

enc = encode_img('/content/temp12.jpg')

## this image predicts the cation for image
def pred_img(img):
  enc = encode_img(img)
  caption = pred(enc)
  return caption

