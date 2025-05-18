import streamlit as st
import pandas as pd
from utils.pdf_reader import extrair_texto_pdf

st.set_page_config(page_title="RM-FISCAL", layout="wide")

st.title("RM-FISCAL - Leitura e Visualização de Arquivos")

menu = st.sidebar.radio("Menu", ["Leitura Excel", "Leitura PDF"])

if menu == "Leitura Excel":
    st.header("Importar Arquivo Excel")
    arquivo_excel = st.file_uploader("Escolha um arquivo Excel", type=["xlsx"])
    if arquivo_excel:
        df = pd.read_excel(arquivo_excel)
        st.success("Arquivo carregado com sucesso!")
        st.dataframe(df)

elif menu == "Leitura PDF":
    st.header("Importar Arquivo PDF")
    arquivo_pdf = st.file_uploader("Escolha um arquivo PDF", type=["pdf"])
    if arquivo_pdf:
        texto = extrair_texto_pdf(arquivo_pdf)
        st.success("PDF carregado com sucesso!")
        for i, pagina in enumerate(texto, start=1):
            st.subheader(f"Página {i}")
            st.text(pagina)