import streamlit as st
import unicodedata
import Levenshtein
import requests
from bs4 import BeautifulSoup
from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer("all-MiniLM-L6-v2")

# Funções de navegação
def next_step():
    st.session_state.step += 1

def prev_step():
    st.session_state.step -= 1

# Normaliza texto do formulário
def normalize(text):
    text = unicodedata.normalize('NFKD', text)
    text = ''.join([c for c in text if not unicodedata.combining(c)])
    return text.lower().strip()

# Válida nome do formulário com documento enviado
def nome_validado(palavras_nome, texto):
    for palavra in palavras_nome:
        correspondencias = [
            Levenshtein.ratio(palavra, palavra_ocr)
            for palavra_ocr in texto.split()
        ]
        if max(correspondencias, default=0) < 0.85:
            return False
    return True

# Extrai texto de uma url para recomendação
def extrair_texto_url(url):
    try:
        r = requests.get(url, timeout=10)
        soup = BeautifulSoup(r.text, 'html.parser')
        textos = soup.find_all(['p', 'h1', 'h2', 'li'])
        return " ".join(t.get_text(strip=True) for t in textos)
    except:
        return ""

# Verifica se um link tem relevância para um usuário
def verificar_relevancia(texto_pagina, perfil_usuario):
    emb1 = model.encode(texto_pagina, convert_to_tensor=True)
    emb2 = model.encode(perfil_usuario, convert_to_tensor=True)
    score = util.pytorch_cos_sim(emb1, emb2).item()
    return score