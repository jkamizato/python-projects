import cv2
from yt_dlp import YoutubeDL
from ultralytics import YOLO

from main import video_url

# 1. Carrega o modelo YOLO (baixa automático na 1ª vez)
print("Carregando modelo YOLO...")
model = YOLO('yolov8n.pt')

# 2. Configuração do Vídeo do YouTube
#video_url = "https://www.youtube.com/watch?v=1EiC9bvVGnk"  # Trânsito NY
#video_url = "https://www.youtube.com/watch?v=F8MN0o6RS9o"
# Ao vivo
video_url = "https://www.youtube.com/watch?v=v1AyuKms2nE"

ydl_opts = {
    'format': 'best[ext=mp4]/best',
    'quiet': True,
    'no_warnings': True
}

print("Conectando ao YouTube...")

try:
    # Extrai a URL direta
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(video_url, download=False)
        url_direta = info['url']
        print(f"Conectado: {info['title']}")

    # Abre o vídeo
    cap = cv2.VideoCapture(url_direta)

    if not cap.isOpened():
        print("Erro ao abrir o vídeo.")
        exit()

    print("Iniciando detecção... Pressione 'q' para sair.")

    while True:
        # 3. Lê o frame (AQUI nasce a variável 'frame')
        success, frame = cap.read()

        if not success:
            break

        # Opcional: Redimensionar para ficar mais leve
        #frame = cv2.resize(frame, (1020, 600))
        frame = cv2.resize(frame, (800, 400))

        # 4. YOLO analisa o frame
        # stream=True deixa mais rápido para vídeos
        results = model(frame, stream=True)

        # 5. Desenha os resultados no frame
        for result in results:
            # O método .plot() desenha as caixas e nomes (Car, Person, Bus)
            frame = result.plot()

        # Mostra na tela
        cv2.imshow('YOLOv8 - Deteccao em Tempo Real', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

except Exception as e:
    print(f"Ocorreu um erro: {e}")