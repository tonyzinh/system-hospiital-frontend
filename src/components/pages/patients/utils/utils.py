def normalize_patients_data(raw):
    """
    Normalizar resposta da API: garantir que `patients` seja uma lista de dicionários
    """
    if not raw:
        return []
    if isinstance(raw, list):
        return raw
    if isinstance(raw, dict):
        # procura campos comuns de paginação/agrupamento
        for k in ("results", "data", "items", "patients"):
            if k in raw and isinstance(raw[k], list):
                return raw[k]
        # se for um único paciente (dict com 'id'), envolvê-lo em lista
        if "id" in raw:
            return [raw]
    # se veio como string ou outro tipo, retornar lista vazia
    return []


def filter_patients_by_search(patients, search_term):
    """
    Filtrar lista de pacientes por termo de busca
    """
    if not search_term or not patients:
        return patients

    return [
        p for p in patients if search_term.lower() in p.get("full_name", "").lower()
    ]


def initialize_session_state():
    """
    Inicializar estados da sessão para pacientes
    """
    import streamlit as st

    if "editing_patient" not in st.session_state:
        st.session_state.editing_patient = None
    if "show_patient_modal" not in st.session_state:
        st.session_state.show_patient_modal = False
    if "patient_form_data" not in st.session_state:
        st.session_state.patient_form_data = None
    if "deleting_patient" not in st.session_state:
        st.session_state.deleting_patient = None
    if "show_delete_confirmation" not in st.session_state:
        st.session_state.show_delete_confirmation = False
    if "confirm_delete" not in st.session_state:
        st.session_state.confirm_delete = False

    # Ensure only one modal can be open at a time
    if (
        st.session_state.show_patient_modal
        and st.session_state.show_delete_confirmation
    ):
        st.session_state.show_delete_confirmation = False


def find_patient_by_id(patients, patient_id):
    """
    Buscar paciente por ID na lista
    """
    return next((p for p in patients if p.get("id") == patient_id), None)
