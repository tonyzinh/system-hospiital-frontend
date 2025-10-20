import streamlit as st
from components.pages.patients.main import pacientes


def dashboard():
    """Página Dashboard"""
    st.title("Dashboard")
    st.info("Dashboard em desenvolvimento...")


def medicamentos():
    """Página Medicamentos"""
    st.title("Medicamentos")
    st.info("Página de medicamentos em desenvolvimento...")


def operacoes():
    """Página Operações"""
    st.title("Operações")
    st.info("Página de operações em desenvolvimento...")


def assistente_ia():
    """Página Assistente IA"""
    st.title("Assistente IA")
    st.info("Assistente IA em desenvolvimento...")


# Configuração da página
st.set_page_config(page_title="Sistema Hospitalar", layout="wide")

# Páginas do sistema
pages = [
    st.Page(dashboard, title="Dashboard"),
    st.Page(pacientes, title="Pacientes"),
    st.Page(medicamentos, title="Medicamentos"),
    st.Page(operacoes, title="Operações"),
    st.Page(assistente_ia, title="Assistente IA"),
]

# Navegação
navegacao = st.navigation(pages, position="top")
navegacao.run()
