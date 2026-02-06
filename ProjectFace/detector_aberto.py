from ultralytics import YOLOWorld
import cv2
import math


def iniciar_detector_personalizado():
    print("🔄 Carregando modelo YOLO-World (pode demorar um pouco)...")

    # Carrega o modelo YOLO-World (versão small ou medium)
    # Ele é maior que o nano, mas muito mais esperto
    model = YOLOWorld('yolov8s-world.pt')

    # AQUI ESTÁ A MÁGICA 🪄
    # Nós definimos o que queremos procurar!
    # Você pode colocar o que quiser aqui, em INGLÊS (funciona melhor)
    classes_personalizadas = ["pen", "mug", "person", "glasses", "watch", "cellphone", "kindle"]

    print(f"🎯 Configurando para detectar: {classes_personalizadas}")
    model.set_classes(classes_personalizadas)

    cap = cv2.VideoCapture(0)

    # Configurações de janela
    cv2.namedWindow("Detector Personalizado", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Detector Personalizado", 1280, 720)

    if not cap.isOpened():
        print("❌ Erro ao abrir webcam.")
        return

    print("🎥 Detector iniciado! Mostre uma caneta ou caneca.")
    print("⌨️  Pressione 'q' para sair.")

    while True:
        success, img = cap.read()
        if not success:
            break

        # Executa a detecção
        # conf=0.3: Baixamos um pouco a confiança pois objetos pequenos são difíceis
        results = model.predict(img, conf=0.25, verbose=False)

        # O próprio YOLO já tem uma função legal para desenhar tudo
        # Isso simplifica nosso código de desenho manual
        annotated_frame = results[0].plot()

        cv2.imshow('Detector Personalizado', annotated_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    iniciar_detector_personalizado()