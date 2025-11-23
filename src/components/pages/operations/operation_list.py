import streamlit as st
from .utils.utils import (
    format_datetime,
    get_status_badge_color,
    get_status_display_name,
    calculate_sla_status,
    get_priority_display,
)


def render_operations_list(operations, api):
    """Renderiza a lista de operações"""

    # Ordenar por prioridade e depois por data de criação
    operations_sorted = sorted(
        operations, key=lambda x: (-x["priority_score"], x.get("started_at") or "")
    )

    for operation in operations_sorted:
        with st.container():
            col1, col2, col3, col4, col5 = st.columns([3, 2, 1.5, 1.5, 1])

            with col1:
                st.write(f"**{operation['name']}**")
                st.caption(
                    f"Tipo: {operation['entity_type']} | ID: {operation['entity_id']}"
                )

            with col2:
                status_color = get_status_badge_color(operation["status"])
                status_name = get_status_display_name(operation["status"])
                st.write(f"{status_color} {status_name}")

                # Mostrar informações de SLA
                sla_status = calculate_sla_status(operation)
                if sla_status == "overdue":
                    st.error("🚨 Fora do SLA")
                elif sla_status == "warning":
                    st.warning("⚠️ SLA próximo")
                elif sla_status == "on_time":
                    st.success("✅ Dentro do SLA")

            with col3:
                priority_display = get_priority_display(operation["priority_score"])
                st.write(priority_display)
                st.caption(f"SLA: {operation['sla_minutes']} min")

            with col4:
                if operation["started_at"]:
                    st.write("**Iniciado:**")
                    st.write(format_datetime(operation["started_at"]))
                else:
                    st.write("**Não iniciado**")

                if operation["completed_at"]:
                    st.write("**Concluído:**")
                    st.write(format_datetime(operation["completed_at"]))

            with col5:
                # Botões de ação baseados no status
                if operation["status"] == "Pendente":
                    if st.button(
                        "▶️", key=f"start_{operation['id']}", help="Iniciar tarefa"
                    ):
                        st.session_state.status_update_task = {
                            "id": operation["id"],
                            "action": "start",
                        }
                        st.rerun()

                elif operation["status"] == "Em Progresso":
                    if st.button(
                        "✅", key=f"complete_{operation['id']}", help="Concluir tarefa"
                    ):
                        st.session_state.status_update_task = {
                            "id": operation["id"],
                            "action": "complete",
                        }
                        st.rerun()

                # Botões sempre disponíveis
                col5a, col5b = st.columns(2)

                with col5a:
                    if st.button("✏️", key=f"edit_{operation['id']}", help="Editar"):
                        st.session_state.editing_operation = operation
                        st.session_state.show_operation_modal = True
                        st.rerun()

                with col5b:
                    if st.button("🗑️", key=f"delete_{operation['id']}", help="Excluir"):
                        st.session_state.operation_to_delete = operation["id"]
                        st.session_state.confirm_delete_operation = True
                        st.rerun()

            # Separador visual
            st.divider()


def render_operations_statistics(operations):
    """Renderiza estatísticas das operações"""
    if not operations:
        return

    # Calcular estatísticas
    total_operations = len(operations)
    pending_count = len([op for op in operations if op["status"] == "Pendente"])
    in_progress_count = len([op for op in operations if op["status"] == "Em Progresso"])
    completed_count = len([op for op in operations if op["status"] == "Completado"])
    cancelled_count = len([op for op in operations if op["status"] == "Cancelado"])

    # Calcular operações fora do SLA
    overdue_count = len(
        [op for op in operations if calculate_sla_status(op) == "overdue"]
    )

    # Calcular prioridades
    critical_count = len([op for op in operations if op["priority_score"] >= 8])
    high_count = len([op for op in operations if 6 <= op["priority_score"] < 8])

    st.subheader("Estatísticas")

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric("Total de Tarefas", total_operations)

    with col2:
        st.metric("Pendentes", pending_count)
        st.metric("Em Progresso", in_progress_count)

    with col3:
        st.metric("Concluídas", completed_count)
        st.metric("Canceladas", cancelled_count)

    with col4:
        st.metric(
            "Fora do SLA", overdue_count, delta=None if overdue_count == 0 else "❗"
        )

    with col5:
        st.metric("Prioridade Crítica", critical_count)
        st.metric("Prioridade Alta", high_count)

    # Gráfico de distribuição de status
    if st.checkbox("Mostrar gráfico de distribuição"):
        status_data = {
            "Pendente": pending_count,
            "Em Progresso": in_progress_count,
            "Concluída": completed_count,
            "Cancelada": cancelled_count,
        }

        # Filtrar apenas status com valores > 0
        status_data = {k: v for k, v in status_data.items() if v > 0}

        if status_data:
            st.bar_chart(status_data)
