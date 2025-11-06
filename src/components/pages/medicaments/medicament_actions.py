import streamlit as st


def handle_medicament_form_submission(api, form_data):
    """
    Processar dados do formulário do modal (Criar/Editar)
    """
    if st.session_state.editing_medicament:
        # Atualizar medicamento existente
        result = api.update_medication(st.session_state.editing_medicament, form_data)
        if result:
            st.success("Medicamento atualizado com sucesso!")
            st.session_state.editing_medicament = None
            st.rerun()
        else:
             st.error("Erro ao atualizar medicamento.")
    else:
        # Criar novo medicamento
        result = api.create_medication(form_data)
        if result:
            st.success("Medicamento criado com sucesso!")
            st.rerun()
        else:
            st.error("Erro ao criar medicamento.")


def handle_medicament_deletion(api):
    """
    Processar confirmação de exclusão
    """
    if st.session_state.confirm_medicament_delete and st.session_state.deleting_medicament:
        result = api.delete_medication(st.session_state.deleting_medicament)
        if result:
            st.success("Medicamento excluído com sucesso!")
        else:
            st.error("Erro ao excluir medicamento!")

        # Limpar estados
        st.session_state.confirm_medicament_delete = False
        st.session_state.deleting_medicament = None
        st.rerun()


def handle_medicament_edit_modal(api):
    """
    Lidar com modal de criação/edição
    """
    if st.session_state.show_medicament_modal:
        from .medicament_forms import medicament_form_modal

        current_medicament = None
        is_edit = False

        if st.session_state.editing_medicament:
            current_medicament = api.get_medication(st.session_state.editing_medicament)
            is_edit = True
            if not current_medicament:
                st.error("Medicamento não encontrado!")
                st.session_state.editing_medicament = None
                st.session_state.show_medicament_modal = False
                st.rerun()
                return

        medicament_form_modal(medicament=current_medicament, is_edit=is_edit)


def handle_medicament_delete_confirmation(api, medicaments):
    """
    Lidar com modal de confirmação de exclusão
    """
    if st.session_state.show_medicament_delete_confirmation and st.session_state.deleting_medicament:
        from .medicament_forms import delete_medicament_modal
        from .utils.utils import find_medicament_by_id

        medicament_to_delete = find_medicament_by_id(
            medicaments, st.session_state.deleting_medicament
        )
        if medicament_to_delete:
            delete_medicament_modal(medicament_to_delete.get("name", "Medicamento"))
        else:
            # Caso não encontre (ex: lista atualizou), apenas feche o modal
            st.session_state.show_medicament_delete_confirmation = False
            st.session_state.deleting_medicament = None
            st.rerun()