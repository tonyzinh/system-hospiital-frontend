import streamlit as st

# Configuração da página DEVE vir antes dos imports
st.set_page_config(
    page_title="Sistema Hospitalar",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': "Sistema Hospitalar v1.0"
    }
)

# Imports lazy loading - só carrega quando necessário
@st.cache_resource
def get_apis():
    """Cache das instâncias das APIs para evitar re-instanciação"""
    from services.patients_api import PatientsAPI
    from services.medicaments_api import MedicamentsAPI
    from services.operations_api import OperationsAPI
    return PatientsAPI(), MedicamentsAPI(), OperationsAPI()

@st.cache_data(ttl=60)  # Cache por 1 minuto
def load_dashboard_data():
    """Carrega dados do dashboard com cache"""
    try:
        patients_api, medications_api, operations_api = get_apis()

        patients = patients_api.get_patients() or []
        medications = medications_api.get_medications() or []
        operations = operations_api.get_process_tasks() or []

        return patients, medications, operations, None
    except Exception as e:
        return [], [], [], str(e)


@st.cache_data(ttl=30)  # Cache por 30 segundos para gráficos
def create_charts(patients, medications, operations):
    """Cria os gráficos do dashboard com cache"""
    import plotly.express as px
    import pandas as pd

    charts = {}

    # Gráfico de status das operações
    if operations:
        status_counts = {}
        status_names = {
            "pending": "Pendente",
            "in_progress": "Em Progresso",
            "completed": "Concluída",
            "cancelled": "Cancelada"
        }

        for op in operations:
            status = op.get("status", "pending")
            display_name = status_names.get(status, status)
            status_counts[display_name] = status_counts.get(display_name, 0) + 1

        if status_counts:
            df_status = pd.DataFrame(
                list(status_counts.items()),
                columns=['Status', 'Quantidade']
            )

            charts['pie'] = px.pie(
                df_status,
                values='Quantidade',
                names='Status',
                title="Status das Operações",
                color_discrete_sequence=px.colors.qualitative.Set3
            )

    # Gráfico de resumo geral
    active_ops = len([op for op in operations if op.get("status") == "in_progress"])
    summary_data = {
        "Módulo": ["Pacientes", "Medicamentos", "Operações Total", "Operações Ativas"],
        "Quantidade": [len(patients), len(medications), len(operations), active_ops],
        "Cor": ["#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4"]
    }

    df_summary = pd.DataFrame(summary_data)
    charts['bar'] = px.bar(
        df_summary,
        x="Módulo",
        y="Quantidade",
        title="Resumo do Sistema",
        color="Módulo",
        color_discrete_sequence=summary_data["Cor"]
    )
    charts['bar'].update_layout(showlegend=False)

    return charts

def dashboard():
    """Página Dashboard com Analytics - Otimizada"""
    st.title("Dashboard - Sistema Hospitalar")

    # Carregar dados com cache
    with st.spinner("Carregando dados..."):
        patients, medications, operations, error = load_dashboard_data()

    if error:
        st.error(f"Erro ao conectar com APIs: {error}")
        return

    # Calcular métricas uma vez
    active_ops = len([op for op in operations if op.get("status") == "in_progress"])
    completed_ops = len([op for op in operations if op.get("status") == "completed"])

    # Métricas principais
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Pacientes", len(patients))
    with col2:
        st.metric("Medicamentos", len(medications))
    with col3:
        st.metric("Operações Ativas", active_ops)
    with col4:
        st.metric("Concluídas", completed_ops)

    st.markdown("---")

    # Dois gráficos lado a lado - com cache
    st.subheader("Gráficos Analytics")

    if any([patients, medications, operations]):
        charts = create_charts(patients, medications, operations)

        col1, col2 = st.columns(2)

        with col1:
            if 'pie' in charts:
                st.plotly_chart(charts['pie'], use_container_width=True)
            else:
                st.info("Nenhuma operação para exibir")

        with col2:
            if 'bar' in charts:
                st.plotly_chart(charts['bar'], use_container_width=True)
            else:
                st.info("Dados insuficientes")

    st.markdown("---")

    # Informações detalhadas sobre cada módulo
    st.subheader("Informações Detalhadas dos Módulos")

    # Criar três colunas para os módulos
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("### Pacientes")
        if patients:
            st.success(f"{len(patients)} pacientes cadastrados")
            # Mostrar alguns pacientes recentes (primeiros 3)
            st.markdown("**Últimos cadastrados:**")
            for i, patient in enumerate(patients[:3]):
                name = patient.get("name", f"Paciente {i+1}")
                st.write(f"• {name}")
            if len(patients) > 3:
                st.caption(f"... e mais {len(patients)-3} pacientes")
        else:
            st.warning("Nenhum paciente cadastrado")

    with col2:
        st.markdown("### Medicamentos")
        if medications:
            st.success(f"{len(medications)} medicamentos disponíveis")
            # Mostrar alguns medicamentos recentes (primeiros 3)
            st.markdown("**Últimos cadastrados:**")
            for i, med in enumerate(medications[:3]):
                name = med.get("name", f"Medicamento {i+1}")
                st.write(f"• {name}")
            if len(medications) > 3:
                st.caption(f"... e mais {len(medications)-3} medicamentos")
        else:
            st.warning("Nenhum medicamento cadastrado")

    with col3:
        st.markdown("### Operações")
        if operations:
            # Estatísticas das operações
            pending = len([op for op in operations if op.get("status") == "pending"])
            in_progress = len([op for op in operations if op.get("status") == "in_progress"])
            completed = len([op for op in operations if op.get("status") == "completed"])

            st.write(f"Total: {len(operations)}")
            st.write(f"Pendentes: {pending}")
            st.write(f"Em progresso: {in_progress}")
            st.write(f"Concluídas: {completed}")

            # Alertas
            if pending > 5:
                st.error(f"Muitas tarefas pendentes ({pending})")
            elif in_progress > 0:
                st.info(f"{in_progress} tarefa(s) em andamento")
            else:
                st.success("Sem tarefas pendentes")
        else:
            st.warning("Nenhuma operação cadastrada")

    # Resumo final
    st.markdown("---")

    if not any([patients, medications, operations]):
        st.info("""
        **Bem-vindo ao Sistema Hospitalar!**

        Comece cadastrando:
        - Pacientes na seção correspondente
        - Medicamentos no módulo de medicamentos
        - Operações para gerenciar tarefas
        """)

    st.caption("Dashboard atualizado em tempo real • Sistema Hospitalar v1.0")


def pacientes():
    """Página Pacientes com lazy loading"""
    from components.pages.patients.main import pacientes as patients_page
    patients_page()

def medicamentos():
    """Página Medicamentos com lazy loading"""
    from components.pages.medicaments.main import medicamentos as medicamentos_page
    medicamentos_page()

def operacoes():
    """Página Operações com lazy loading"""
    from components.pages.operations.main import operacoes as operations_page
    operations_page()

def assistente_ia():
    """Página Assistente IA com lazy loading"""
    from components.pages.chat.main import assistente_ia as chat_assistente_ia
    chat_assistente_ia()

# Páginas do sistema
pages = [
    st.Page(dashboard, title="Dashboard"),
    st.Page(pacientes, title="Pacientes"),
    st.Page(medicamentos, title="Medicamentos"),
    st.Page(operacoes, title="Operações"),
    st.Page(assistente_ia, title="Assistente IA"),
]

# Navegação
navegacao = st.navigation(pages, position="top")
navegacao.run()
