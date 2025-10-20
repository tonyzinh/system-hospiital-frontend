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
        self.timeout = 120  # 2 minutos de timeout

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
            response = requests.post(
                url,
                json=data,
                timeout=self.timeout,
                headers={'Content-Type': 'application/json'}
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

    def check_health(self) -> bool:
        """
        Verifica se o serviço de IA está funcionando

        Returns:
            True se o serviço estiver funcionando, False caso contrário
        """
        try:
            url = f"{self.base_url}/ai/health"
            response = requests.get(url, timeout=10)

            if response.status_code == 200:
                data = response.json()
                return data.get('status') == 'healthy'
            return False

        except Exception:
            return False

    def simple_question(self, question: str, model: Optional[str] = None) -> str:
        """
        Faz uma pergunta simples para a IA

        Args:
            question: Pergunta a ser feita
            model: Modelo específico a usar (opcional)

        Returns:
            Resposta da IA
        """
        data = {"question": question}
        if model:
            data["model"] = model

        response = self._make_request("ai/answer", data)
        return response.get("answer", "")

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

    def chat_with_history(self, question: str, history: List[Dict[str, str]],
                         model: Optional[str] = None) -> str:
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