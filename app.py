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

def salvar_codigos(data_hora, codigos):
    with open(ARQUIVO, "a", encoding="utf-8") as f:
        f.write(f"\n=== {data_hora} ===\n")
        for i, codigo in enumerate(codigos, start=1):
            f.write(f"{i} - {codigo}\n")

def ver_codigos_por_data(data):
    try:
        with open(ARQUIVO, "r", encoding="utf-8") as f:
            linhas = f.readlines()

        mostrar = False
        encontrados = {}
        chave_atual = None
        for linha in linhas:
            linha = linha.strip()
            if linha.startswith("===") and data in linha:
                mostrar = True
                chave_atual = linha
                encontrados[chave_atual] = []
                continue
            if linha.startswith("===") and mostrar:
                mostrar = False
            if mostrar and linha:
                encontrados[chave_atual].append(linha)
        return encontrados
    except FileNotFoundError:
        return {}

def apagar_codigos(data_hora):
    try:
        with open(ARQUIVO, "r", encoding="utf-8") as f:
            linhas = f.readlines()

        with open(ARQUIVO, "w", encoding="utf-8") as f:
            skip = False
            for linha in linhas:
                if linha.strip() == f"=== {data_hora} ===":
                    skip = True
                    continue
                if linha.startswith("===") and skip:
                    skip = False
                if not skip:
                    f.write(linha)
    except FileNotFoundError:
        pass

# --- Streamlit App ---
st.set_page_config(page_title="Gerador de Códigos", layout="centered")
st.title("⚡ Gerador de Códigos")

# Entrada de dados
ano = st.text_input("Ano", value=str(datetime.now().year))
qtd = st.number_input("Quantidade de códigos", min_value=1, max_value=100, value=1)

if st.button("Gerar Código(s)"):
    codigos = [gerar_codigo(ano) for _ in range(qtd)]
    data_hora = datetime.now().strftime("%H:%M %d/%m/%Y")

    st.subheader("✅ Códigos Gerados:")
    for i, codigo in enumerate(codigos, start=1):
        st.code(f"{i} - {codigo}")

    salvar_codigos(data_hora, codigos)
    st.success(f"{qtd} código(s) salvos para {data_hora}.")

# Consultar histórico com calendário
st.subheader("📅 Consultar Histórico")
data_selecionada = st.date_input("Selecione a data")

if st.button("Ver códigos dessa data"):
    data_formatada = data_selecionada.strftime("%d/%m/%Y")
    encontrados = ver_codigos_por_data(data_formatada)
    if encontrados:
        for chave, lista in encontrados.items():
            st.markdown(f"### {chave}")
            for linha in lista:
                st.code(linha)
    else:
        st.warning(f"Nenhum código encontrado para {data_formatada}.")

# Função apagar códigos
st.subheader("🗑️ Apagar códigos")
data_para_apagar = st.text_input("Digite data e hora ex: 12:30 30/09/2025")
if st.button("Apagar códigos dessa data/hora"):
    apagar_codigos(data_para_apagar)
    st.success(f"Códigos apagados para {data_para_apagar}")
