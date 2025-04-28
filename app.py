# app.py
import streamlit as st
import pytesseract
from PIL import Image
import requests
from transformers import pipeline
import datetime

# Configuração da página
st.set_page_config(page_title="Know Your Fan | FURIA",
                   page_icon='images/logo.png')

st.markdown(
    """
    <div style="text-align: center; margin-top: 5px; margin-bottom: 20px;">
        <img src="https://furiagg.fbitsstatic.net/sf/img/logo-furia.svg?theme=main&v=202503171541" alt="Logo" width="250">
    </div>
    """,
    unsafe_allow_html=True
)

st.title("🎮 Know Your Fan")
st.subheader("Cadastro do Fã de eSports")

# Formulário de Dados Básicos
with st.form(key="basic_form"):
    name = st.text_input("Nome completo")
    birth_date = st.date_input("Data de Nascimento"
                               ,min_value=datetime.date(1900, 1, 1),
                               max_value=datetime.date.today()
                               )
    address = st.text_input("Endereço")
    cpf = st.text_input("CPF")
    interests = st.text_area("Interesses em eSports")
    submitted = st.form_submit_button("Salvar Informações")

    if submitted:
        st.success("Informações salvas!")

st.divider()

# Upload de Documento
st.subheader("📄 Validação de Documento")
uploaded_file = st.file_uploader("Envie seu documento (imagem)", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Documento enviado", use_column_width=True)

    # OCR para extrair texto
    text_extracted = pytesseract.image_to_string(image)
    st.write("Texto extraído do documento:")
    st.code(text_extracted)

    # Validação simples (checando se nome ou CPF aparecem no texto)
    if name.lower() in text_extracted.lower() and cpf in text_extracted:
        st.success("✅ Documento validado!")
    else:
        st.error("❌ Documento inválido ou informações não conferem.")

st.divider()

# Análise de Perfil de eSports
st.subheader("🔗 Análise de Links de Perfil de eSports")
url = st.text_input("Cole o link de perfil ou conteúdo sobre eSports")

if st.button("Analisar Link"):
    # Simulação: baixando o conteúdo do link (ideal seria scraping real)
    st.info("Simulando análise do conteúdo...")
    sample_text = "FURIA vence campeonato de CS:GO e encanta fãs."

    # Classificador usando modelo HuggingFace
    classifier = pipeline("text-classification", model="distilbert-base-uncased-finetuned-sst-2-english")

    result = classifier(sample_text)[0]
    label = result['label']
    score = result['score']

    if label == "POSITIVE" and score > 0.7:
        st.success(f"✅ Conteúdo relevante para eSports! (Confiança: {score:.2f})")
    else:
        st.warning(f"⚠️ Conteúdo não diretamente relacionado. (Confiança: {score:.2f})")
