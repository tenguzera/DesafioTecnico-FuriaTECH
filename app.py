import streamlit as st
import pytesseract
import datetime
import re
from funcoes import *
from transformers import pipeline
from PIL import Image

bearer_token = "AAAAAAAAAAAAAAAAAAAAANkT1AEAAAAAZyfbCYniSFjo%2F5ZZW35eIMJ7J3c%3DVEdI9G59NuAhfqkjyJ1VdP3xfwfmz3U3wSSRmmEDE6WcaZiI5H"

# ------------------- Configuração da página -------------------
st.set_page_config(page_title="Know Your Fan | FURIA",
                   page_icon='images/logo.png')

# Inicializa o estado da etapa atual
if "step" not in st.session_state:
    st.session_state.step = 1

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

if st.session_state.get("step") == 1:
    st.title("Know Your Fan")
    st.subheader("Nos ajude a te conhecer melhor!")
elif st.session_state.get("step") == 6:
    st.title("Obrigado por responder!")
    st.subheader("Aqui estão alguns perfis que você pode se interessar:")

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

    generos = ["Masculino", "Feminino", "Outro", "Prefiro não informar"]
    st.session_state.genero = st.radio(
        "Gênero:",
        options=generos,
        index=generos.index(st.session_state.get("genero", "Prefiro não informar"))
        if st.session_state.get("genero") in generos else generos.index("Prefiro não informar"),
        horizontal=True
    )

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
        st.button("Próximo ➡️", on_click=next_step)

# ========================
# ETAPA 4 - Integração com redes sociais
# ========================
elif st.session_state.step == 4:
    st.header("Etapa 4: Integração com redes sociais")

    st.subheader("Vincule seu X/Twitter")

    username = st.text_input("Digite seu @ do X (sem o @)")
    st.session_state['twitter_username'] = username
    if st.button("Buscar dados do X"):
        with st.spinner("Buscando dados..."):
            dados, erro = get_twitter_data(username, bearer_token)
            if erro:
                st.error(erro)
            else:
                st.session_state.twitter_data = dados
                st.success("Dados coletados com sucesso!")
                st.write("📝 Tweets recentes:")
                for t in dados["tweets"]:
                    st.markdown(f"- {t['text']}")

                furia_mencionada = any("furia" in tweet["text"].lower() for tweet in dados["tweets"])
                st.session_state['furia_mencionada'] = furia_mencionada


    col1, col_spacer, col2 = st.columns([1, 5, 1])
    with col1:
        st.button("⬅️ Voltar", on_click=prev_step)
    with col2:
        st.button("Próximo ➡️", on_click=next_step)

# ========================
# ETAPA 5 - Upload de Documento
# ========================
elif st.session_state.step == 5:
    st.header("Etapa 5: Validação de Documento")

    uploaded_file = st.file_uploader("Envie seu documento (imagem)", type=["png", "jpg", "jpeg"])

    col1, col_spacer, col2 = st.columns([1, 5, 1])
    with col1:
        st.button("⬅️ Voltar", on_click=prev_step)
    with col2:
        st.empty()

    if uploaded_file is not None:
        image = Image.open(uploaded_file)

        # OCR para extrair texto
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        text_extracted = pytesseract.image_to_string(image)

        # Texto limpo
        texto_ocr_normalizado = normalize(text_extracted).replace('\n', ' ')

        # Nome do usuário limpo e dividido em palavras
        nome_usuario = normalize(st.session_state.name)
        palavras_nome = nome_usuario.split()

        # ------------------- CPF -------------------
        # Normaliza o texto extraído pelo OCR
        texto_limpo = text_extracted.replace('\n', ' ').replace(' ', '').replace('-', '').replace('.', '').replace('/', '')
        # Extrai todas as sequências de 11 dígitos (possíveis CPFs)
        possiveis_cpfs = re.findall(r'\d{11}', texto_limpo)
        # Verifica se o CPF está entre os extraídos
        cpf_valido = st.session_state.cpf in possiveis_cpfs

        # ------------------- Nome -------------------
        nome_valido = nome_validado(palavras_nome, texto_ocr_normalizado)

        if nome_valido and cpf_valido:
            st.success("✅ Documento validado com sucesso! Clique para finalizar.")
            with col2:
                submit = st.button("Finalizar ✅")
                if submit:
                    # Verifica se todos os campos obrigatórios estão preenchidos
                    campos_obrigatorios = [
                        st.session_state.get("name"),
                        st.session_state.get("birth_date"),
                        st.session_state.get("genero"),
                        st.session_state.get("cpf"),
                        st.session_state.get("email"),
                        st.session_state.get("estado"),
                        st.session_state.get("cidade"),
                        st.session_state.get("endereco"),
                        st.session_state.get("fav_org"),
                        st.session_state.get("jogos"),
                        st.session_state.get("plataformas"),
                        st.session_state.get("eventos"),
                        st.session_state.get("compras"),
                        st.session_state.get("twitter_username"),
                    ]

                    if all(campos_obrigatorios):
                        dados = {
                            "nome": st.session_state.name,
                            "data_nascimento": str(st.session_state.birth_date),
                            "genero": st.session_state.genero,
                            "cpf": st.session_state.cpf,
                            "email": st.session_state.email,
                            "estado": st.session_state.estado,
                            "cidade": st.session_state.cidade,
                            "endereco": st.session_state.endereco,
                            "organizacao_favorita": st.session_state.fav_org,
                            "jogos": st.session_state.jogos,
                            "plataformas": st.session_state.plataformas,
                            "eventos": st.session_state.eventos,
                            "compras": st.session_state.compras,
                            "usuario_twitter": st.session_state.twitter_username,
                            "furia_mencionada": st.session_state.get("furia_mencionada", False)
                        }

                        try:
                            response = requests.post("http://localhost:5000/salvar", json=dados)
                            if response.status_code == 200:
                                st.session_state.step += 1
                            else:
                                st.error(f"❌ Erro ao enviar os dados: {response.text}")
                        except Exception as e:
                            st.error(f"❌ Erro ao conectar com a API: {e}")
                    else:
                        st.error("⚠️ Por favor, preencha todos os campos antes de finalizar o formulário.")
        else:
            if not nome_valido:
                st.error("❌ Nome não encontrado no documento.")
            if not cpf_valido:
                st.error("❌ CPF não encontrado ou inválido no documento.")

# ========================
# ETAPA 6 - Recomendação de Perfis
# ========================
elif st.session_state.step == 6:
    resumo_usuario = (
        f"Eventos: {st.session_state['eventos']}. "
        f"Compras: {st.session_state['compras']}. "
        f"Joga: {', '.join(st.session_state['jogos'])}. "
        f"Usa as plataformas: {', '.join(st.session_state['plataformas'])}. "
        f"Organização favorita: {st.session_state['fav_org']}."
    )

    links_catalogo = [
        "https://pt.wikipedia.org/wiki/Furia_Esports",
        "https://en.wikipedia.org/wiki/Python_(programming_language)"
    ]

    for link in links_catalogo:
        texto = extrair_texto_url(link)
        if texto:
            similaridade = verificar_relevancia(texto, resumo_usuario)
            if similaridade > 0.2:
                st.success(f"🔗 Recomendado: {link}")
        else:
            st.error(f"❌ Não foi possível acessar: {link}")