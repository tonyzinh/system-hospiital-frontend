import requests
import streamlit as st
from typing import Dict, Any, Optional, List
from components.config import API_BASE_URL


class AIAPIError(Exception):
    """Exceção customizada para erros da API de IA"""

    pass


class AIService:
    """Serviço para interação com endpoints de IA"""

    def __init__(self):
        self.base_url = API_BASE_URL
        self.timeout = 90  # 90 segundos máximo - prioriza velocidade
        self._original_timeout = 90  # Backup do timeout original

    def _make_request(self, endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Faz uma requisição para a API

        Args:
            endpoint: Endpoint da API
            data: Dados para enviar na requisição

        Returns:
            Resposta da API

        Raises:
            AIAPIError: Em caso de erro na API
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"

        try:
            # Usar timeout duplo: (conexão, leitura)
            timeout_tuple = (
                30,
                self.timeout,
            )  # 30s para conexão, self.timeout para leitura
            response = requests.post(
                url,
                json=data,
                timeout=timeout_tuple,
                headers={
                    "Content-Type": "application/json; charset=utf-8",
                    "Accept": "application/json",
                },
            )

            if response.status_code == 200:
                return response.json()
            else:
                error_msg = f"Erro {response.status_code}: {response.text}"
                raise AIAPIError(error_msg)

        except requests.exceptions.Timeout:
            raise AIAPIError("Timeout: A requisição demorou muito para responder")
        except requests.exceptions.ConnectionError:
            raise AIAPIError("Erro de conexão: Não foi possível conectar à API")
        except requests.exceptions.RequestException as e:
            raise AIAPIError(f"Erro na requisição: {str(e)}")

    def check_health(self) -> Dict[str, Any]:
        """
        Verifica se o serviço de IA está funcionando

        Returns:
            Dict com informações detalhadas do status
        """
        try:
            url = f"{self.base_url}/ai/health"
            # Timeout mais curto para health check (conexão, leitura)
            timeout_tuple = (5, 15)  # 5s conexão, 15s leitura
            response = requests.get(url, timeout=timeout_tuple)

            if response.status_code == 200:
                data = response.json()
                return {
                    "healthy": data.get("status") == "healthy",
                    "status": data.get("status"),
                    "details": data,
                }
            return {
                "healthy": False,
                "status": "unhealthy",
                "error": f"HTTP {response.status_code}",
            }

        except Exception as e:
            return {"healthy": False, "status": "error", "error": str(e)}

    def warmup_ollama(self) -> bool:
        """
        Força o pré-aquecimento do Ollama

        Returns:
            True se o warmup foi bem sucedido
        """
        try:
            url = f"{self.base_url}/ai/health"
            timeout_tuple = (5, 30)  # 30s para warmup
            response = requests.post(url, timeout=timeout_tuple)

            if response.status_code == 200:
                data = response.json()
                return data.get("status") == "ready"
            return False

        except Exception:
            return False

    def simple_question(self, question: str, model: Optional[str] = None) -> str:
        """
        Faz uma pergunta simples para a IA com sistema de fallback

        Args:
            question: Pergunta a ser feita
            model: Modelo específico a usar (opcional)

        Returns:
            Resposta da IA
        """
        data = {"question": question}
        if model:
            data["model"] = model

        # Primeiro, tenta com timeout menor para perguntas rápidas
        try:
            # Salva o timeout original
            original_timeout = self.timeout

            # Para perguntas curtas, usa timeout menor
            if len(question) < 50:
                self.timeout = 60  # 1 minuto para perguntas curtas

            response = self._make_request("ai/answer", data)
            return response.get("answer", "")

        except AIAPIError as e:
            # Restaura timeout original
            self.timeout = original_timeout

            # Se foi timeout e a pergunta é mais longa, tenta novamente
            if "timeout" in str(e).lower() and len(question) >= 50:
                try:
                    response = self._make_request("ai/answer", data)
                    return response.get("answer", "")
                except AIAPIError:
                    # Se ainda falhou, sugere usar advanced
                    raise AIAPIError(
                        "Pergunta complexa detectada. Tente reformular de forma mais simples ou use o modo avançado."
                    )

            raise e
        finally:
            # Sempre restaura o timeout original
            self.timeout = getattr(self, "_original_timeout", 300)

    def advanced_question(self, question: str, model: Optional[str] = None) -> str:
        """
        Faz uma pergunta avançada para a IA

        Args:
            question: Pergunta a ser feita
            model: Modelo específico a usar (opcional)

        Returns:
            Resposta da IA
        """
        data = {"question": question}
        if model:
            data["model"] = model

        response = self._make_request("ai/answer-advanced", data)
        return response.get("answer", "")

    def chat_with_history(
        self, question: str, history: List[Dict[str, str]], model: Optional[str] = None
    ) -> str:
        """
        Faz uma pergunta considerando o histórico da conversa

        Args:
            question: Pergunta atual
            history: Histórico de mensagens
            model: Modelo específico a usar (opcional)

        Returns:
            Resposta da IA
        """
        # Nota: O backend tem um AiChatView que aceita histórico,
        # mas não está nas URLs. Por agora, usaremos o advanced_question
        return self.advanced_question(question, model)


# Instância global do serviço
ai_service = AIService()
