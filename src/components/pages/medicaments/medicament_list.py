import streamlit as st


def render_medicaments_list(medicaments):
    """Renderiza lista de medicamentos em tabela"""
    if not medicaments or not isinstance(medicaments, list):
        st.info("Nenhum medicamento cadastrado ainda.")
        return

    # Cabeçalho da tabela
    col1, col2, col3, col4, col5 = st.columns([3, 3, 2, 2, 2])
    with col1:
        st.write("**NOME**")
    with col2:
        st.write("**PRINCÍPIO ATIVO**")
    with col3:
        st.write("**FORMA**")
    with col4:
        st.write("**DOSAGEM**")
    with col5:
        st.write("**AÇÃO**")

    st.divider()

    for med in medicaments:
        if not isinstance(med, dict):
            continue

        col1, col2, col3, col4, col5 = st.columns([3, 3, 2, 2, 2])

        with col1:
            name = med.get("name") or "(sem nome)"
            st.write(name)

        with col2:
            ingredient = med.get("active_ingredient", "N/A")
            st.write(ingredient)

        with col3:
            form = med.get("form", "N/A")
            st.write(form)

        with col4:
            strength = med.get("strength", "N/A")
            st.write(strength)

        with col5:
            mid = med.get("id")
            if mid:
                col_edit, col_delete = st.columns(2)
                with col_edit:
                    if st.button("Editar", key=f"med_edit_{mid}", help="Editar medicamento"):
                        st.session_state.editing_medicament = mid
                        st.session_state.show_medicament_modal = True
                        st.rerun()
                with col_delete:
                    if st.button(
                        "Excluir",
                        key=f"med_delete_{mid}",
                        help="Excluir medicamento",
                        type="secondary",
                    ):
                        st.session_state.deleting_medicament = mid
                        st.session_state.show_medicament_delete_confirmation = True
                        st.rerun()
        st.divider()


def render_medicaments_statistics(medicaments):
    """Renderiza estatísticas dos medicamentos"""
    if not medicaments:
        return

    st.divider()
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total de Medicamentos", len(medicaments))

    with col2:
        # Contar formas farmacêuticas únicas
        forms = {m.get("form") for m in medicaments if m.get("form")}
        st.metric("Formas Farmacêuticas", len(forms))

    with col3:
        # Contar princípios ativos únicos
        ingredients = {m.get("active_ingredient") for m in medicaments if m.get("active_ingredient")}
        st.metric("Princípios Ativos", len(ingredients))