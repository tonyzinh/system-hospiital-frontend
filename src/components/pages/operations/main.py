import streamlit as st
from services.operations_api import OperationsAPI
from .operation_list import render_operations_list, render_operations_statistics
from .utils.utils import (
    normalize_operations_data,
    filter_operations_by_search,
    initialize_session_state,
)
from .operation_actions import (
    handle_operation_form_submission,
    handle_operation_deletion,
    handle_operation_edit_modal,
    handle_operation_delete_confirmation,
    handle_status_updates,
)


def operacoes():
    """Página principal de gerenciamento de operações"""

    api = OperationsAPI()
    initialize_session_state()

    # Cabeçalho
    st.title("Gestão de Operações")

    # Barra de ações
    col1, col2, col3, col4 = st.columns([2, 1, 1, 1])

    with col1:
        search_term = st.text_input(
            "Buscar",
            placeholder="Buscar por nome da tarefa, tipo ou status...",
            label_visibility="collapsed",
        )

    with col2:
        status_filter = st.selectbox(
            "Filtrar por Status",
            ["Todos", "Pendente", "Em Progresso", "Completado", "Cancelado"],
            label_visibility="collapsed",
        )

    with col3:
        if st.button("Nova Tarefa", use_container_width=True):
            st.session_state.editing_operation = None
            st.session_state.show_operation_modal = True
            st.rerun()

    with col4:
        if st.button("Atualizar", use_container_width=True):
            st.rerun()

    # Buscar e processar operações
    raw_operations = api.get_process_tasks()
    operations = normalize_operations_data(raw_operations)
    operations = filter_operations_by_search(operations, search_term, status_filter)

    # Processar modals e ações
    handle_operation_edit_modal(api)
    handle_operation_delete_confirmation(api, operations)
    handle_status_updates(api)

    # Processar dados do formulário
    if st.session_state.operation_form_data:
        form_data = st.session_state.operation_form_data
        st.session_state.operation_form_data = None
        handle_operation_form_submission(api, form_data)

    # Processar exclusão
    handle_operation_deletion(api)

    # Lista de operações
    st.subheader("Tarefas de Processo")

    if operations:
        render_operations_list(operations, api)
    else:
        if search_term or status_filter != "Todos":
            st.info("Nenhuma tarefa encontrada com os filtros aplicados.")
        else:
            st.info(
                "Nenhuma tarefa cadastrada ainda. Clique em 'Nova Tarefa' para começar."
            )

    # Rodapé com estatísticas
    render_operations_statistics(operations)
