import cv2
import face_recognition
import os
import numpy as np
import sys


def carregar_e_treinar_rostos(diretorio):
    """
    Carrega as imagens de uma pasta e cria os encodings (assinaturas digitais) dos rostos.
    """
    rostos_conhecidos_encodings = []
    rostos_conhecidos_nomes = []

    print(f"🔄 Iniciando treinamento com imagens em '{diretorio}'...")

    # Verifica se a pasta existe
    if not os.path.exists(diretorio):
        os.makedirs(diretorio)
        print(f"⚠️ Pasta '{diretorio}' não existia e foi criada. Por favor, coloque fotos lá e reinicie!")
        return [], []

    lista_arquivos = os.listdir(diretorio)

    # Filtra apenas arquivos de imagem
    imagens_validas = [f for f in lista_arquivos if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp'))]

    if not imagens_validas:
        print(f"⚠️ Nenhuma foto encontrada em '{diretorio}'. O sistema só vai detectar 'Desconhecido'.")
        print("👉 Dica: Adicione fotos com o nome da pessoa (ex: Julio.jpg) nesta pasta.")

    for arquivo in imagens_validas:
        caminho_imagem = os.path.join(diretorio, arquivo)

        try:
            # Carrega a imagem
            imagem = face_recognition.load_image_file(caminho_imagem)

            # Tenta encontrar um rosto na imagem de treino
            encodings = face_recognition.face_encodings(imagem)

            if len(encodings) > 0:
                # Pega o primeiro rosto encontrado (encoding)
                rostos_conhecidos_encodings.append(encodings[0])

                # O nome será o nome do arquivo sem a extensão
                nome = os.path.splitext(arquivo)[0]
                rostos_conhecidos_nomes.append(nome)
                print(f"✅ Rosto aprendido: {nome}")
            else:
                print(f"❌ Aviso: Nenhum rosto encontrado na imagem: {arquivo} (tente uma foto mais clara)")
        except Exception as e:
            print(f"❌ Erro ao processar {arquivo}: {e}")

    return rostos_conhecidos_encodings, rostos_conhecidos_nomes


def iniciar_reconhecimento(encodings_conhecidos, nomes_conhecidos):
    print("\n🎥 Tentando abrir a webcam...")
    # Tenta o índice 0 (padrão) e depois o 1 (caso tenha webcam externa ou virtual)
    video_capture = cv2.VideoCapture(0)

    if not video_capture.isOpened():
        video_capture = cv2.VideoCapture(1)
        if not video_capture.isOpened():
            print("❌ Erro Crítico: Não foi possível acessar nenhuma webcam.")
            print("Verifique se ela está conectada ou sendo usada por outro programa (Zoom, Teams, etc).")
            return

    print("✅ Webcam iniciada! Olhe para a câmera.")
    print("⌨️  Pressione a tecla 'q' para encerrar o programa.")

    while True:
        # Captura frame a frame
        ret, frame = video_capture.read()
        if not ret:
            print("❌ Falha ao capturar frame da câmera.")
            break

        # Otimização: Reduzir o tamanho do frame para 1/4 para processar mais rápido
        frame_pequeno = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Converter de BGR (OpenCV) para RGB (face_recognition)
        # O numpy ascontiguousarray previne erros de memória em versões novas
        rgb_frame_pequeno = np.ascontiguousarray(frame_pequeno[:, :, ::-1])

        # Encontrar todos os rostos e seus encodings no frame atual
        face_locations = face_recognition.face_locations(rgb_frame_pequeno)
        face_encodings = face_recognition.face_encodings(rgb_frame_pequeno, face_locations)

        face_names = []

        for face_encoding in face_encodings:
            # Vê se o rosto bate com algum conhecido
            # tolerance=0.6 é o padrão. Menor = mais rigoroso, Maior = mais tolerante
            matches = face_recognition.compare_faces(encodings_conhecidos, face_encoding, tolerance=0.5)
            name = "Desconhecido"

            # Usa a distância do rosto para encontrar o melhor match
            face_distances = face_recognition.face_distance(encodings_conhecidos, face_encoding)

            if len(face_distances) > 0:
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = nomes_conhecidos[best_match_index]

            face_names.append(name)

        # Exibir os resultados
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Escala de volta para o tamanho original (x4)
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Define a cor (Verde para conhecido, Vermelho para desconhecido)
            cor = (0, 255, 0) if name != "Desconhecido" else (0, 0, 255)

            # Desenha o retângulo
            cv2.rectangle(frame, (left, top), (right, bottom), cor, 2)

            # Desenha a etiqueta com nome
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), cor, cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 0.8, (255, 255, 255), 1)

        # Mostra a imagem resultante
        cv2.imshow('Sistema de Reconhecimento Facial (Pressione Q para sair)', frame)

        # Pressione 'q' para sair
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Libera a câmera e fecha janelas
    video_capture.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    pasta_treino = "rostos_conhecidos"
    encodings, nomes = carregar_e_treinar_rostos(pasta_treino)
    iniciar_reconhecimento(encodings, nomes)