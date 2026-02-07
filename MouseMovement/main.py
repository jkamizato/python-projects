import cv2
import mediapipe as mp
import pyautogui
import numpy as np
import time

# --- CONFIGURAÇÕES ---
wCam, hCam = 640, 480  # Tamanho da janela da câmera
#wCam, hCam = 1200, 1600  # Tamanho da janela da câmera
frame_reduction = 100  # Margem de redução (para não precisar esticar muito o braço)
suavizacao = 5  # Quanto maior, mais suave (e lento) o movimento

# Inicializa o MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.5
)
mp_draw = mp.solutions.drawing_utils

# Pega o tamanho da sua tela (ex: 1920x1080)
wScreen, hScreen = pyautogui.size()

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

prev_loc_x, prev_loc_y = 0, 0
curr_loc_x, curr_loc_y = 0, 0

print("Mouse Virtual Iniciado!")
print("Use o dedo INDICADOR para mover.")
print("Junte INDICADOR e POLEGAR para clicar.")
print("Pressione 'q' para sair.")

while True:
    success, img = cap.read()
    if not success:
        break

    # 1. Encontrar a mão
    # Espelha a imagem para ficar intuitivo (mover direita vai para direita)
    img = cv2.flip(img, 1)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)

    # Desenha o retângulo da área útil de controle
    cv2.rectangle(img, (frame_reduction, frame_reduction),
                  (wCam - frame_reduction, hCam - frame_reduction), (255, 0, 255), 2)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # 2. Pegar coordenadas dos dedos
            # Landmark 8 = Ponta do Indicador
            # Landmark 4 = Ponta do Polegar

            # Lista de coordenadas
            lmList = []
            for id, lm in enumerate(hand_landmarks.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append([id, cx, cy])

            # Se detectou a mão
            if len(lmList) != 0:
                x1, y1 = lmList[8][1], lmList[8][2]  # Indicador
                x2, y2 = lmList[4][1], lmList[4][2]  # Polegar

                # 3. Checar se o dedo está na área útil (Retângulo Roxo)
                # Converter coordenadas da Câmera para coordenadas da Tela (Interpolação)
                x3 = np.interp(x1, (frame_reduction, wCam - frame_reduction), (0, wScreen))
                y3 = np.interp(y1, (frame_reduction, hCam - frame_reduction), (0, hScreen))

                # 4. Suavizar o movimento (para o mouse não tremer)
                curr_loc_x = prev_loc_x + (x3 - prev_loc_x) / suavizacao
                curr_loc_y = prev_loc_y + (y3 - prev_loc_y) / suavizacao

                # Mover o Mouse
                pyautogui.moveTo(curr_loc_x, curr_loc_y)
                prev_loc_x, prev_loc_y = curr_loc_x, curr_loc_y

                # 5. Modo Clique (Distância entre indicador e polegar)
                # Calcula a distância
                length = np.hypot(x2 - x1, y2 - y1)

                # Se estiverem muito perto (< 30 pixels), clica
                if length < 30:
                    cv2.circle(img, (x1, y1), 15, (0, 255, 0), cv2.FILLED)  # Bola verde visual
                    pyautogui.click()
                    print("Click!")
                    # Pequeno delay para não dar duplo clique sem querer
                    # time.sleep(0.1) 

    # Mostrar imagem
    cv2.imshow("Mouse Virtual - Python", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()