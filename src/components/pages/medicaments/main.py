import streamlit as st
from services.medicaments_api import MedicamentsAPI
from .medicament_list import render_medicaments_list, render_medicaments_statistics
from .utils.utils import (
    normalize_medicaments_data,
    filter_medicaments_by_search,
    initialize_session_state,
)
from .medicament_actions import (
    handle_medicament_form_submission,
    handle_medicament_deletion,
    handle_medicament_edit_modal,
    handle_medicament_delete_confirmation,
)


def medicamentos():
    """Página principal de gerenciamento de medicamentos"""

    api = MedicamentsAPI()
    initialize_session_state()

    # Cabeçalho
    st.title("Gestão de Medicamentos")

    # Barra de ações
    col1, col2, col3 = st.columns([2, 1, 1])

    with col1:
        search_term = st.text_input(
            "Buscar",
            placeholder="Buscar por nome ou princípio ativo...",
            label_visibility="collapsed",
        )

    with col2:
        if st.button("Novo Medicamento", use_container_width=True):
            st.session_state.editing_medicament = None
            st.session_state.show_medicament_modal = True
            st.rerun()

    with col3:
        if st.button("Atualizar", use_container_width=True):
            st.rerun()

    # Buscar e processar medicamentos
    raw_medicaments = api.get_medications()
    medicaments = normalize_medicaments_data(raw_medicaments)
    medicaments = filter_medicaments_by_search(medicaments, search_term)

    # Processar modals e ações
    handle_medicament_edit_modal(api)
    handle_medicament_delete_confirmation(api, medicaments)

    # Processar dados do formulário
    if st.session_state.medicament_form_data:
        form_data = st.session_state.medicament_form_data
        st.session_state.medicament_form_data = None
        handle_medicament_form_submission(api, form_data)

    # Processar exclusão
    handle_medicament_deletion(api)

    # Lista de medicamentos
    st.subheader("Medicamentos Cadastrados")

    if medicaments:
        render_medicaments_list(medicaments)
    else:
        if search_term:
            st.info("Nenhum medicamento encontrado com esse termo de busca.")
        else:
            st.info(
                "Nenhum medicamento cadastrado ainda. Clique em 'Novo Medicamento' para começar."
            )

    # Rodapé com estatísticas
    render_medicaments_statistics(medicaments)