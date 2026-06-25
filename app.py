# app.py
# =========================================
# Chatbot ERP – Portal principal
# =========================================

import streamlit as st


# =========================================
# Configuración de la página
# =========================================
st.set_page_config(
    layout="wide",
    page_title="OptiFlow ERP",
    page_icon="📦",
)

st.title("📦 OptiFlow ERP")
st.write("Selecciona el módulo que deseas utilizar.")


# =========================================
# Tarjetas de navegación
# =========================================
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 📦 Catálogo de productos")
    st.markdown("Limpieza y validación del catálogo de productos.")
    st.page_link(
        "pages/1_catalogo_productos.py",
        label="Abrir catálogo de productos",
        icon="📦",
    )

with col2:
    st.markdown("### 🧪 Catálogo de materias primas")
    st.markdown("Limpieza y validación del catálogo de materias primas.")
    st.page_link(
        "pages/2_catalogo_materias_primas.py",
        label="Abrir catálogo de materias primas",
        icon="🧪",
    )


# =========================================
# Nota general
# =========================================
st.markdown("---")
st.info("Ambos módulos comparten la misma base de limpieza, validación y descarga de archivos.")