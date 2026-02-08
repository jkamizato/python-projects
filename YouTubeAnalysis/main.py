import cv2
import mediapipe as mp
from yt_dlp import YoutubeDL

# --- 1. CONFIGURAÇÃO DO MEDIAPIPE (IA de Rosto) ---
mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils

# model_selection=1 é melhor para rostos mais distantes (comum em vídeos)
# min_detection_confidence=0.5 garante que ele só marque se tiver 50% de certeza
face_detection = mp_face_detection.FaceDetection(model_selection=1, min_detection_confidence=0.5)

# --- 2. CONFIGURAÇÃO DO YOUTUBE ---
# Exemplo: Pessoas andando em Tóquio (ótimo para testar)
video_url = "https://www.youtube.com/watch?v=F8MN0o6RS9o"
#video_url = "https://www.youtube.com/watch?v=Zx-YWuhn2Tw"

ydl_opts = {
    'format': 'best[ext=mp4]/best',
    'quiet': True,
    'no_warnings': True
}

print("Conectando ao YouTube... aguarde...")

try:
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(video_url, download=False)
        url_direta = info['url']
        print(f"Conectado: {info['title']}")

    # Inicia o vídeo
    cap = cv2.VideoCapture(url_direta)

    while True:
        success, frame = cap.read()
        if not success:
            break

        # Redimensionar para processar mais rápido (opcional, mas recomendado)
        frame = cv2.resize(frame, (1020, 600))

        # --- 3. DETECÇÃO DE ROSTO ---
        # O MediaPipe precisa de RGB, o OpenCV usa BGR
        img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_detection.process(img_rgb)

        if results.detections:
            for detection in results.detections:
                # O MediaPipe retorna coordenadas relativas (0.0 a 1.0)
                # Precisamos converter para pixels reais
                bboxC = detection.location_data.relative_bounding_box
                ih, iw, ic = frame.shape

                x = int(bboxC.xmin * iw)
                y = int(bboxC.ymin * ih)
                w = int(bboxC.width * iw)
                h = int(bboxC.height * ih)

                # Desenha o Retângulo (Quadrado)
                # Cor (0, 255, 0) = Verde
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

                # (Opcional) Escreve "Rosto" e a % de confiança
                confianca = int(detection.score[0] * 100)
                cv2.putText(frame, f'{confianca}%', (x, y - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # Mostra o resultado
        cv2.imshow('Detector de Rostos YouTube', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

except Exception as e:
    print(f"Erro: {e}")