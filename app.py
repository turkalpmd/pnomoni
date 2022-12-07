import pickle
import pandas as pd
import numpy as np
from PIL import Image
import streamlit as st

PAGE_TITLE = "Pnömoni | AI_MED"
PAGE_ICON = ":lungs:" # https://streamlit-emoji-shortcodes-streamlit-app-gwckff.streamlit.app/

st.set_page_config(page_title=PAGE_TITLE, page_icon=PAGE_ICON)

st.title("Pnömoni hastasının yoğun bakım ihtiyacı ihtimali")

img = Image.open("./images/pnm.webp")
st.image(img)


st.text("""
Bu uygulamada kararın doktora ait olduğu sadece bunun bir karar destek mekanizması 
olduğundan bahsetmek gerekir
        """)

filename = "./model/cart_model.sav"

loaded_model = pickle.load(open(filename, 'rb'))

pxid = st.number_input("Dosya No;", step = False)

pxgender = st.radio("Cinsiyet",
                         ('Erkek', 'Kız'))  

col1,col2,col3,col4,col5 = st.columns(5)

with col1:
    hypoxia = st.radio("Hipoksi durumu",
                       ('Var', 'Yok'))

    if hypoxia == 'Var':
        hypoxia = 1
    else:
        hypoxia = 0


with col2:
    resp_dist = st.radio("Solunum yetmezliği",
                         ('Var', 'Yok'))        

    if resp_dist == 'Var':
        resp_dist = 1
    else:
        resp_dist = 0                                        

with col3:
    fever = st.radio("Ateş Öyküsü",
                    ('Var', 'Yok'))   

    if fever == 'Var':
        fever = 1
    else:
        fever = 0                    

with col4:
    complaint = st.number_input("Şikayet süresi;", step = 1)

    

with col5: 
    agemo = st.number_input("Ay cinsinden yaşı;", step = 1)


px = {'Hypoxia':[hypoxia], 
      'Respiratory distress':[resp_dist], 
      'Fever':[fever], 
      'Complaint period':[complaint], 
      'Age':[agemo]}


pxdf = pd.DataFrame(px)

result = loaded_model.predict(pxdf).tolist()
result = result[0]

pxdf["Dosya No"] = pxid
pxdf["Hasta Cinsiyeti"] = pxgender

if result == 0:
    result = "Kritik bakım ihtiyacı beklenmiyor"
else:
    result = "Kritik bakım ihtiyacı oalbilir"



pxdf["result"] = result
pxdf.rename(columns={"Hypoxia":"Hipoksi",
                     "Respiratory distress":"Sol. yetm.",
                     "Fever":"Ateş",
                     "Complaint period":"Başvuru süresi",
                     "Age":"Yaş",
                     "result":"Tahmin"  }, inplace=True)


