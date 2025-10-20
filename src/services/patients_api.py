import requests
import streamlit as st
from config import API_BASE_URL


class PatientsAPI:
    def __init__(self, base_url=API_BASE_URL):
        self.base_url = base_url

    def get_patients(self):
        """Busca todos os pacientes"""
        try:
            response = requests.get(f"{self.base_url}/patients/")
            response.raise_for_status()
            raw = response.json()
            # debug helper
            if st.session_state.get("debug_api"):
                st.write("DEBUG: raw patients response:", raw)

            # Normalizar uma lista de pacientes
            if isinstance(raw, list):
                return raw
            if isinstance(raw, dict):
                for k in ("results", "data", "items", "patients"):
                    if k in raw and isinstance(raw[k], list):
                        return raw[k]
                # se for um dict único com 'id', retorná-lo como lista
                if "id" in raw:
                    return [raw]
            # caso inesperado
            return []
        except requests.exceptions.RequestException as e:
            st.error(f"Erro ao buscar pacientes: {e}")
            return []

    def get_patient(self, patient_id):
        """Busca um paciente específico"""
        try:
            response = requests.get(f"{self.base_url}/patients/{patient_id}/")
            response.raise_for_status()
            raw = response.json()
            if st.session_state.get("debug_api"):
                st.write("DEBUG: raw patient response:", raw)
            # se veio como lista, pegar primeiro elemento
            if isinstance(raw, list) and raw:
                return raw[0]
            if isinstance(raw, dict):
                return raw
            return None
        except requests.exceptions.RequestException as e:
            st.error(f"Erro ao buscar paciente: {e}")
            return None

    def create_patient(self, patient_data):
        """Cria um novo paciente"""
        try:
            response = requests.post(f"{self.base_url}/patients/", json=patient_data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            st.error(f"Erro ao criar paciente: {e}")
            return None

    def update_patient(self, patient_id, patient_data):
        """Atualiza um paciente existente"""
        try:
            response = requests.put(
                f"{self.base_url}/patients/{patient_id}/", json=patient_data
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            st.error(f"Erro ao atualizar paciente: {e}")
            return None

    def delete_patient(self, patient_id):
        """Remove um paciente"""
        try:
            response = requests.delete(f"{self.base_url}/patients/{patient_id}/")
            response.raise_for_status()
            return True
        except requests.exceptions.RequestException as e:
            st.error(f"Erro ao deletar paciente: {e}")
            return False
