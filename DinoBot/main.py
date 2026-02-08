import pyautogui
import time
from PIL import ImageGrab, ImageOps


def pular():
    pyautogui.keyDown('space')
    # O pulo no jogo depende de quanto tempo segura a tecla.
    # Um toque MUITO rápido faz um pulo baixo (bom para cactos duplos).
    time.sleep(0.02)
    pyautogui.keyUp('space')
    print("Pulo!")


print("--- BOT DO DINO V3 (Turbo) ---")
print("1. Posicione o mouse NA FRENTE do dino.")
print("2. DICA: Coloque um pouco mais longe (direita) para dar tempo de reagir.")
print("3. Aguarde 5 segundos...")

time.sleep(5)

# Pega posição inicial
x_mouse, y_mouse = pyautogui.position()

# Define uma CAIXA DE SENSOR em vez de um ponto
# Vamos olhar uma área de 40 pixels de largura por 10 de altura
# Isso garante que não vamos perder o cacto se ele for fino
box_width = 50
box_height = 10
sensor_box = (x_mouse, y_mouse, x_mouse + box_width, y_mouse + box_height)

# Tira foto inicial para saber a cor do fundo (pega a média da caixa)
img_inicial = ImageGrab.grab(sensor_box)
gray_inicial = ImageOps.grayscale(img_inicial)
# Calcula a soma dos pixels da área inicial (nossa referência de "vazio")
soma_referencia = sum(gray_inicial.getdata())

print(f"Sensor configurado! Referência de Luz: {soma_referencia}")
print("GO! (Clique no jogo)")
time.sleep(3)

pular()

try:
    while True:
        # Captura a área do sensor
        image = ImageGrab.grab(sensor_box)
        gray = ImageOps.grayscale(image)

        # Soma os valores dos pixels atuais
        soma_atual = sum(gray.getdata())

        # A LÓGICA MATEMÁTICA:
        # Se entrar um cacto (pixels pretos/cinzas), a soma total vai CAIR.
        # Fundo Branco (255) -> Cacto (80).
        # Se a diferença for significativa, é obstáculo.

        # Sensibilidade: Se mudar 1500 pontos (numa área de 500 pixels), pula.
        # Ajuste esse 1500 se estiver pulando à toa (aumente) ou não pulando (diminua).
        if soma_referencia - soma_atual > 1500:
            pular()
            # SEM SLEEP AQUI!
            # Queremos que ele volte a verificar o sensor IMEDIATAMENTE enquanto está no ar.
            # Assim, se tiver outro cacto logo depois, ele já vai saber.

            # Pequeno truque: Enquanto está no ar, não adianta apertar espaço.
            # Mas não vamos travar o código. Vamos deixar ele "ver" o segundo cacto
            # e tentar pular assim que tocar o chão.

except KeyboardInterrupt:
    print("Fim.")