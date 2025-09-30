import random
import string
from datetime import datetime
import streamlit as st

ARQUIVO = "codigos.txt"

def gerar_codigo(ano):
    ultimos_digitos = ano[-2:]
    N = str(random.randint(0, 9))
    A = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(5))
    return N + A + ultimos_digitos

def salvar_codigos(data, codigos):
    with open(ARQUIVO, "a", encoding="utf-8") as f:
        f.write(f"\n=== {data} ===\n")
        for i, codigo in enumerate(codigos, start=1):
            f.write(f"{i} - {codigo}\n")

def ver_codigos_por_data(data):
    try:
        with open(ARQUIVO, "r", encoding="utf-8") as f:
            linhas = f.readlines()

        mostrar = False
        encontrados = []
        for linha in linhas:
            linha = linha.strip()
            if linha == f"=== {data} ===":
                mostrar = True
                continue
            if linha.startswith("===") and mostrar:
                break
            if mostrar and linha:
                encontrados.append(linha)
        return encontrados
    except FileNotFoundError:
        return []

# --- Streamlit App ---
st.set_page_config(page_title="Gerador de Códigos", layout="centered")

st.title("⚡ Gerador de Códigos")

# Entrada de dados
ano = st.text_input("Ano", value=str(datetime.now().year))
qtd = st.number_input("Quantidade de códigos", min_value=1, max_value=100, value=1)

if st.button("Gerar Código(s)"):
    codigos = [gerar_codigo(ano) for _ in range(qtd)]
    data_hoje = datetime.now().strftime("%d/%m/%Y")

    st.subheader("✅ Códigos Gerados:")
    for i, codigo in enumerate(codigos, start=1):
        st.code(f"{i} - {codigo}")

    salvar_codigos(data_hoje, codigos)
    st.success(f"{qtd} código(s) salvos para a data {data_hoje}.")

# Consultar histórico
st.subheader("📅 Consultar Histórico")
data = st.text_input("Digite a data (dd/mm/aaaa)")

if st.button("Ver códigos dessa data"):
    encontrados = ver_codigos_por_data(data)
    if encontrados:
        st.subheader(f"Códigos de {data}:")
        for linha in encontrados:
            st.code(linha)
    else:
        st.warning(f"Nenhum código encontrado para {data}.")
