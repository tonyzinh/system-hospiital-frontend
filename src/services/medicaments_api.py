import requests
import streamlit as st
from config import API_BASE_URL


class MedicamentsAPI:
    def __init__(self, base_url=API_BASE_URL):
        self.base_url = base_url

    def get_medications(self):
        """Busca todos os medicamentos"""
        try:
            response = requests.get(f"{self.base_url}/medications/")
            response.raise_for_status()
            raw = response.json()
            
            if st.session_state.get("debug_api"):
                st.write("DEBUG: raw medications response:", raw)

            # Normalizar uma lista de medicamentos
            if isinstance(raw, list):
                return raw
            if isinstance(raw, dict):
                for k in ("results", "data", "items", "medications"):
                    if k in raw and isinstance(raw[k], list):
                        return raw[k]
                if "id" in raw:
                    return [raw]
            
            return []
        except requests.exceptions.RequestException as e:
            st.error(f"Erro ao buscar medicamentos: {e}")
            return []

    def get_medication(self, medication_id):
        """Busca um medicamento específico"""
        try:
            response = requests.get(f"{self.base_url}/medications/{medication_id}/")
            response.raise_for_status()
            raw = response.json()
            
            if st.session_state.get("debug_api"):
                st.write("DEBUG: raw medication response:", raw)
                
            if isinstance(raw, list) and raw:
                return raw[0]
            if isinstance(raw, dict):
                return raw
            return None
        except requests.exceptions.RequestException as e:
            st.error(f"Erro ao buscar medicamento: {e}")
            return None

    def create_medication(self, medication_data):
        """Cria um novo medicamento"""
        try:
            response = requests.post(f"{self.base_url}/medications/", json=medication_data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            st.error(f"Erro ao criar medicamento: {e}")
            return None

    def update_medication(self, medication_id, medication_data):
        """Atualiza um medicamento existente"""
        try:
            response = requests.put(
                f"{self.base_url}/medications/{medication_id}/", json=medication_data
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            st.error(f"Erro ao atualizar medicamento: {e}")
            return None

    def delete_medication(self, medication_id):
        """Remove um medicamento"""
        try:
            response = requests.delete(f"{self.base_url}/medications/{medication_id}/")
            response.raise_for_status()
            return True
        except requests.exceptions.RequestException as e:
            st.error(f"Erro ao deletar medicamento: {e}")
            return False