import streamlit as st
import pandas as pd
import numpy as np
import tempfile
from io import BytesIO
from catalogo_core import analizar_y_limpiar_excel

st.set_page_config(page_title="OptiFlow Catálogo", layout="wide")
st.title("📦 Analiza y limpia tu catálogo de productos")
st.caption("Sube un Excel y obtén un análisis básico con archivo limpio descargable.")

uploaded_file = st.file_uploader("Sube tu archivo Excel", type=["xlsx", "xls"])

if uploaded_file:
    with tempfile.NamedTemporaryFile(suffix=".xlsx", delete=False) as tmp_input:
        tmp_input.write(uploaded_file.getvalue())
        tmp_input_path = tmp_input.name

    with tempfile.NamedTemporaryFile(suffix="_limpio.xlsx", delete=False) as tmp_output:
        tmp_output_path = tmp_output.name

    with st.spinner("Analizando y limpiando catálogo..."):
        resumen = analizar_y_limpiar_excel(tmp_input_path, tmp_output_path)

    st.subheader("Análisis detectado")
    for line in resumen.split("\n"):
        if line.startswith("-") or line.startswith("Análisis") == False:
            st.text(line)

    df = pd.read_excel(tmp_output_path)
    st.dataframe(df.head(20))

    with open(tmp_output_path, "rb") as f:
        st.download_button(
            "Descargar catálogo limpio",
            data=f.read(),
            file_name="catalogo_limpio.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    # limpia archivos temporales al final
    st.write("Listo. Puedes subir otro archivo o recargar la página.")
else:
    st.info("Sube un archivo Excel para empezar.")
