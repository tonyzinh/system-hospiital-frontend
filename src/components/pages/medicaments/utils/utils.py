import streamlit as st

def initialize_session_state():
    """Inicializa chaves do session_state para medicamentos"""
    keys = [
        'show_medicament_modal', 
        'editing_medicament',
        'show_medicament_delete_confirmation', 
        'deleting_medicament',
        'confirm_medicament_delete', 
        'medicament_form_data'
    ]
    for key in keys:
        if key not in st.session_state:
            st.session_state[key] = None

def normalize_medicaments_data(data):
    """Garante que os dados sejam uma lista de dicts"""
    if isinstance(data, list):
        return data
    return []

def filter_medicaments_by_search(medicaments, search_term):
    """Filtra medicamentos por nome ou princípio ativo"""
    if not search_term:
        return medicaments
    
    search_term = search_term.lower()
    filtered_list = []
    
    for med in medicaments:
        if not isinstance(med, dict):
            continue
            
        name = med.get('name', '').lower()
        ingredient = med.get('active_ingredient', '').lower()
        
        if search_term in name or search_term in ingredient:
            filtered_list.append(med)
            
    return filtered_list

def find_medicament_by_id(medicaments, medicament_id):
    """Encontra um medicamento na lista pelo ID"""
    if not medicaments or not isinstance(medicaments, list):
        return None
    return next((m for m in medicaments if m.get("id") == medicament_id), None)