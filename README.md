# RM-FISCAL

Aplicação em Streamlit para leitura e validação de arquivos fiscais em Excel e PDF.

## Como executar

1. Crie um ambiente virtual (opcional)
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate   # Windows
```

2. Instale as dependências
```bash
pip install -r requirements.txt
```

3. Execute o app
```bash
streamlit run app.py
```

## Estrutura esperada do Excel
- Colunas obrigatórias: `Data`, `CNPJ`, `CFOP`, `NCM`, `Valor`