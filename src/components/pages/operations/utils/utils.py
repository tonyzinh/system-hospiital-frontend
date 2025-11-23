import streamlit as st
from datetime import datetime


def normalize_operations_data(operations):
    """Normaliza dados de operações vindos da API"""
    if not operations:
        return []

    normalized = []
    for op in operations:
        # Garantir que temos todos os campos necessários
        normalized_op = {
            "id": op.get("id"),
            "entity_type": op.get("entity_type", ""),
            "entity_id": op.get("entity_id", ""),
            "name": op.get("name", ""),
            "status": op.get("status", "pending"),
            "sla_minutes": op.get("sla_minutes", 60),
            "started_at": op.get("started_at"),
            "completed_at": op.get("completed_at"),
            "priority_score": op.get("priority_score", 0.0),
        }
        normalized.append(normalized_op)

    return normalized


def filter_operations_by_search(operations, search_term, status_filter="Todos"):
    """Filtra operações por termo de busca e status"""
    if not operations:
        return []

    filtered = operations

    # Mapear nomes amigáveis para valores reais do status
    status_mapping = {
        "Pendente": "pending",
        "Em Progresso": "in_progress",
        "Completado": "completed",
        "Cancelado": "cancelled"
    }

    # Filtrar por status
    if status_filter != "Todos":
        real_status = status_mapping.get(status_filter, status_filter.lower())
        filtered = [op for op in filtered if op["status"] == real_status]

    # Filtrar por termo de busca
    if search_term:
        search_lower = search_term.lower()
        filtered = [
            op
            for op in filtered
            if search_lower in op["name"].lower()
            or search_lower in op["entity_type"].lower()
            or search_lower in op["status"].lower()
        ]

    return filtered


def initialize_session_state():
    """Inicializa variáveis do session state para operações"""
    if "show_operation_modal" not in st.session_state:
        st.session_state.show_operation_modal = False

    if "editing_operation" not in st.session_state:
        st.session_state.editing_operation = None

    if "operation_form_data" not in st.session_state:
        st.session_state.operation_form_data = None

    if "operation_to_delete" not in st.session_state:
        st.session_state.operation_to_delete = None

    if "confirm_delete_operation" not in st.session_state:
        st.session_state.confirm_delete_operation = False

    if "status_update_task" not in st.session_state:
        st.session_state.status_update_task = None


def format_datetime(datetime_str):
    """Formata string de datetime para exibição"""
    if not datetime_str:
        return "-"

    try:
        dt = datetime.fromisoformat(datetime_str.replace("Z", "+00:00"))
        return dt.strftime("%d/%m/%Y %H:%M")
    except Exception:
        return datetime_str


def get_status_badge_color(status):
    """Retorna cor para badge de status"""
    colors = {
        "pending": "🟡",
        "in_progress": "🔵",
        "completed": "🟢",
        "cancelled": "🔴",
    }
    return colors.get(status, "⚪")


def get_status_display_name(status):
    """Retorna nome amigável para status"""
    names = {
        "pending": "Pendente",
        "in_progress": "Em Progresso",
        "completed": "Concluída",
        "cancelled": "Cancelada",
    }
    return names.get(status, status.title())


def calculate_sla_status(operation):
    """Calcula se a operação está dentro do SLA"""
    if operation["status"] == "completed":
        return "completed"

    if not operation["started_at"]:
        return "not_started"

    try:
        started = datetime.fromisoformat(operation["started_at"].replace("Z", "+00:00"))
        now = datetime.now(started.tzinfo)
        elapsed_minutes = (now - started).total_seconds() / 60

        if elapsed_minutes > operation["sla_minutes"]:
            return "overdue"
        elif elapsed_minutes > operation["sla_minutes"] * 0.8:
            return "warning"
        else:
            return "on_time"
    except Exception:
        return "unknown"


def get_priority_display(priority_score):
    """Retorna exibição amigável para prioridade"""
    if priority_score >= 8:
        return "🔴 Crítica"
    elif priority_score >= 6:
        return "🟠 Alta"
    elif priority_score >= 4:
        return "🟡 Média"
    else:
        return "🟢 Baixa"
