import cv2
import os
from hardware_camera import CameraHardware
from processamento_imagem import ProcessadorImagem
from extracao_dados import ExtratorCaracteristicas
from exportador_pdf import ExportadorRelatorio

def criar_pastas():
    pastas = ["resultados", "resultados/sementes_isoladas"]
    for pasta in pastas:
        os.makedirs(pasta, exist_ok=True)

def executar_pipeline():
    criar_pastas()
    print("=== INICIANDO SISTEMA DE FENOTIPAGEM ALTO RENDIMENTO ===")
    
    hardware = CameraHardware()
    processador = ProcessadorImagem()
    extrator = ExtratorCaracteristicas()
    exportador = ExportadorRelatorio()
    
    caminho_imagem = hardware.capturar_imagem()
    if not caminho_imagem:
        return
        
    print("[Processamento] Analisando imagem...")
    img_original, img_cinza, img_binarizada, contornos = processador.obter_contornos(caminho_imagem)    

    
    # Salvar diagnósticos básicos
    cv2.imwrite("resultados/1_imagem_original.jpg", img_original)
    cv2.imwrite("resultados/2_imagem_tons_cinza.jpg", img_cinza)
    cv2.imwrite("resultados/3_imagem_opening.jpg", img_binarizada)    
    print("[Extração] Recortando fundo e calculando dados morfológicos...")
    lista_sementes = extrator.extrair_dados(img_original, contornos)
    
    # Salvar imagem com marcações
    img_marcacoes = img_original.copy()
    for s in lista_sementes:
        cv2.drawContours(img_marcacoes, [s.contorno], -1, (0, 255, 0), 2)
        cv2.putText(img_marcacoes, f"ID: {s.id_semente}", (s.centro_x - 15, s.centro_y - 15), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    cv2.imwrite("resultados/3_imagem_marcacoes.jpg", img_marcacoes)
    
    print(f"[Extração] {len(lista_sementes)} sementes processadas.")
    
    # Gerar Relatório PDF
    print("[Exportador] Gerando relatório PDF...")
    exportador.gerar_pdf(lista_sementes)
    
    print("=== PROCESSO CONCLUÍDO. Verifique a pasta 'resultados'. ===")

if __name__ == "__main__":
    executar_pipeline()