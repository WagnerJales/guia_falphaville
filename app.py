import streamlit as st
from data import buscar_lote, setores, pontos_referencia, BASE_COORDS

st.set_page_config(page_title="AlphaVille Locator", page_icon="📍", layout="wide")

st.markdown("""
# **AlphaVille**
### Sistema de Localização — São Luís/MA
Encontre rapidamente qualquer lote dentro do condomínio.
""")


with st.form(key="busca"):
    col1, col2 = st.columns([2,1])
    with col1:
        lote_str = st.text_input("Número do Lote", placeholder="Ex.: A123, B45, L15, R8 ...").strip()
    with col2:
        setor = st.selectbox("Setor (opcional)", [""] + [s.nome for s in setores])
    submitted = st.form_submit_button("Encontrar Lote", use_container_width=True)

if submitted:
    from data import buscar_lotes_por_setor
    cand = buscar_lote(lote_str)
    if not cand and setor:
        # filtra por setor e tenta achar parcial pelo prefixo
        lotes_setor = buscar_lotes_por_setor(setor)
        cand = next((l for l in lotes_setor if lote_str.upper() in l.numero.upper()), None)
    if cand:
        st.session_state["selected_lote"] = cand.numero
        st.success(f"Lote {cand.numero} encontrado no {cand.setor}.")
        st.page_link("pages/1_🗺️_Mapa.py", label="Abrir mapa com rota", icon="🗺️", args={"lote": cand.numero})
    else:
        st.error("Lote não encontrado. Tente por exemplo: A1, B25, C50, L10, R5.")

st.markdown("""
---
#### Como funciona
1. Digite o **número do lote** (ex.: A12).  
2. Clique em **Encontrar Lote**.  
3. Abra a página **Mapa** para visualizar o trajeto desde a portaria ou sua posição atual (se disponível).
""")


with st.expander("Informações rápidas"):
    st.write("Cobertura 100%, 500+ lotes mapeados, 7 setores, 2 portarias.")
