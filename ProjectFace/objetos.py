import cv2
from ultralytics import YOLO
import math


def iniciar_detector_objetos():
    print("🔄 Carregando modelo YOLOv8 (pode demorar um pouco na 1ª vez)...")

    # Carrega o modelo 'nano' (n). É o mais leve e rápido para rodar na CPU.
    # Ele vai baixar o arquivo 'yolov8n.pt' automaticamente se não tiver.
    model = YOLO('yolov8n.pt')

    # Lista de classes que o modelo conhece (COCO dataset)
    classNames = ["pessoa", "bicicleta", "carro", "moto", "aviao", "onibus", "trem", "caminhao", "barco", "semaforo",
                  "hidrante", "placa pare", "parquimetro", "banco", "passaro", "gato", "cachorro", "cavalo", "ovelha",
                  "vaca",
                  "elefante", "urso", "zebra", "girafa", "mochila", "guarda-chuva", "bolsa", "gravata", "mala",
                  "frisbee",
                  "esqui", "snowboard", "bola esportiva", "pipa", "taco beisebol", "luva beisebol", "skate",
                  "prancha surf", "raquete tenis", "garrafa",
                  "taça vinho", "copo", "garfo", "faca", "colher", "tigela", "banana", "maca", "sanduiche", "laranja",
                  "brocolis", "cenoura", "cachorro-quente", "pizza", "donut", "bolo", "cadeira", "sofa", "vaso planta",
                  "cama",
                  "mesa jantar", "vaso sanitario", "monitor tv", "laptop", "mouse", "remoto", "teclado", "celular",
                  "microondas", "forno",
                  "torradeira", "pia", "geladeira", "livro", "relogio", "vaso", "tesoura", "ursinho", "secador",
                  "escova dentes", "caneta", "caneca"]

    cap = cv2.VideoCapture(0)
    cap.set(3, 1280)  # Largura
    cap.set(4, 720)  # Altura

    if not cap.isOpened():
        print("❌ Erro ao abrir webcam.")
        return

    print("🎥 Detector iniciado! Aponte para objetos (celular, garrafa, pessoas).")
    print("⌨️  Pressione 'q' para sair.")

    while True:
        success, img = cap.read()
        if not success:
            break

        # O YOLO faz a mágica aqui. stream=True ajuda na performance
        results = model(img, stream=True, verbose=False)

        # Para cada detecção
        for r in results:
            boxes = r.boxes
            for box in boxes:
                # 1. Bounding Box (Coordenadas do retângulo)
                x1, y1, x2, y2 = box.xyxy[0]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

                # 2. Confiança (0 a 1)
                conf = math.ceil((box.conf[0] * 100)) / 100

                # 3. Nome da Classe (O que é o objeto?)
                cls = int(box.cls[0])
                currentClass = classNames[cls]


                # Filtro: Só desenhar se tiver mais de 50% de certeza
                if conf > 0.5:
                    cor = (255, 0, 255)
                    label = f'{currentClass} {conf}'

                    if currentClass == 'celular':
                        cor = (255, 0, 0)
                        label = "PROIBIDO!"

                    # Desenha o retângulo
                    cv2.rectangle(img, (x1, y1), (x2, y2), cor, 3)

                    # Escreve o nome e a confiança
                    t_size = cv2.getTextSize(label, 0, fontScale=1, thickness=2)[0]
                    c2 = x1 + t_size[0], y1 - t_size[1] - 3

                    cv2.rectangle(img, (x1, y1), c2, cor, -1)  # Fundo do texto
                    cv2.putText(img, label, (x1, y1 - 2), 0, 1, [255, 255, 255], thickness=1, lineType=cv2.LINE_AA)

        cv2.imshow('Detector de Objetos YOLOv8', img)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    iniciar_detector_objetos()