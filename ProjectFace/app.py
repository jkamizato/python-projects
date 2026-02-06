import streamlit as st
import cv2
import numpy as np
from PIL import Image

st.title("🕵️ Meu Sistema de Visão Computacional")

# Sidebar
confianca = st.sidebar.slider("Nível de Confiança", 0.0, 1.0, 0.5)
usar_webcam = st.sidebar.checkbox("Usar Webcam")

st.write("Ajuste a confiança na barra lateral!")

# Espaço para a imagem
frame_placeholder = st.empty()

if usar_webcam:
    cap = cv2.VideoCapture(0)
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            st.error("Erro na câmera")
            break

        # Aqui entraria sua lógica do YOLO ou Face Recognition!
        # Por enquanto, vamos só inverter as cores para testar
        frame = cv2.bitwise_not(frame)

        # Converter para formato que o navegador entende
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Mostrar no site
        frame_placeholder.image(frame, channels="RGB")

        # Botão de parada (truque do streamlit)
        if st.sidebar.button("Parar"):
            break
    cap.release()