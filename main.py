import keras
import cv2
from keras.applications import VGG16
from keras.layers import Sequential,Dense,Dropout,Flatten
from keras.layers.merge import concatenate

from keras.regularizers import l2
from datasets import load_dataset
ds = load_dataset("EmbeddingStudio/amazon-products-with-images")

img_width=224
img_height=224
CNN_model = VGG16(weights='imagenet', include_top=False, input_shape=(img_width, img_height, 3))

def make_final_model(CNN_model,vec_size,n_classes,dropout=0.5,l2_strength=1e-5):
    text_model= Sequential()
    text_model.add(Dense(vec_size,input_shape=(vec_size,)))# обработка текста в векторизованном виде
    #обрабокта вывода с CNN модели
    image_model = Sequential()
    image_model.add(Flatten(input_shape=CNN_model.output_shape[1:]))
    image_model.add(Dense(256,activation="relu",W_regularizer=l2(l2_strength)))
    image_model.add(Dropout(dropout))
    image_model.add(Dense(256,activation="relu",W_regularizer=l2(l2_strength)))
    CNN_model.add(image_model)# добавляем к исходной CNN модели

    merged = concatenate([CNN_model,text_model])
    final_model = Sequential()
    final_model.add(merged)
    final_model.add(Dropout(dropout))
    final_model.add(Dense(n_classes,activation="softmax"))
    return final_model
