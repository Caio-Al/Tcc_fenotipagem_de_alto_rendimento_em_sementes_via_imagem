import cv2
import numpy as np
import os

# --- Configurações ---
NOME_IMAGEM = "image_copy2.png" # Usando o resultado de segmentação limpo
PASTA_CROP = "sementes_isoladas"   # Pasta onde vamos salvar os recortes
LIMIAR_AREA_MINIMA = 100          # Área mínima para ignorar ruído
LIMIAR_AREA_MAXIMA = 50000        # Área máxima para ignorar objetos grandes (fundo/amontoados se houver)

# Criar a pasta de recortes se ela não existir
if not os.path.exists(PASTA_CROP):
    os.makedirs(PASTA_CROP)

# 1. Carregar a imagem
img = cv2.imread(NOME_IMAGEM)
if img is None:
    print(f"Erro: Não foi possível carregar a imagem {NOME_IMAGEM}")
    exit()

img_final = img.copy() # Cópia para desenhar os resultados

# 2. Pré-processamento Simples
# Convertemos para tons de cinza
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Desfoque leve (GaussianBlur) para suavizar bordas
blurred = cv2.GaussianBlur(gray, (5, 5), 0)

# 3. Binarização Simples e Agressiva
# Como o fundo é BRANCO PURO e as sementes têm cores e tons diferentes,
# um limiar fixo funciona muito melhor do que Otsu.
# Sementes (escuras) viram BRANCAS, Fundo (claro) vira PRETO.
# O valor '240' é o limiar. Se o fundo não for branco puro, podemos abaixar esse valor (ex: 200).
_, thresh = cv2.threshold(blurred, 240, 255, cv2.THRESH_BINARY_INV)

# 4. Encontrar os contornos
contornos, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# 5. Isolamento, Extração de Dados e Geração de Resultados
# Vamos analisar um por um
print("-" * 50)
print(f"{'ID':<5} | {'Área (px)':<10} | {'Perím. (px)':<10} | {'Cor Média (R,G,B)':<20}")
print("-" * 50)

contador_sementes = 0
for i, contorno in enumerate(contornos):
    area = cv2.contourArea(contorno)
    
    # Filtro de Área
    if area > LIMIAR_AREA_MINIMA and area < LIMIAR_AREA_MAXIMA:
        contador_sementes += 1
        perimetro = cv2.arcLength(contorno, True)
        
        # --- Extração de Dados Cromáticos (Cor Média) ---
        # Criamos uma máscara preta apenas para a semente atual
        mask = np.zeros(gray.shape, dtype="uint8")
        cv2.drawContours(mask, [contorno], -1, 255, -1)
        
        # Calculamos a cor média da semente usando a máscara
        cor_media_bgr = cv2.mean(img, mask=mask)[:3]
        # Convertemos de BGR (padrão OpenCV) para RGB (padrão humano)
        cor_media_rgb = (int(cor_media_bgr[2]), int(cor_media_bgr[1]), int(cor_media_bgr[0]))
        
        # Printar dados no terminal
        print(f"{contador_sementes:<5} | {area:<10.1f} | {perimetro:<10.2f} | {str(cor_media_rgb):<20}")
        
        # --- Fazer o Recorte (Crop) ---
        x, y, w, h = cv2.boundingRect(contorno)
        semente_recortada = img[y:y+h, x:x+w]
        
        # Salvar a semente isolada
        nome_arquivo_crop = f"{PASTA_CROP}/semente_{contador_sementes}.jpg"
        cv2.imwrite(nome_arquivo_crop, semente_recortada)
        
        # --- Desenhar na Imagem Final ---
        # Desenhar o contorno em verde
        cv2.drawContours(img_final, [contorno], -1, (0, 255, 0), 2)
        # Escrever o ID da semente
        cv2.putText(img_final, str(contador_sementes), (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

# Salvar as imagens de diagnóstico para você entender o processo
cv2.imwrite("diagnostico_1_binarizacao_limpa.jpg", thresh)
cv2.imwrite("resultado_final_marcacoes_limpas.jpg", img_final)

print("-" * 50)
print(f"Processamento concluído.")
print(f"Foram identificadas {contador_sementes} sementes válidas.")
print(f"Os recortes foram salvos na pasta: {PASTA_CROP}")
print(f"Verifique 'resultado_final_marcacoes_limpas.jpg' para validação visual.")