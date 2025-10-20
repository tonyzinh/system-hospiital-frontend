import streamlit as st


def handle_patient_form_submission(api, form_data):
    """
    Processar dados do formulário do modal
    """
    if st.session_state.editing_patient:
        # Atualizar paciente existente
        result = api.update_patient(st.session_state.editing_patient, form_data)
        if result:
            st.success("Paciente atualizado com sucesso!")
            st.session_state.editing_patient = None
            st.rerun()
    else:
        # Criar novo paciente
        result = api.create_patient(form_data)
        if result:
            st.success("Paciente criado com sucesso!")
            st.rerun()


def handle_patient_deletion(api):
    """
    Processar confirmação de exclusão
    """
    if st.session_state.confirm_delete and st.session_state.deleting_patient:
        result = api.delete_patient(st.session_state.deleting_patient)
        if result:
            st.success("Paciente excluído com sucesso!")
        else:
            st.error("Erro ao excluir paciente!")

        # Limpar estados
        st.session_state.confirm_delete = False
        st.session_state.deleting_patient = None
        st.rerun()


def handle_edit_modal(api, patients):
    """
    Lidar com modal de criação/edição
    """
    if st.session_state.show_patient_modal:
        from .patient_forms import patient_form_modal

        current_patient = None
        is_edit = False

        if st.session_state.editing_patient:
            current_patient = api.get_patient(st.session_state.editing_patient)
            is_edit = True
            if not current_patient:
                st.error("Paciente não encontrado!")
                st.session_state.editing_patient = None
                st.session_state.show_patient_modal = False
                st.rerun()
                return

        patient_form_modal(patient=current_patient, is_edit=is_edit)


def handle_delete_confirmation(patients):
    """
    Lidar com modal de confirmação de exclusão
    """
    if st.session_state.show_delete_confirmation and st.session_state.deleting_patient:
        from .patient_forms import delete_patient_modal
        from .utils.utils import find_patient_by_id

        patient_to_delete = find_patient_by_id(
            patients, st.session_state.deleting_patient
        )
        if patient_to_delete:
            delete_patient_modal(patient_to_delete.get("full_name", "Paciente"))
        else:
            st.session_state.show_delete_confirmation = False
            st.session_state.deleting_patient = None
            st.rerun()
