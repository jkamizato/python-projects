import cv2
import easyocr
import time

print("Loading OCR model")

render = easyocr.Reader(['pt', 'en'], gpu=False)

cap = cv2.VideoCapture(0)

print("System ready. Show a text and click on <space> to be read")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    cv2.imshow("OCR Reader - Click on <space>", frame)

    key = cv2.waitKey(1) & 0xFF

    if key == 32:
        print("Reading text...")

        resultados = render.readtext(frame)

        for(bbox, texto, probabilidade) in resultados:
            top_left = tuple(map(int, bbox[0]))
            bottom_right = tuple(map(int, bbox[2]))

            # Filtra leituras com confiança muito baixa (opcional)
            if probabilidade > 0.3:
                # Desenha o retângulo verde
                cv2.rectangle(frame, top_left, bottom_right, (0, 255, 0), 2)

                # Escreve o texto lido acima do retângulo
                cv2.putText(frame, texto, (top_left[0], top_left[1] - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

                print(f"Texto detectado: {texto} (Confiança: {probabilidade:.2f})")

            # Mostra o resultado congelado por 3 segundos ou até apertar tecla
        cv2.imshow('Resultado da Leitura', frame)
        cv2.waitKey(0)  # Espera qualquer tecla para voltar ao vídeo ao vivo



        # 4. Sair (Tecla 'q')
    elif key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()