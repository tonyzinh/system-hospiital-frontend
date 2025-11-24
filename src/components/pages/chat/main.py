import streamlit as st
from typing import Optional
import time

from services.ai_api import ai_service, AIAPIError


def is_complex_question(question: str) -> bool:
    """Detecta se a pergunta é complexa e pode demorar mais para responder"""
    complex_keywords = [
        "explique",
        "como funciona",
        "diferença",
        "comparação",
        "análise",
        "detalhadamente",
        "passo a passo",
        "tutorial",
        "exemplos",
        "processo",
        "diagnóstico",
        "tratamento",
    ]

    question_lower = question.lower()
    return (
        len(question) > 100  # Perguntas longas
        or any(keyword in question_lower for keyword in complex_keywords)
        or "?" in question
        and len(question.split("?")) > 2  # Múltiplas perguntas
    )


def chat_ia():
    # Configuração da página
    st.title("Chatbot")
    st.markdown("Converse naturalmente com o assistente do hospital")

    # Informações na sidebar
    with st.sidebar:
        st.info(
            "**Tempos de Resposta Otimizados**\n\n"
            "• Perguntas simples: 10-30 segundos\n"
            "• Perguntas médicas: 30-60 segundos\n"
            "• Perguntas complexas: até 90 segundos\n"
            "• Use frases diretas para respostas mais rápidas"
        )

        if st.button("Testar Conexão"):
            with st.spinner("Testando..."):
                health_info = ai_service.check_health()
                if health_info.get("healthy"):
                    st.success("Conectado!")
                else:
                    st.error("Desconectado")
                    st.write(f"Erro: {health_info.get('error', 'Desconhecido')}")

        if st.button("Pré-aquecer Sistema"):
            with st.spinner("Pré-aquecendo..."):
                if ai_service.warmup_ollama():
                    st.success("Sistema aquecido!")
                else:
                    st.error("Falha no aquecimento")

    # Inicializar histórico do chat
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Verificar status da IA
    try:
        health_info = ai_service.check_health()

        if health_info.get("healthy"):
            details = health_info.get("details", {})
            if details.get("warmed_up"):
                st.success("Online - Sistema pré-aquecido e pronto")
            elif details.get("ready"):
                st.success("Online - Sistema pronto para uso")
            else:
                st.success("Online - Ollama conectado")
        else:
            error = health_info.get("error", "Status desconhecido")
            st.error(f"Offline - {error}")

            # Botão para tentar pré-aquecimento
            if st.button("Tentar Pré-aquecimento"):
                with st.spinner("Pré-aquecendo o sistema..."):
                    if ai_service.warmup_ollama():
                        st.success("Pré-aquecimento concluído!")
                        st.rerun()
                    else:
                        st.error("Falha no pré-aquecimento")

            st.info("Para iniciar o Ollama, execute: `ollama serve` no terminal")
            return

    except Exception as e:
        st.error("Não foi possível conectar com a IA")
        st.error(f"Detalhes: {str(e)}")
        st.info("Verifique se o backend está rodando e se o Ollama está disponível")
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
            message_placeholder = st.empty()

            try:
                # Detectar complexidade da pergunta
                is_complex = is_complex_question(prompt)

                if is_complex:
                    spinner_text = (
                        "Processando pergunta... Isso pode demorar alguns minutos."
                    )
                    endpoint_func = ai_service.advanced_question
                else:
                    spinner_text = "Processando sua pergunta..."
                    endpoint_func = ai_service.simple_question

                with st.spinner(spinner_text):
                    # Usar endpoint apropriado baseado na complexidade
                    response = endpoint_func(prompt)

                    if response:
                        message_placeholder.markdown(response)
                        # Adicionar resposta ao histórico
                        st.session_state.messages.append(
                            {"role": "assistant", "content": response}
                        )
                    else:
                        error_msg = "Desculpe, não consegui processar sua pergunta. Tente novamente."
                        message_placeholder.markdown(f"{error_msg}")
                        st.session_state.messages.append(
                            {"role": "assistant", "content": error_msg}
                        )

            except AIAPIError as e:
                error_details = str(e)
                if "Timeout" in error_details:
                    error_msg = "A resposta está demorando mais que o esperado. Isso pode acontecer com perguntas complexas. Tente uma pergunta mais simples ou aguarde um momento."
                elif "502" in error_details:
                    error_msg = "O serviço de IA está temporariamente indisponível. Tente novamente em alguns instantes."
                else:
                    error_msg = f"Erro na comunicação: {error_details}"

                message_placeholder.markdown(error_msg)
                st.session_state.messages.append(
                    {"role": "assistant", "content": error_msg}
                )

            except Exception as e:
                error_msg = f"Erro inesperado: {str(e)}"
                message_placeholder.markdown(error_msg)
                st.session_state.messages.append(
                    {"role": "assistant", "content": error_msg}
                )

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
