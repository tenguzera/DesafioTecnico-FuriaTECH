# 🧠 Know Your Fan – Desafio Técnico FURIA

Este é um projeto desenvolvido para o desafio técnico da FURIA, com o objetivo de conhecer melhor os fãs de e-sports por meio da coleta de dados e análise de interações sociais, utilizando inteligência artificial.

---

## ✨ Funcionalidades

- Formulário de múltiplas etapas com validações (nome, CPF, nascimento, interesses, etc.)
- Upload e validação de documento com OCR (nome e CPF)
- Autenticação com API do Twitter/X
- Leitura de atividades nas redes sociais (como mencionar a FURIA nos últimos tweets)
- Recomendação personalizada de conteúdo com base nas respostas
- Armazenamento dos dados do usuário em um backend Flask
- Design responsivo com Streamlit

---

## 📦 Tecnologias utilizadas

- [Streamlit](https://streamlit.io/) – Frontend interativo com Python
- [Flask](https://flask.palletsprojects.com/) – API para armazenamento de dados
- [Pytesseract](https://github.com/madmaze/pytesseract) – OCR para leitura de documentos
- [Twitter API v2](https://developer.twitter.com/en/docs) – Integração com redes sociais

---

## ⚙️ Requisitos

- Python 3.8+
- Tesseract OCR instalado e disponível no PATH
- Contas de desenvolvedor no [Twitter Developer Portal](https://developer.twitter.com/)

---

## 🚀 Como rodar o projeto localmente

### 1. Clone o repositório

```bash
git clone https://github.com/tenguzera/DesafioTecnico-FuriaTECH.git
cd DesafioTecnico-FuriaTECH
```

### 2. Crie e ative um ambiente virtual

```bash
python -m venv venv
source venv/bin/activate  # no Windows: venv\Scripts\activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Instale o Tesseract OCR

- **Windows**: Baixe de [https://github.com/tesseract-ocr/tesseract](https://github.com/tesseract-ocr/tesseract)
- **Linux/macOS**: `sudo apt install tesseract-ocr`

**Obs:** É possível que seja necessário modificar o programa a depender de onde o tesseract foi instalado.

---

## 🧪 Executando o app

### 1. Inicie o backend Flask (em outro terminal):

```bash
python server.py
```

### 2. Inicie a interface Streamlit:

```bash
streamlit run app.py
```

---

## 📝 Estrutura do projeto

```
DesafioTecnico-FuriaTECH/
│
├── app.py                  # Frontend principal com Streamlit
├── funcoes.py              # Funções auxiliares (OCR, Twitter, etc.)
├── server.py               # API Flask para receber e armazenar os dados    
├── .streamlit/
│   └── config.toml         # Tema padrão (claro)
├── requirements.txt
└── README.md
```

---

## 🔐 Observações sobre as APIs

- A autenticação com Twitter/X segue o padrão OAuth 2.0.
- Nenhum token de acesso é armazenado no frontend — tudo é temporário em sessão.
- Os dados enviados são exclusivamente seus, usados para demonstração do desafio.

---