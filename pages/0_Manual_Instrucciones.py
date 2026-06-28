# pages/0_Manual_Instrucciones.py
import os
import streamlit as st

# Configuración de la página web
st.set_page_config(
    layout="wide",
    page_title="Manual de Instrucciones",
    page_icon="📖",
)

# Botón de navegación para regresar a casa
st.page_link("app.py", label="🔙 Volver a la portada", icon="🏠")
st.markdown("---")

# Ruta al archivo instrucciones.md centralizado en la raíz
ruta_instrucciones = "instrucciones.md"

if os.path.exists(ruta_instrucciones):
    with open(ruta_instrucciones, "r", encoding="utf-8") as f:
        contenido_markdown = f.read()
    st.markdown(contenido_markdown)
else:
    st.error("⚠️ No se encontró el archivo 'instrucciones.md' en el directorio raíz.")