import streamlit as st


def render_operation_form(operation=None):
    """Renderiza formulário de operação"""

    # Valores padrão ou valores da operação existente
    if operation:
        entity_type = operation.get("entity_type", "")
        entity_id = operation.get("entity_id", "")
        name = operation.get("name", "")
        status = operation.get("status", "pending")
        sla_minutes = operation.get("sla_minutes", 60)
        priority_score = operation.get("priority_score", 0.0)
    else:
        entity_type = ""
        entity_id = ""
        name = ""
        status = "pending"
        sla_minutes = 60
        priority_score = 0.0

    with st.form("operation_form", clear_on_submit=False):
        # Campos do formulário
        col1, col2 = st.columns(2)

        with col1:
            form_entity_type = st.selectbox(
                "Tipo de Entidade *",
                options=[
                    "patient",
                    "medication",
                    "appointment",
                    "admission",
                    "prescription",
                    "other",
                ],
                index=[
                    "patient",
                    "medication",
                    "appointment",
                    "admission",
                    "prescription",
                    "other",
                ].index(entity_type)
                if entity_type
                in [
                    "patient",
                    "medication",
                    "appointment",
                    "admission",
                    "prescription",
                    "other",
                ]
                else 0,
                help="Tipo de entidade relacionada à tarefa",
            )

            form_entity_id = st.text_input(
                "ID da Entidade",
                value=entity_id,
                help="ID da entidade relacionada (opcional)",
            )

            form_name = st.text_input(
                "Nome da Tarefa *", value=name, help="Nome descritivo da tarefa"
            )

        with col2:
            form_status = st.selectbox(
                "Status",
                options=["Pendente", "Em Progresso", "Completado", "Cancelado"],
                index=["Pendente", "Em Progresso", "Completado", "Cancelado"].index(status)
                if status in ["Pendente", "Em Progresso", "Completado", "Cancelado"]
                else 0,
                help="Status atual da tarefa",
            )

            form_sla_minutes = st.number_input(
                "SLA (minutos)",
                value=sla_minutes,
                min_value=1,
                max_value=10080,  # 1 semana
                step=15,
                help="Tempo limite para conclusão em minutos",
            )

            form_priority_score = st.slider(
                "Prioridade",
                min_value=0.0,
                max_value=10.0,
                value=priority_score,
                step=0.5,
                help="Score de prioridade (0=baixa, 10=crítica)",
            )

        # Mostrar descrição da prioridade
        if form_priority_score >= 8:
            st.error("🔴 Prioridade Crítica - Requer atenção imediata")
        elif form_priority_score >= 6:
            st.warning("🟠 Prioridade Alta - Importante resolver em breve")
        elif form_priority_score >= 4:
            st.info("🟡 Prioridade Média - Resolver quando possível")
        else:
            st.success("🟢 Prioridade Baixa - Pode aguardar")

        # Botões do formulário
        col1, col2, col3 = st.columns(3)

        with col1:
            submitted = st.form_submit_button(
                "Atualizar Tarefa" if operation else "Criar Tarefa",
                use_container_width=True,
            )

        with col2:
            if st.form_submit_button("Cancelar", use_container_width=True):
                st.session_state.show_operation_modal = False
                st.session_state.editing_operation = None
                st.rerun()

        with col3:
            # Botão de cancelar tarefa (apenas para tarefas existentes em progresso)
            if operation and operation.get("status") == "Em Progresso":
                if st.form_submit_button("Cancelar Tarefa", use_container_width=True):
                    st.session_state.status_update_task = {
                        "id": operation["id"],
                        "action": "cancel",
                    }
                    st.session_state.show_operation_modal = False
                    st.rerun()

        # Processar submissão
        if submitted:
            # Validações
            if not form_name.strip():
                st.error("Nome da tarefa é obrigatório")
                return

            if not form_entity_type:
                st.error("Tipo de entidade é obrigatório")
                return

            # Preparar dados do formulário
            form_data = {
                "id": operation["id"] if operation else None,
                "entity_type": form_entity_type,
                "entity_id": form_entity_id.strip(),
                "name": form_name.strip(),
                "status": form_status,
                "sla_minutes": int(form_sla_minutes),
                "priority_score": float(form_priority_score),
            }

            # Salvar dados no session state para processamento
            st.session_state.operation_form_data = form_data
            st.session_state.show_operation_modal = False
            st.session_state.editing_operation = None
            st.rerun()
