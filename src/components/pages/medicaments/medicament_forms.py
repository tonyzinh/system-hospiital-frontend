import streamlit as st

@st.dialog("Dados do Medicamento", width="large")
def medicament_form_modal(medicament=None, is_edit=False):
    """Modal para criar/editar medicamento"""
    if medicament and not isinstance(medicament, dict):
        medicament = None

    st.markdown("### " + ("Editar Medicamento" if is_edit else "Novo Medicamento"))

    with st.form(key="medicament_modal_form"):
        col1, col2 = st.columns(2)

        with col1:
            name = st.text_input(
                "Nome do Medicamento *",
                value=medicament.get("name", "") if medicament else "",
                placeholder="Ex: Paracetamol",
            )
            form = st.text_input(
                "Forma Farmacêutica",
                value=medicament.get("form", "") if medicament else "",
                placeholder="Ex: Comprimido, Xarope, Injetável",
            )
            atc_code = st.text_input(
                "Código ATC (Opcional)",
                value=medicament.get("atc_code", "") if medicament else "",
                placeholder="Ex: N02BE01",
            )

        with col2:
            active_ingredient = st.text_input(
                "Princípio Ativo",
                value=medicament.get("active_ingredient", "") if medicament else "",
                placeholder="Ex: Paracetamol",
            )
            strength = st.text_input(
                "Dosagem / Concentração",
                value=medicament.get("strength", "") if medicament else "",
                placeholder="Ex: 500mg, 750mg/mL",
            )

        st.markdown("---")
        col_save, col_cancel = st.columns([1, 1])

        with col_save:
            submitted = st.form_submit_button(
                "Salvar", type="primary", use_container_width=True
            )

        with col_cancel:
            cancelled = st.form_submit_button("Cancelar", use_container_width=True)

        if cancelled:
            st.session_state.show_medicament_modal = False
            st.session_state.editing_medicament = None
            st.rerun()

        if submitted:
            if not name:
                st.error("Nome do medicamento é obrigatório!")
                return None

            form_data = {
                "name": name,
                "active_ingredient": active_ingredient,
                "form": form,
                "strength": strength,
                "atc_code": atc_code,
            }

            st.session_state.medicament_form_data = form_data
            st.session_state.show_medicament_modal = False
            st.rerun()

    return None


@st.dialog("Confirmar Exclusão", width="small")
def delete_medicament_modal(medicament_name):
    """Modal para confirmar exclusão de medicamento"""
    st.markdown("### ⚠️ Confirmar Exclusão")
    st.markdown("---")

    st.warning(f"Tem certeza que deseja excluir o medicamento **{medicament_name}**?")
    st.markdown("Esta ação não pode ser desfeita.")

    st.markdown("---")
    col1, col2 = st.columns(2)

    with col1:
        if st.button("Cancelar", use_container_width=True, key="cancel_med_delete"):
            st.session_state.show_medicament_delete_confirmation = False
            st.session_state.deleting_medicament = None
            st.rerun()

    with col2:
        if st.button(
            "Confirmar Exclusão",
            type="primary",
            use_container_width=True,
            key="confirm_med_delete_btn",
        ):
            st.session_state.confirm_medicament_delete = True
            st.session_state.show_medicament_delete_confirmation = False
            st.rerun()