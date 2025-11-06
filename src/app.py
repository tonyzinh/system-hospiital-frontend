import streamlit as st
from components.pages.patients.main import pacientes
from components.pages.chat.main import assistente_ia as chat_assistente_ia
from components.pages.medicaments.main import medicamentos as medicamentos_page

def dashboard():
    """Página Dashboard"""
    st.title("Dashboard")
    st.info("Dashboard em desenvolvimento...")


def medicamentos():
    """Página Medicamentos"""
    medicamentos_page()


def operacoes():
    """Página Operações"""
    st.title("Operações")
    st.info("Página de operações em desenvolvimento...")


def assistente_ia():
    """Página Assistente IA"""
    chat_assistente_ia()


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
