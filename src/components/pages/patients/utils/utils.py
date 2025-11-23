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

    # Estados básicos
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

    # Novos estados para controle de fragmentos
    if "form_submitted" not in st.session_state:
        st.session_state.form_submitted = False
    if "deletion_completed" not in st.session_state:
        st.session_state.deletion_completed = False

    # Limpar estados de ações completadas
    if st.session_state.form_submitted:
        st.session_state.form_submitted = False
    if st.session_state.deletion_completed:
        st.session_state.deletion_completed = False

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


def validate_cpf(cpf):
    """
    Valida CPF brasileiro
    """
    if not cpf:
        return True  # CPF é opcional

    # Remover caracteres não numéricos
    cpf = ''.join(filter(str.isdigit, cpf))

    # Verificar se tem 11 dígitos
    if len(cpf) != 11:
        return False

    # Verificar se todos os dígitos são iguais (CPF inválido)
    if cpf == cpf[0] * 11:
        return False

    # Calcular primeiro dígito verificador
    soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
    primeiro_digito = 11 - (soma % 11)
    if primeiro_digito >= 10:
        primeiro_digito = 0

    # Calcular segundo dígito verificador
    soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
    segundo_digito = 11 - (soma % 11)
    if segundo_digito >= 10:
        segundo_digito = 0

    # Verificar se os dígitos calculados conferem
    return cpf[9] == str(primeiro_digito) and cpf[10] == str(segundo_digito)


def validate_email(email):
    """
    Validação básica de email
    """
    if not email:
        return True  # Email é opcional

    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_phone(phone):
    """
    Validação básica de telefone brasileiro
    """
    if not phone:
        return True  # Telefone é opcional

    # Remover caracteres não numéricos
    phone_digits = ''.join(filter(str.isdigit, phone))

    # Aceitar telefones com 10 ou 11 dígitos (com ou sem 9 no celular)
    return len(phone_digits) in [10, 11]


def calculate_age(birthdate_str):
    """
    Calcula idade a partir da data de nascimento
    """
    from datetime import datetime, date

    try:
        if isinstance(birthdate_str, str):
            birthdate = datetime.strptime(birthdate_str, "%Y-%m-%d").date()
        else:
            birthdate = birthdate_str

        today = date.today()
        age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
        return age
    except:
        return 0


def format_phone(phone):
    """
    Formata telefone para exibição
    """
    if not phone:
        return ""

    # Remover caracteres não numéricos
    digits = ''.join(filter(str.isdigit, phone))

    if len(digits) == 11:
        return f"({digits[:2]}) {digits[2:7]}-{digits[7:]}"
    elif len(digits) == 10:
        return f"({digits[:2]}) {digits[2:6]}-{digits[6:]}"
    else:
        return phone


def format_cpf(cpf):
    """
    Formata CPF para exibição
    """
    if not cpf:
        return ""

    digits = ''.join(filter(str.isdigit, cpf))
    if len(digits) == 11:
        return f"{digits[:3]}.{digits[3:6]}.{digits[6:9]}-{digits[9:]}"
    else:
        return cpf
