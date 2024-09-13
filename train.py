import keras
from googletrans import Translator
import cv2
import numpy as np
from google.colab import drive
import requests
from PIL import Image
drive.mount('/content/drive')
from keras.applications import VGG16
from keras.models import Sequential,Model
from keras.layers import Dense,Dropout,Flatten,Input
from keras.layers import Concatenate
from keras import regularizers
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction.text import HashingVectorizer
from google.colab.patches import cv2_imshow
from pandas import read_csv,DataFrame
import re
import pickle

def train():
  ds = read_csv("/content/drive/MyDrive/ready_to_train.csv")

  n_classes = len(set(ds['category']))


  def preprocess_ds(ds)->list:
    translator = Translator()
    last_value = None
    categories = set(ds["category"])
    ans_lst= []
    max_samples=20
    dict_s  = {i:0 for i in categories}

    for index,r in ds.iterrows():
      if dict_s[r["category"]]<max_samples:
        text_data = str(translator.translate(r["text_data"],dest="en")).split()[:23]
        ans_lst.append([ " ".join(text_data),r["image"],r["category"]])
        dict_s[r["category"]]+=1


    return DataFrame(ans_lst,columns=["text_data","image","category"])

  def remove_html_tags(text):
      clean_text=re.sub(r'<.*?>', '', text)
      return clean_text

  ds = preprocess_ds(ds)
  from io import BytesIO
  def data_generator(ds, image_size,text_data,batch_size,le):
      def download_img(url):
        data = BytesIO(requests.get(url.replace("'","")).content)
        try:
          img = Image.open(data)
        except:
          print("ошибка",url.replace("'",""))
          return np.zeros((128,128,3))
        return resize_img(img)
      def resize_img(image):
          if not image: return np.zeros((128,128,3))
          img = cv2.resize(np.array(image),image_size)
          if img.shape==image_size:
            img=np.zeros((128,128,3))
          return img
      while True:
        for i in range(0,len(ds),batch_size):
          images_list = [download_img(i) for i in ds["image"][i:i+batch_size]]
          batch_labels = le.transform(ds["category"][i:i+batch_size])
          batch_text =text_data[i:i+batch_size]
          yield (np.array(images_list), np.array(batch_text)), np.array(batch_labels)

  texts = ds["text_data"]
  vectorizer = HashingVectorizer(n_features=1024)
  text_data = vectorizer.fit_transform(texts).toarray()

  img_width=64
  img_height=64
  CNN_model = VGG16(weights='imagenet', include_top=False, input_shape=(img_width, img_height,3))

  def make_final_model(CNN_model,vec_size,n_classes,dropout=0.5):
      image_input = Input(shape=(img_width, img_height,3))
      x = CNN_model(image_input)
      x = Flatten()(x)
      x = Dense(256, activation="relu",kernel_regularizer = regularizers.l2(1e-5))(x)
      x = Dropout(dropout)(x)
      x = Dense(256, activation="relu",kernel_regularizer = regularizers.l2(1e-5))(x)

      text_input = Input(shape=(vec_size,))
      y = Dense(vec_size, activation='relu')(text_input)

      combined = Concatenate()([x, y])
      z = Dropout(dropout)(combined)
      output = Dense(n_classes, activation="softmax")(z)

      model = Model(inputs=[image_input, text_input], outputs=output)
      return model
  label_encoder = LabelEncoder()
  y = label_encoder.fit_transform(ds['category'])
  y = np.array(y, dtype=np.int32)
  vec_size = text_data.shape[1]
  print(vec_size)
  model = make_final_model(CNN_model,vec_size,n_classes)
  batch_size=32
  model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
  model.fit(data_generator(ds,(img_width,img_height),text_data,batch_size,label_encoder),steps_per_epoch=len(ds["image"])//batch_size,epochs=10)
  return model,label_encoder,vectorizer
def predict(model,vectorizer,label_encoder,image,text):
  image = cv2.resize(np.array(Image.open("/content/drive/MyDrive/don_don.jpg")),(128,128))
  TEXT_DATA = [vectorizer.transform([text]).toarray()]
  predict = model.predict(x=[np.array([image]),TEXT_DATA])
  metka = predict.argmax(axis=-1)[0]
  answer = label_encoder.inverse_transform([metka])
