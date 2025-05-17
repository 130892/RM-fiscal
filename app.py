import streamlit as st
import pandas as pd
import os
import xml.etree.ElementTree as ET
import sqlite3
import fitz  # PyMuPDF
import pytesseract
import io
from PIL import Image
import plotly.express as px
from datetime import datetime

st.set_page_config(page_title="RM-FISCAL", layout="wide")
st.title("🧾 RM-FISCAL — Plataforma de Gestão Fiscal Automatizada")

# Inicializar banco SQLite
conn = sqlite3.connect("clientes.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS clientes (id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT, cnpj TEXT, data_cadastro TEXT)")
conn.commit()

# Funções utilitárias
def parse_xml(xml_file):
    ns = {'nfe': 'http://www.portalfiscal.inf.br/nfe'}
    tree = ET.parse(xml_file)
    root = tree.getroot()
    emit = root.find('.//nfe:emit', ns)
    dest = root.find('.//nfe:dest', ns)
    ide = root.find('.//nfe:ide', ns)
    produtos = root.findall('.//nfe:det', ns)

    dados = []
    for prod in produtos:
        prod_info = prod.find('nfe:prod', ns)
        dados.append({
            'CNPJ Emitente': emit.find('nfe:CNPJ', ns).text if emit.find('nfe:CNPJ', ns) is not None else '',
            'CNPJ Destinatário': dest.find('nfe:CNPJ', ns).text if dest.find('nfe:CNPJ', ns) is not None else '',
            'Data de Emissão': ide.find('nfe:dhEmi', ns).text[:10] if ide.find('nfe:dhEmi', ns) is not None else '',
            'Produto': prod_info.find('nfe:xProd', ns).text if prod_info.find('nfe:xProd', ns) is not None else '',
            'CFOP': prod_info.find('nfe:CFOP', ns).text if prod_info.find('nfe:CFOP', ns) is not None else '',
            'NCM': prod_info.find('nfe:NCM', ns).text if prod_info.find('nfe:NCM', ns) is not None else '',
            'Valor Total': float(prod_info.find('nfe:vProd', ns).text) if prod_info.find('nfe:vProd', ns) is not None else 0,
        })
    return dados

def calcular_impostos(df):
    df["ICMS"] = df["Valor Total"] * 0.18
    df["PIS"] = df["Valor Total"] * 0.0165
    df["COFINS"] = df["Valor Total"] * 0.076
    return df

def processar_pdf(pdf_file):
    texto_extraido = ""
    with fitz.open(stream=pdf_file.read(), filetype="pdf") as doc:
        for page in doc:
            texto_extraido += page.get_text()
    return texto_extraido[:1000]

# Upload de arquivos
st.sidebar.header("📂 Importar Arquivos")
tipo = st.sidebar.selectbox("Tipo de Arquivo", ["XML de NFe", "Planilha Excel", "PDF"])
uploaded_files = st.sidebar.file_uploader("Envie seus arquivos", type=["xml", "xlsx", "xls", "pdf"], accept_multiple_files=True)

dados_gerais = []

if uploaded_files:
    for file in uploaded_files:
        if tipo == "XML de NFe" and file.name.endswith(".xml"):
            dados = parse_xml(file)
            dados_gerais.extend(dados)
        elif tipo == "Planilha Excel" and (file.name.endswith(".xlsx") or file.name.endswith(".xls")):
            df_excel = pd.read_excel(file)
            dados_gerais.extend(df_excel.to_dict(orient='records'))
        elif tipo == "PDF" and file.name.endswith(".pdf"):
            texto = processar_pdf(file)
            st.text_area(f"Conteúdo extraído de {file.name}", texto, height=200)

if dados_gerais:
    df = pd.DataFrame(dados_gerais)
    df = calcular_impostos(df)

    st.success("✅ Arquivos processados com sucesso!")
    with st.expander("📊 Dados Consolidados"):
        st.dataframe(df)

    st.download_button("📥 Baixar Excel", data=df.to_csv(index=False).encode(), file_name="relatorio_fiscal.csv", mime="text/csv")

    with st.expander("📈 Indicadores Fiscais"):
        grafico = px.pie(df, values="Valor Total", names="CFOP", title="Distribuição por CFOP")
        st.plotly_chart(grafico)

# Cadastro de clientes
st.sidebar.header("👤 Cadastro de Clientes")
with st.sidebar.form("form_cliente"):
    nome = st.text_input("Nome")
    cnpj = st.text_input("CNPJ")
    if st.form_submit_button("Cadastrar"):
        cursor.execute("INSERT INTO clientes (nome, cnpj, data_cadastro) VALUES (?, ?, ?)", (nome, cnpj, datetime.now().strftime("%Y-%m-%d")))
        conn.commit()
        st.sidebar.success("Cliente cadastrado com sucesso!")

# Histórico de clientes
st.sidebar.markdown("---")
if st.sidebar.checkbox("📜 Ver clientes cadastrados"):
    clientes = pd.read_sql_query("SELECT * FROM clientes", conn)
    st.sidebar.dataframe(clientes)
