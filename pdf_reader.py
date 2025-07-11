import pdfplumber

def extrair_texto_pdf(arquivo_pdf):
    texto = []
    with pdfplumber.open(arquivo_pdf) as pdf:
        for page in pdf.pages:
            txt = page.extract_text()
            if txt:
                texto.append(txt)
    return texto