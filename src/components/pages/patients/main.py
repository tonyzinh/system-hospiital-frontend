import streamlit as st
from services.patients_api import PatientsAPI
from .patient_list import render_patients_list, render_patients_statistics
from .utils.utils import (
    normalize_patients_data,
    filter_patients_by_search,
    initialize_session_state,
)
from .patient_actions import (
    handle_patient_form_submission,
    handle_patient_deletion,
    handle_edit_modal,
    handle_delete_confirmation,
)


def pacientes():
    """Página principal de gerenciamento de pacientes"""

    api = PatientsAPI()
    initialize_session_state()

    # Cabeçalho
    st.title("Gestão de Pacientes")

    # Barra de ações
    col1, col2, col3 = st.columns([2, 1, 1])

    with col1:
        search_term = st.text_input(
            "Buscar",
            placeholder="Buscar por nome do paciente...",
            label_visibility="collapsed",
        )

    with col2:
        if st.button("Novo Paciente", use_container_width=True):
            st.session_state.editing_patient = None
            st.session_state.show_patient_modal = True
            st.rerun()

    with col3:
        if st.button("Atualizar", use_container_width=True):
            st.rerun()

    # Buscar e processar pacientes
    raw_patients = api.get_patients()
    patients = normalize_patients_data(raw_patients)
    patients = filter_patients_by_search(patients, search_term)

    # Processar modals e ações
    handle_edit_modal(api, patients)
    handle_delete_confirmation(patients)

    # Processar dados do formulário
    if st.session_state.patient_form_data:
        form_data = st.session_state.patient_form_data
        st.session_state.patient_form_data = None
        handle_patient_form_submission(api, form_data)

    # Processar exclusão
    handle_patient_deletion(api)

    # Lista de pacientes
    st.subheader("Pacientes Cadastrados")

    if patients:
        render_patients_list(patients)
    else:
        if search_term:
            st.info("Nenhum paciente encontrado com esse termo de busca.")
        else:
            st.info(
                "Nenhum paciente cadastrado ainda. Clique em 'Novo Paciente' para começar."
            )

    # Rodapé com estatísticas
    render_patients_statistics(patients)
