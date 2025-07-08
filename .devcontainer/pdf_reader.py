import pdfplumber

def extrair_texto_pdf(arquivo_pdf):
    texto_paginas = []
    with pdfplumber.open(arquivo_pdf) as pdf:
        for pagina in pdf.pages:
            texto = pagina.extract_text()
            if texto:
                texto_paginas.append(texto)
    return texto_paginas