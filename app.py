import pandas as pd
import numpy as np
import streamlit as st 
from PIL import Image
from datetime import datetime
import time
import requests
import os
import pickle



image = Image.open('IMG-20171231-WA0001.jpg')

st.image(image, caption='')

st.markdown("# Vai Corrê!!!")


def vai_corre():
  
  model = pickle.load(open('model/best_model_xgb.pkl', 'rb'))
  

  dia_semana = st.text_input('Dia da semana 00 = segunda ...  06 = domingo', '06')

  volume_semanal = st.text_input('Volume semanal atual', '8')

  data = {'dia_semana': dia_semana,
          'vol_semanal_ant': [volume_semanal]
          }

  treino = model.predict(pd.DataFrame(data))


  st.markdown("--------------------")

  st.markdown("Vai corrê:")
  st.write(treino)

  st.markdown(datetime.now())


if __name__ == '__main__':
    vai_corre()
    