import streamlit as st
import pandas as pd
from utils.pdf_reader import extrair_texto_pdf

st.set_page_config(page_title="RM-FISCAL", layout="wide")
st.title("📁 RM-FISCAL – Leitura e Validação de Arquivos")

colunas_obrigatorias = ["Data", "CNPJ", "CFOP", "NCM", "Valor"]
uploaded_file = st.file_uploader("Selecione um arquivo Excel ou PDF", type=["xlsx", "pdf"])

if uploaded_file:
    file_name = uploaded_file.name
    st.success(f"Arquivo carregado: {file_name}")

    if file_name.endswith(".xlsx"):
        try:
            df = pd.read_excel(uploaded_file)
            st.subheader("Colunas encontradas na planilha:")
            st.write(list(df.columns))

            colunas_faltando = [col for col in colunas_obrigatorias if col not in df.columns]

            if colunas_faltando:
                st.error(f"⚠️ As seguintes colunas obrigatórias estão faltando: {colunas_faltando}")
            else:
                st.success("✅ Todas as colunas obrigatórias foram encontradas.")
                st.subheader("Prévia dos dados:")
                st.dataframe(df, use_container_width=True)
        except Exception as e:
            st.error(f"Erro ao ler o arquivo Excel: {e}")

    elif file_name.endswith(".pdf"):
        try:
            texto = extrair_texto_pdf(uploaded_file)
            st.subheader("Texto extraído do PDF:")
            for i, pagina in enumerate(texto):
                st.markdown(f"**Página {i+1}:**")
                st.text(pagina)
        except Exception as e:
            st.error(f"Erro ao ler o PDF: {e}")