import cv2
import numpy as np

class Semente:
    def __init__(self, id_semente, area, perimetro, largura, comprimento, cx, cy, contorno, cor_rgb):
        self.id_semente = id_semente
        self.area = area
        self.perimetro = perimetro
        self.largura = largura
        self.comprimento = comprimento
        self.centro_x = cx
        self.centro_y = cy
        self.contorno = contorno
        self.cor_rgb = cor_rgb 
        
        self.circularidade = (4 * np.pi * area) / (perimetro ** 2) if perimetro > 0 else 0
        self.razao_aspecto = comprimento / largura if largura > 0 else 0

class ExtratorCaracteristicas:
    def extrair_dados(self, img_original, contornos, limiar_area_min=100):
        lista_sementes = []
        contador = 0
        
        for contorno in contornos:
            area = cv2.contourArea(contorno)
            if area > limiar_area_min:
                contador += 1
                perimetro = cv2.arcLength(contorno, True)
                
                retangulo_min = cv2.minAreaRect(contorno)
                (cx, cy), (w, h), angulo = retangulo_min
                comprimento = max(w, h)
                largura = min(w, h)
                
                x, y, bw, bh = cv2.boundingRect(contorno)
                recorte_bruto = img_original[y:y+bh, x:x+bw].copy()
                
                contorno_deslocado = contorno - [x, y]
                
                mascara = np.zeros((bh, bw), dtype=np.uint8)
                cv2.drawContours(mascara, [contorno_deslocado], -1, 255, -1)
                
                cor_bgr = cv2.mean(recorte_bruto, mask=mascara)[:3]
                cor_rgb = (int(cor_bgr[2]), int(cor_bgr[1]), int(cor_bgr[0]))
                
                semente_bgra = cv2.cvtColor(recorte_bruto, cv2.COLOR_BGR2BGRA)
                semente_bgra[:, :, 3] = mascara
                
                caminho_salvamento = f"resultados/sementes_isoladas/semente_{contador}.png"
                cv2.imwrite(caminho_salvamento, semente_bgra)
                
                semente_obj = Semente(contador, area, perimetro, largura, comprimento, int(cx), int(cy), contorno, cor_rgb)
                lista_sementes.append(semente_obj)
                
        return lista_sementes