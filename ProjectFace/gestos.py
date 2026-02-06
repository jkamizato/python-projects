import cv2
import mediapipe as mp

# Configurações do MediaPipe
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# Inicializa o detector de mãos
# max_num_hands=2: Detecta até duas mãos
# min_detection_confidence=0.7: Só considera se tiver 70% de certeza que é uma mão
hands = mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.7)

# IDs dos pontos das pontas dos dedos (conforme documentação do MediaPipe)
# 4=Dedão, 8=Indicador, 12=Médio, 16=Anelar, 20=Mínimo
PONTAS_DEDOS = [4, 8, 12, 16, 20]


def iniciar_deteccao_gestos():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("❌ Erro ao abrir a webcam.")
        return

    print("✋ Sistema de Gestos Iniciado! Mostre sua mão para a câmera.")
    print("⌨️  Pressione 'q' para sair.")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Espelhar a imagem (para ficar intuitivo como um espelho)
        frame = cv2.flip(frame, 1)

        # Converter BGR (OpenCV) para RGB (MediaPipe)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Processar a imagem buscando mãos
        results = hands.process(frame_rgb)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Desenhar o esqueleto da mão na imagem original
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                # Lógica para contar dedos levantados
                dedos_levantados = []

                # --- DEDÃO (Lógica diferente: movimento lateral) ---
                # Verifica se a ponta do dedão (4) está à esquerda ou direita da articulação (3)
                # Nota: Como espelhamos a imagem, a lógica inverte dependendo da mão.
                # Esta é uma lógica simplificada que funciona bem para a mão direita na tela.
                if hand_landmarks.landmark[PONTAS_DEDOS[0]].x < hand_landmarks.landmark[PONTAS_DEDOS[0] - 1].x:
                    dedos_levantados.append(1)
                else:
                    dedos_levantados.append(0)

                # --- OUTROS 4 DEDOS (Lógica vertical) ---
                # Verifica se a ponta do dedo (y) está ACIMA da articulação do meio (y)
                # Lembre-se: Em imagens, Y=0 é o topo. Então "menor Y" significa "mais alto".
                for id_ponta in PONTAS_DEDOS[1:]:
                    if hand_landmarks.landmark[id_ponta].y < hand_landmarks.landmark[id_ponta - 2].y:
                        dedos_levantados.append(1)
                    else:
                        dedos_levantados.append(0)

                total_dedos = dedos_levantados.count(1)

                # Exibir o número de dedos na tela
                cv2.rectangle(frame, (20, 20), (170, 110), (0, 255, 0), cv2.FILLED)
                cv2.putText(frame, f'{total_dedos}', (45, 100), cv2.FONT_HERSHEY_PLAIN,
                            6, (255, 0, 0), 10)

                # Exibir mensagem baseada no gesto
                mensagem = ""
                if total_dedos == 0:
                    mensagem = "Mao Fechada"
                elif total_dedos == 5:
                    mensagem = "Mao Aberta"
                elif total_dedos == 2 and dedos_levantados[1] and dedos_levantados[2]:
                    mensagem = "Paz e Amor"
                elif total_dedos == 2 and dedos_levantados[0] and dedos_levantados[4]:
                    mensagem = "HangLoose"
                    # Teste para fechar no hangloose
                    cap.release()
                    cv2.destroyAllWindows()

                if mensagem:
                    cv2.putText(frame, mensagem, (190, 80), cv2.FONT_HERSHEY_PLAIN,
                                3, (0, 255, 0), 3)

        cv2.imshow("Detector de Gestos (MediaPipe)", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    iniciar_deteccao_gestos()