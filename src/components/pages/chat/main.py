import streamlit as st
from typing import Optional
import time

from services.ai_api import ai_service, AIAPIError


def chat_ia():
    # Configuração da página
    st.title("💬 Chat com IA")
    st.markdown("Converse naturalmente com o assistente do hospital")

    # Inicializar histórico do chat
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Verificar status da IA
    try:
        ai_status = ai_service.check_health()
        if ai_status:
            st.success("🟢 IA Online")
        else:
            st.error("🔴 IA Offline")
            return
    except:
        st.error("🔴 Não foi possível conectar com a IA")
        return

    # Exibir histórico do chat
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Input do usuário
    if prompt := st.chat_input("Digite sua mensagem..."):
        # Adicionar mensagem do usuário ao histórico
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Exibir mensagem do usuário
        with st.chat_message("user"):
            st.markdown(prompt)

        # Obter resposta da IA
        with st.chat_message("assistant"):
            with st.spinner("Pensando..."):
                try:
                    # Usar endpoint simples por padrão
                    response = ai_service.simple_question(prompt)

                    if response:
                        st.markdown(response)
                        # Adicionar resposta ao histórico
                        st.session_state.messages.append({"role": "assistant", "content": response})
                    else:
                        error_msg = "Desculpe, não consegui processar sua pergunta."
                        st.markdown(error_msg)
                        st.session_state.messages.append({"role": "assistant", "content": error_msg})

                except Exception as e:
                    error_msg = f"Erro: {str(e)}"
                    st.error(error_msg)
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})

    # Botão para limpar chat (posicionado no final)
    if st.session_state.messages:
        if st.button("Limpar Chat", type="secondary"):
            st.session_state.messages = []
            st.rerun()


# Função para integração com o app principal
def assistente_ia():
    """Função compatível com o sistema de navegação existente"""
    chat_ia()


if __name__ == "__main__":
    # Para teste independente
    chat_ia()