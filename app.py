import pandas as pd
import numpy as np
import streamlit as st 
from PIL import Image
from datetime import datetime
import time
import requests
import os
import pickle

from keras.models import model_from_json


image = Image.open('IMG-20171231-WA0001.jpg')

st.image(image, caption='')

st.markdown("# Vai Corrê!!!")


def vai_corre():

  #json_file = open('model/model.json', 'r')
  #loaded_model_json = json_file.read()
  #json_file.close()
  #loaded_model = model_from_json(loaded_model_json)
  # load weights into new model
  #loaded_model.load_weights("model/model.h5")
  #print("Loaded model from disk")
  
  model = pickle.load(open('model/best_model_rf.pkl', 'rb'))

  #model_predictor = model.load_model('model-2022-02-23.json')


  dia_semana = st.text_input('0 = dia normal ...  1 = fim de semana', 1)

  volume_semanal_ant = st.text_input('Volume semanal atual', '25')

  volume_semanal_ant2 = st.text_input('Volume semana anterior', '20')

  data = {'dia_semana': dia_semana,
          'vol_semanal_ant': [volume_semanal_ant],
          'vol_semanal_ant2': [volume_semanal_ant2]
          }

  treino = model.predict(pd.DataFrame(data))


  st.markdown("--------------------")

  st.markdown("Vai corrê:")
  st.write(treino)

  st.markdown(datetime.now())


if __name__ == '__main__':
    vai_corre()
    