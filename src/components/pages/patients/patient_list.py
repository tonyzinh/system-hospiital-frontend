import streamlit as st


def render_patients_list(patients):
    """Renderiza lista de pacientes em tabela"""
    if not patients or not isinstance(patients, list):
        st.info("Nenhum paciente cadastrado ainda.")
        return

    # CSS para estilizar o botão de excluir
    st.markdown(
        """
    <style>
    div[data-testid="stButton"] > button[kind="secondary"] {
        background-color: #ff4b4b;
        color: white;
        border: none;
    }
    div[data-testid="stButton"] > button[kind="secondary"]:hover {
        background-color: #ff6b6b;
        color: white;
        border: none;
    }
    </style>
    """,
        unsafe_allow_html=True,
    )

    # Cabeçalho da tabela
    col1, col2, col3, col4, col5 = st.columns([3, 2, 2, 2, 2])
    with col1:
        st.write("**NOME**")
    with col2:
        st.write("**EMAIL**")
    with col3:
        st.write("**CONTATO**")
    with col4:
        st.write("**DOC**")
    with col5:
        st.write("**AÇÃO**")

    st.divider()

    for patient in patients:
        # certificar que cada paciente é um dict
        if not isinstance(patient, dict):
            continue

        col1, col2, col3, col4, col5 = st.columns([3, 2, 2, 2, 2])

        with col1:
            name = patient.get("full_name") or "(sem nome)"
            st.write(name)

        with col2:
            contact = patient.get("contact_json", {})
            email = contact.get("email", "N/A")
            st.write(email)

        with col3:
            phone = contact.get("phone", "N/A")
            st.write(phone)

        with col4:
            document = patient.get("document", "N/A")
            st.write(document)

        with col5:
            pid = patient.get("id")
            if pid:
                col_edit, col_delete = st.columns(2)
                with col_edit:
                    if st.button("Editar", key=f"edit_{pid}", help="Editar paciente"):
                        st.session_state.editing_patient = pid
                        st.session_state.show_patient_modal = True
                        st.rerun()
                with col_delete:
                    if st.button(
                        "Excluir",
                        key=f"delete_{pid}",
                        help="Excluir paciente",
                        type="secondary",
                    ):
                        st.session_state.deleting_patient = pid
                        st.session_state.show_delete_confirmation = True
                        st.rerun()

        st.divider()


def render_patients_statistics(patients):
    """Renderiza estatísticas dos pacientes"""
    if not patients:
        return

    st.divider()
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total de Pacientes", len(patients))

    with col2:
        male_count = len([p for p in patients if p.get("sex") == "M"])
        st.metric("Pacientes Masculinos", male_count)

    with col3:
        female_count = len([p for p in patients if p.get("sex") == "F"])
        st.metric("Pacientes Femininos", female_count)
