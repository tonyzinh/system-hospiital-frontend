import streamlit as st
from .operation_forms import render_operation_form


def handle_operation_form_submission(api, form_data):
    """Processa submissão do formulário de operação"""
    try:
        if form_data["id"]:  # Editando
            result = api.update_process_task(form_data["id"], form_data)
            if result:
                st.success("Tarefa atualizada com sucesso!")
            else:
                st.error("Erro ao atualizar tarefa")
        else:  # Criando nova
            # Remover id None antes de enviar
            form_data.pop("id", None)
            result = api.create_process_task(form_data)
            if result:
                st.success("Tarefa criada com sucesso!")
            else:
                st.error("Erro ao criar tarefa")

        st.session_state.show_operation_modal = False
        st.rerun()
    except Exception as e:
        st.error(f"Erro ao processar formulário: {e}")


def handle_operation_deletion(api):
    """Processa exclusão de operação"""
    if st.session_state.operation_to_delete:
        task_id = st.session_state.operation_to_delete
        result = api.delete_process_task(task_id)

        if result:
            st.success("Tarefa excluída com sucesso!")
        else:
            st.error("Erro ao excluir tarefa")

        st.session_state.operation_to_delete = None
        st.rerun()


def handle_operation_edit_modal(api):
    """Gerencia modal de edição/criação de operação"""
    if st.session_state.show_operation_modal:
        with st.container():
            st.subheader(
                "Nova Tarefa"
                if not st.session_state.editing_operation
                else "Editar Tarefa"
            )

            # Renderizar formulário
            render_operation_form(st.session_state.editing_operation)


def handle_operation_delete_confirmation(api, operations):
    """Gerencia confirmação de exclusão"""
    if (
        st.session_state.confirm_delete_operation
        and st.session_state.operation_to_delete
    ):
        # Encontrar a operação para mostrar detalhes
        operation_to_delete = next(
            (
                op
                for op in operations
                if op["id"] == st.session_state.operation_to_delete
            ),
            None,
        )

        if operation_to_delete:
            st.warning(
                f"Tem certeza que deseja excluir a tarefa '{operation_to_delete['name']}'? "
                "Esta ação não pode ser desfeita."
            )

            col1, col2 = st.columns(2)

            with col1:
                if st.button("✅ Confirmar Exclusão", use_container_width=True):
                    st.session_state.confirm_delete_operation = False
                    # A exclusão será processada por handle_operation_deletion
                    st.rerun()

            with col2:
                if st.button("❌ Cancelar", use_container_width=True):
                    st.session_state.operation_to_delete = None
                    st.session_state.confirm_delete_operation = False
                    st.rerun()


def handle_status_updates(api):
    """Gerencia atualizações de status das tarefas"""
    if st.session_state.status_update_task:
        task_info = st.session_state.status_update_task
        task_id = task_info["id"]
        action = task_info["action"]

        result = None
        message = ""

        if action == "start":
            result = api.start_task(task_id)
            message = "Tarefa iniciada com sucesso!"
        elif action == "complete":
            result = api.complete_task(task_id)
            message = "Tarefa concluída com sucesso!"
        elif action == "cancel":
            result = api.cancel_task(task_id)
            message = "Tarefa cancelada com sucesso!"

        if result:
            st.success(message)
        else:
            st.error(f"Erro ao {action} a tarefa")

        st.session_state.status_update_task = None
        st.rerun()
