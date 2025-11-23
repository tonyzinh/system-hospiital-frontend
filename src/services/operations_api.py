import requests
import streamlit as st
from config import API_BASE_URL


class OperationsAPI:
    def __init__(self, base_url=API_BASE_URL):
        self.base_url = base_url

    def get_process_tasks(self):
        """Busca todas as tarefas de processo"""
        try:
            response = requests.get(f"{self.base_url}/process-tasks/")
            response.raise_for_status()
            raw = response.json()
            # debug helper
            if st.session_state.get("debug_api"):
                st.write("DEBUG: raw process tasks response:", raw)

            # Normalizar uma lista de tarefas
            if isinstance(raw, list):
                return raw
            if isinstance(raw, dict):
                for k in ("results", "data", "items", "process_tasks"):
                    if k in raw and isinstance(raw[k], list):
                        return raw[k]
                # se for um dict único com 'id', retorná-lo como lista
                if "id" in raw:
                    return [raw]
            # caso inesperado
            return []
        except requests.exceptions.RequestException as e:
            st.error(f"Erro ao buscar tarefas de processo: {e}")
            return []

    def get_process_task(self, task_id):
        """Busca uma tarefa específica"""
        try:
            response = requests.get(f"{self.base_url}/process-tasks/{task_id}/")
            response.raise_for_status()
            raw = response.json()
            if st.session_state.get("debug_api"):
                st.write("DEBUG: raw process task response:", raw)
            # se veio como lista, pegar primeiro elemento
            if isinstance(raw, list) and raw:
                return raw[0]
            if isinstance(raw, dict):
                return raw
            return None
        except requests.exceptions.RequestException as e:
            st.error(f"Erro ao buscar tarefa: {e}")
            return None

    def create_process_task(self, task_data):
        """Cria uma nova tarefa de processo"""
        try:
            response = requests.post(f"{self.base_url}/process-tasks/", json=task_data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            st.error(f"Erro ao criar tarefa: {e}")
            return None

    def update_process_task(self, task_id, task_data):
        """Atualiza uma tarefa existente"""
        try:
            response = requests.put(
                f"{self.base_url}/process-tasks/{task_id}/", json=task_data
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            st.error(f"Erro ao atualizar tarefa: {e}")
            return None

    def delete_process_task(self, task_id):
        """Remove uma tarefa"""
        try:
            response = requests.delete(f"{self.base_url}/process-tasks/{task_id}/")
            response.raise_for_status()
            return True
        except requests.exceptions.RequestException as e:
            st.error(f"Erro ao deletar tarefa: {e}")
            return False

    def update_task_status(self, task_id, status):
        """Atualiza apenas o status de uma tarefa"""
        try:
            # Primeiro buscar a tarefa atual para manter outros dados
            current_task = self.get_process_task(task_id)
            if not current_task:
                return None

            # Atualizar apenas o status
            current_task["status"] = status
            return self.update_process_task(task_id, current_task)
        except Exception as e:
            st.error(f"Erro ao atualizar status da tarefa: {e}")
            return None

    def start_task(self, task_id):
        """Inicia uma tarefa (atualiza status para 'in_progress')"""
        return self.update_task_status(task_id, "in_progress")

    def complete_task(self, task_id):
        """Completa uma tarefa (atualiza status para 'completed')"""
        return self.update_task_status(task_id, "completed")

    def cancel_task(self, task_id):
        """Cancela uma tarefa (atualiza status para 'cancelled')"""
        return self.update_task_status(task_id, "cancelled")
