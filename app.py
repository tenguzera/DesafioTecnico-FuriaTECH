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

# Inicializa o estado da etapa atual
if "step" not in st.session_state:
    st.session_state.step = 1

# Funções de navegação
def next_step():
    st.session_state.step += 1

def prev_step():
    st.session_state.step -= 1

st.markdown(
    f"""
    <style>
        .logo-wrapper {{
            display: flex;
            justify-content: center;
            align-items: center;
            margin-top: 20px;
            margin-bottom: 20px;
        }}
    </style>
    <div class="logo-wrapper">
        <img src="https://furiagg.fbitsstatic.net/sf/img/logo-furia.svg?theme=main&v=202503171541" width="250">
    </div>
    """,
    unsafe_allow_html=True
)

st.title("Know Your Fan")
st.subheader("Nos ajude a te conhecer melhor!")

# ========================
# ETAPA 1 - Informações pessoais
# ========================
if st.session_state.step == 1:
    st.header("Etapa 1: Informações Pessoais")

    st.session_state.name = st.text_input("Nome Completo:", st.session_state.get("name", ""))
    st.session_state.birth_date = st.date_input("Data de Nascimento:",
        value=st.session_state.get("birth_date", datetime.date(2000, 1, 1)),
        min_value=datetime.date(1900, 1, 1),
        max_value=datetime.date.today())

    cpf = st.text_input("CPF: (Somente Números)", st.session_state.get("cpf", ""))
    st.session_state.cpf = cpf  # Salva no estado
    # Validação imediata
    if cpf and (not cpf.isdigit() or len(cpf) != 11):
        st.warning("⚠️ O CPF deve conter exatamente 11 dígitos numéricos.")

    st.session_state.email = st.text_input("E-mail:", st.session_state.get("email", ""))

    estados_brasil = [
        "Acre", "Alagoas", "Amapá", "Amazonas", "Bahia", "Ceará",
        "Distrito Federal", "Espírito Santo", "Goiás", "Maranhão",
        "Mato Grosso", "Mato Grosso do Sul", "Minas Gerais", "Pará",
        "Paraíba", "Paraná", "Pernambuco", "Piauí", "Rio de Janeiro",
        "Rio Grande do Norte", "Rio Grande do Sul", "Rondônia",
        "Roraima", "Santa Catarina", "São Paulo", "Sergipe", "Tocantins"
    ]
    st.session_state.estado = st.selectbox(
        "Estado:",
        options=estados_brasil,
        index=estados_brasil.index(st.session_state.get("estado", "São Paulo")) if st.session_state.get(
            "estado") in estados_brasil else 0
    )

    st.session_state.cidade = st.text_input("Cidade:", st.session_state.get("cidade", ""))
    st.session_state.endereco = st.text_input("Endereço Completo:", st.session_state.get("endereco", ""))

    col1, col_spacer, col2 = st.columns([1, 5, 1])
    with col1:
        st.empty()
    with col2:
        st.button("Próximo ➡️", on_click=next_step)

# ========================
# ETAPA 2 - Interesses
# ========================
elif st.session_state.step == 2:
    st.header("Etapa 2: Interesses em eSports")

    st.session_state.fav_org = st.text_input("Organização favorita: (ex: FURIA)", st.session_state.get("fav_org", ""))
    st.session_state.jogos = st.multiselect("Quais jogos você acompanha?",
                                            ["CS2", "LoL", "Valorant", "Fortnite", "Free Fire", "Outros"],
                                            default=st.session_state.get("jogos", []))
    st.session_state.plataformas = st.multiselect("Onde você acompanha os jogos?",
                                                  ["Twitch", "YouTube", "TikTok", "Twitter/X", "Outros"],
                                                  default=st.session_state.get("plataformas", []))

    col1, col_spacer, col2 = st.columns([1, 5, 1])
    with col1:
        st.button("⬅️ Voltar", on_click=prev_step)
    with col2:
        st.button("Próximo ➡️", on_click=next_step)

# ========================
# ETAPA 3 - Participação
# ========================
elif st.session_state.step == 3:
    st.header("Etapa 3: Eventos e Compras")

    st.session_state.eventos = st.text_area("Eventos de eSports que participou no último ano:",
                                            st.session_state.get("eventos", ""))
    st.session_state.compras = st.text_area("Produtos ou serviços que comprou relacionados a eSports:",
                                            st.session_state.get("compras", ""))

    col1, col_spacer, col2 = st.columns([1, 5, 1])
    with col1:
        st.button("⬅️ Voltar", on_click=prev_step)
    with col2:
        submit = st.button("Finalizar ✅")

    if submit:
         # Verifica se todos os campos obrigatórios estão preenchidos
           campos_obrigatorios = [
               st.session_state.get("name"),
               st.session_state.get("birth_date"),
               st.session_state.get("cpf"),
               st.session_state.get("email"),
               st.session_state.get("estado"),
               st.session_state.get("endereco"),
               st.session_state.get("fav_org"),
               st.session_state.get("jogos"),
               st.session_state.get("plataformas"),
               st.session_state.get("eventos"),
               st.session_state.get("compras")
           ]

           if all(campos_obrigatorios):
               dados = {
                   "nome": st.session_state.name,
                   "data_nascimento": str(st.session_state.birth_date),
                   "cpf": st.session_state.cpf,
                   "email": st.session_state.email,
                   "estado": st.session_state.estado,
                   "endereco": st.session_state.endereco,
                   "organizacao_favorita": st.session_state.fav_org,
                   "jogos": st.session_state.jogos,
                   "plataformas": st.session_state.plataformas,
                   "eventos": st.session_state.eventos,
                   "compras": st.session_state.compras
               }

               try:
                   response = requests.post("http://localhost:5000/salvar", json=dados)
                   if response.status_code == 200:
                       st.success("✅ Dados enviados com sucesso ao servidor!")
                   else:
                       st.error(f"❌ Erro ao enviar os dados: {response.text}")
               except Exception as e:
                   st.error(f"❌ Erro ao conectar com a API: {e}")
           else:
               st.error("⚠️ Por favor, preencha todos os campos antes de finalizar o formulário.")

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

