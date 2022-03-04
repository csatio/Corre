import pandas as pd
import numpy as np
import streamlit as st 
from PIL import Image
from datetime import datetime
import time
import os
import pickle
import psycopg2
import psycopg2.extras
import pandas.io.sql as psql
import matplotlib.pyplot as plt
import seaborn as sns


#image = Image.open('IMG-20171231-WA0001.jpg')

#st.image(image, caption='')

st.markdown('# Vai Corrê!')

st.markdown("--------------------")

st.title("PRÓXIMO TREINO")


def vai_corre():

  #json_file = open('model/model.json', 'r')
  #loaded_model_json = json_file.read()
  #json_file.close()
  #loaded_model = model_from_json(loaded_model_json)
  # load weights into new model
  #loaded_model.load_weights("model/model.h5")
  #print("Loaded model from disk")

  DATABASE_URL = os.environ['DATABASE_URL']

  conn = psycopg2.connect(DATABASE_URL, sslmode='require')
  df = psql.read_sql('SELECT * FROM corridas', conn)
  #product_category = psql.read_sql_query('select * from product_category', connection)
  conn.close()

  df['pace'] = df['duration'] / df ['distancia']
  df['week_number'] = df['date'].dt.year.astype(str) + '-' + (df['date'].dt.week + 100).astype(str).str[1:3]
  df['dia_semana'] = (df['date'].dt.weekday + 100).astype(str).str[1:3]
  df['vol_semanal'] = df['distancia'].groupby(df['week_number']).transform('sum')
  df['vol_semanal_ant'] = df.vol_semanal.shift(-1)
  df['vol_semanal_ant2'] = df.vol_semanal.shift(-2)
  fds = []
  for row in df['dia_semana']:
    if row=='06' or row=='05':
        fds.append(1)
    else:
        fds.append(0)
  df['fds'] = fds

  ult = df.head(1)
  
  hoje = datetime.today().strftime('%Y-%m-%d')

  dia_semana = datetime.today().weekday()

  if dia_semana == 5 or dia_semana == 6:
        fds = 1
  else:
        fds = 0

  volume_semanal_ant = ult['vol_semanal_ant']

  volume_semanal_ant2 = ult['vol_semanal_ant2']

  
  DATABASE_URL = os.environ['DATABASE_URL']
  
  model = pickle.load(open('model/best_model_rf_pg.pkl', 'rb'))

  #model_predictor = model.load_model('model-2022-02-23.json')


  data = {'fds': dia_semana,
          'vol_semanal_ant': [volume_semanal_ant],
          'vol_semanal_ant2': [volume_semanal_ant2]
          }

  #if st.button('Melhor treino'):
  treino = model.predict(pd.DataFrame(data))
  #else:
  #treino = ''

  

  #st.markdown("Vai corrê:")
  #st.write(treino[0])
  st.markdown(f'# {treino[0]} km')
  #st.markdown("km")
  #st.markdown("DISTÂNCIA")

  st.markdown("--------------------")

  st.markdown(datetime.now())
  #st.markdown("DATA")

  st.markdown("--------------------")
  st.markdown("CADASTRAR CORRIDA")
  #st.markdown("Distância (km):")

  distancia = st.text_input("Distância (km):", "")

  #st.markdown("Data (AAAA-MM-DD):")

  data_t = st.text_input("Data (AAAA-MM-DD):", "")

  #st.markdown("Tempo (HH:MM:SS):")

  tempo = st.text_input("Tempo (HH:MM:SS):", "")

  if st.button('Cadastrar'):
    msg =''
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cur = conn.cursor()
    cur.execute("SELECT date FROM corridas WHERE date = %s", (data_t,))
    tem = cur.fetchone() is not None

    if tem == False:
      cur.execute("INSERT INTO corridas(date, distancia, duration) VALUES (%s, %s, %s)", (data_t,distancia,tempo))
      msg = f'Data: {data_t}, Distância: {distancia}, Tempo: {tempo} registrado com sucesso.'
    else:
      cur.execute("UPDATE corridas set date= %s, distancia=%s, duration=%s where date=%s", (data_t,distancia,tempo,data_t))
      msg = f'Data: {data_t}, Distância: {distancia}, Tempo: {tempo} atualizado com sucesso.'

    conn.commit()
    cur.close()
    conn.close()
    st.markdown(msg)

  st.markdown("--------------------")
  st.markdown("VOLUME SEMANAL")
  st.markdown(volume_semanal_ant[0])

  df_bar = df[['date','distancia','vol_semanal_ant','pace']].sort_values(by="date")

  fig = plt.figure(figsize=(10, 4))
  sns.lineplot(x = "date", y = "distancia", data = df_bar)
  st.pyplot(fig)

  fig = plt.figure(figsize=(10, 4))
  sns.lineplot(x = "date", y = "vol_semanal_ant", data = df_bar)
  st.pyplot(fig)



if __name__ == '__main__':
    vai_corre()
    