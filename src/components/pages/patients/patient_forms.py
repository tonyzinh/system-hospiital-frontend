import streamlit as st
from datetime import datetime, date
from .utils.utils import validate_cpf, validate_email, validate_phone, calculate_age


@st.dialog("Dados do Paciente", width="large")
def patient_form_modal(patient=None, is_edit=False):
    """Modal para criar/editar paciente"""
    # Garantir que patient seja um dict válido ou None
    if patient and not isinstance(patient, dict):
        patient = None

    st.markdown("### " + ("Editar Paciente" if is_edit else "Novo Paciente"))

    with st.form(key="patient_modal_form"):
        col1, col2 = st.columns(2)

        with col1:
            full_name = st.text_input(
                "Nome Completo *",
                value=patient.get("full_name", "") if patient else "",
                placeholder="Digite o nome completo",
            )

            sex = st.selectbox(
                "Sexo *",
                options=["M", "F"],
                format_func=lambda x: "Masculino" if x == "M" else "Feminino",
                index=0 if not patient else (0 if patient.get("sex") == "M" else 1),
            )

        with col2:
            # Tratar data de nascimento de forma segura
            birthdate_value = date.today()
            if patient and patient.get("birthdate"):
                try:
                    birthdate_str = patient.get("birthdate")
                    if isinstance(birthdate_str, str):
                        birthdate_value = datetime.strptime(
                            birthdate_str, "%Y-%m-%d"
                        ).date()
                except (ValueError, TypeError):
                    birthdate_value = date.today()

            birthdate = st.date_input(
                "Data de Nascimento *",
                value=birthdate_value,
                min_value=date(1950, 1, 1),
                max_value=date(2025, 12, 31),
                format="DD/MM/YYYY",
            )

            document = st.text_input(
                "Documento",
                value=patient.get("document", "") if patient else "",
                placeholder="CPF, RG ou outro documento",
            )

        # Contato
        st.markdown("#### Informações de Contato")
        contact_json = patient.get("contact_json", {}) if patient else {}

        col3, col4 = st.columns(2)
        with col3:
            phone = st.text_input(
                "Telefone",
                value=contact_json.get("phone", ""),
                placeholder="(00) 00000-0000",
            )
        with col4:
            email = st.text_input(
                "Email",
                value=contact_json.get("email", ""),
                placeholder="email@exemplo.com",
            )

        address = st.text_area(
            "Endereço",
            value=contact_json.get("address", ""),
            placeholder="Rua, número, bairro, cidade",
            height=100,
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
            st.session_state.show_patient_modal = False
            st.session_state.editing_patient = None

        if submitted:
            # Validações obrigatórias
            errors = []

            # Validar nome
            if not full_name or len(full_name.strip()) < 2:
                errors.append("Nome completo deve ter pelo menos 2 caracteres")
            elif not full_name.replace(" ", "").replace("-", "").replace("'", "").isalpha():
                errors.append("Nome deve conter apenas letras, espaços, hífens e apostrofes")

            # Validar idade
            age = calculate_age(birthdate)
            if age < 0:
                errors.append("Data de nascimento não pode ser no futuro")
            elif age > 150:
                errors.append("Data de nascimento não pode ser anterior a 150 anos")

            # Validar documento (assumindo CPF se tiver 11 dígitos)
            if document:
                document_digits = ''.join(filter(str.isdigit, document))
                if len(document_digits) == 11:  # Parece ser CPF
                    if not validate_cpf(document):
                        errors.append("CPF inválido")
                elif len(document.strip()) < 5:
                    errors.append("Documento deve ter pelo menos 5 caracteres")

            # Validar email
            if not validate_email(email):
                errors.append("Email deve ter formato válido (exemplo@dominio.com)")

            # Validar telefone
            if not validate_phone(phone):
                errors.append("Telefone deve ter formato válido (10 ou 11 dígitos)")

            # Exibir erros se houver
            if errors:
                for error in errors:
                    st.error(f"❌ {error}")
                return None

            contact_data = {}
            if phone:
                contact_data["phone"] = phone
            if email:
                contact_data["email"] = email
            if address:
                contact_data["address"] = address

            form_data = {
                "full_name": full_name.strip(),
                "birthdate": birthdate.strftime("%Y-%m-%d"),
                "sex": sex,
                "document": document.strip() if document else "",
                "contact_json": contact_data,
            }

            # Armazenar dados no session_state para processamento na página principal
            st.session_state.patient_form_data = form_data
            st.session_state.show_patient_modal = False

    return None


@st.dialog("Confirmar Exclusão", width="small")
def delete_patient_modal(patient_name):
    """Modal para confirmar exclusão de paciente"""
    st.markdown("### ⚠️ Confirmar Exclusão")
    st.markdown("---")

    st.warning(f"Tem certeza que deseja excluir o paciente **{patient_name}**?")
    st.markdown("Esta ação não pode ser desfeita.")

    st.markdown("---")
    col1, col2 = st.columns(2)

    with col1:
        if st.button("Cancelar", use_container_width=True, key="cancel_delete"):
            st.session_state.show_delete_confirmation = False
            st.session_state.deleting_patient = None

    with col2:
        if st.button(
            "Confirmar Exclusão",
            type="primary",
            use_container_width=True,
            key="confirm_delete_btn",
        ):
            st.session_state.confirm_delete = True
            st.session_state.show_delete_confirmation = False


def render_patient_form(patient=None, form_key="patient_form"):
    """Renderiza formulário de paciente para criar/editar (versão inline)"""
    # Garantir que patient seja um dict válido ou None
    if patient and not isinstance(patient, dict):
        patient = None

    with st.form(key=form_key):
        st.subheader("Dados do Paciente")

        col1, col2 = st.columns(2)

        with col1:
            full_name = st.text_input(
                "Nome Completo *",
                value=patient.get("full_name", "") if patient else "",
                placeholder="Digite o nome completo",
            )

            sex = st.selectbox(
                "Sexo *",
                options=["M", "F"],
                format_func=lambda x: "Masculino" if x == "M" else "Feminino",
                index=0 if not patient else (0 if patient.get("sex") == "M" else 1),
            )

        with col2:
            # Tratar data de nascimento de forma segura
            birthdate_value = date.today()
            if patient and patient.get("birthdate"):
                try:
                    birthdate_str = patient.get("birthdate")
                    if isinstance(birthdate_str, str):
                        birthdate_value = datetime.strptime(
                            birthdate_str, "%Y-%m-%d"
                        ).date()
                except (ValueError, TypeError):
                    birthdate_value = date.today()

            birthdate = st.date_input(
                "Data de Nascimento *",
                value=birthdate_value,
                min_value=date(1950, 1, 1),
                max_value=date(2025, 12, 31),
                format="DD/MM/YYYY",
            )

            document = st.text_input(
                "Documento",
                value=patient.get("document", "") if patient else "",
                placeholder="CPF, RG ou outro documento",
            )

        # Contato (JSON)
        st.subheader("Informações de Contato")
        contact_json = patient.get("contact_json", {}) if patient else {}

        col3, col4 = st.columns(2)
        with col3:
            phone = st.text_input(
                "Telefone",
                value=contact_json.get("phone", ""),
                placeholder="(00) 00000-0000",
            )
        with col4:
            email = st.text_input(
                "Email",
                value=contact_json.get("email", ""),
                placeholder="email@exemplo.com",
            )

        address = st.text_area(
            "Endereço",
            value=contact_json.get("address", ""),
            placeholder="Rua, número, bairro, cidade",
        )

        submitted = st.form_submit_button(
            "Salvar Paciente", type="primary", use_container_width=True
        )

        if submitted:
            # Validações obrigatórias
            errors = []

            # Validar nome
            if not full_name or len(full_name.strip()) < 2:
                errors.append("Nome completo deve ter pelo menos 2 caracteres")
            elif not full_name.replace(" ", "").replace("-", "").replace("'", "").isalpha():
                errors.append("Nome deve conter apenas letras, espaços, hífens e apostrofes")

            # Validar idade
            age = calculate_age(birthdate)
            if age < 0:
                errors.append("Data de nascimento não pode ser no futuro")
            elif age > 150:
                errors.append("Data de nascimento não pode ser anterior a 150 anos")

            # Validar documento (assumindo CPF se tiver 11 dígitos)
            if document:
                document_digits = ''.join(filter(str.isdigit, document))
                if len(document_digits) == 11:  # Parece ser CPF
                    if not validate_cpf(document):
                        errors.append("CPF inválido")
                elif len(document.strip()) < 5:
                    errors.append("Documento deve ter pelo menos 5 caracteres")

            # Validar email
            if not validate_email(email):
                errors.append("Email deve ter formato válido (exemplo@dominio.com)")

            # Validar telefone
            if not validate_phone(phone):
                errors.append("Telefone deve ter formato válido (10 ou 11 dígitos)")

            # Exibir erros se houver
            if errors:
                for error in errors:
                    st.error(f"❌ {error}")
                return None

            contact_data = {}
            if phone:
                contact_data["phone"] = phone
            if email:
                contact_data["email"] = email
            if address:
                contact_data["address"] = address

            return {
                "full_name": full_name.strip(),
                "birthdate": birthdate.strftime("%Y-%m-%d"),
                "sex": sex,
                "document": document.strip() if document else "",
                "contact_json": contact_data,
            }
    return None
