# Sistema de Fenotipagem — Versão Web (Celular)

## O que mudou em relação ao pré-TCC

| Antes                     | Agora                              |
|---------------------------|------------------------------------|
| Raspberry Pi 4 + câmera   | Computador comum + celular         |
| Picamera2 (CSI)           | Câmera do celular via browser      |
| hardware_camera.py        | **api.py** (Flask)                 |
| Rodar main.py localmente  | Acessar site no celular            |

> Os arquivos `processamento_imagem.py`, `extracao_dados.py` e `exportador_pdf.py`
> **não foram alterados**. A mudança foi cirúrgica: só a camada de captura mudou.

---

## Estrutura de arquivos

```
projeto/
├── api.py                      ← NOVO: backend Flask (substitui hardware_camera.py)
├── processamento_imagem.py     ← sem alteração
├── extracao_dados.py           ← sem alteração
├── exportador_pdf.py           ← sem alteração
├── main.py                     ← ainda pode ser usado para testes locais
├── requirements.txt            ← atualizado com flask e flask-cors
├── templates/
│   └── index.html              ← NOVO: interface web para o celular
└── resultados/                 ← gerado automaticamente
```

---

## Como instalar

```bash
pip install -r requirements.txt
```

---

## Como rodar

### 1. Descubra o IP do seu computador

**Windows:**
```
ipconfig
```
Procure por "Endereço IPv4" (ex: `192.168.1.15`)

**Linux/Mac:**
```
ip addr   ou   ifconfig
```

### 2. Inicie a API

```bash
python api.py
```

Você verá algo como:
```
* Running on http://0.0.0.0:5000
```

### 3. Acesse pelo celular

O celular e o computador precisam estar **no mesmo Wi-Fi**.

Abra o navegador do celular e acesse:
```
http://192.168.1.15:5000
```
(use o IP do seu computador)

> A página `index.html` também pode ser aberta diretamente no browser
> do celular sem servidor, mas nesse caso ela não pode enviar imagens
> para a API — é melhor servir pelo Flask mesmo.

---

## Adicionando a rota para servir o HTML (opcional)

Se quiser que a API já sirva o HTML automaticamente, adicione isso no `api.py`:

```python
from flask import render_template

@app.route("/")
def index():
    return render_template("index.html")
```

Aí você acessa `http://IP:5000/` e já cai direto na interface.

---

## Fluxo resumido

```
Celular (browser)
    │ foto via <input capture="environment">
    │ POST /analisar  (multipart/form-data)
    ▼
api.py (Flask)
    │ decodifica imagem com OpenCV
    │ chama processamento_imagem.py
    │ chama extracao_dados.py
    │ chama exportador_pdf.py
    │ retorna JSON com dados + imagem marcada (base64)
    ▼
Celular (browser)
    │ exibe tabela de sementes
    │ exibe imagem com contornos marcados
    └ botão para baixar PDF  →  GET /relatorio
```

---

## Testando sem celular (com Postman ou curl)

```bash
curl -X POST http://localhost:5000/analisar \
  -F "imagem=@sua_foto.jpg"
```