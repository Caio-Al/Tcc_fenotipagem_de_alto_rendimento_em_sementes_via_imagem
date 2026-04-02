import shutil

class CameraHardware:
    def capturar_imagem(self):
        print("[Hardware] Simulando acionamento do Relé de LED...")
        print("[Hardware] Capturando foto...")
        caminho_salvo = "img/captura_atual.jpg"
        try:
            shutil.copy("image copy 3.png", caminho_salvo)
            print(f"[Hardware] Foto salva em: {caminho_salvo}")
            return caminho_salvo
        except FileNotFoundError:
            print("Erro: Coloque uma foto chamada 'sample_31.png' na pasta do projeto para testar.")
            return None