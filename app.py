# app.py
import streamlit as st
from bot import procesar_catalogo, validar_archivo_excel
import pandas as pd

st.set_page_config(layout="wide")
st.title("🗂 Chatbot ERP – Limpieza de Catálogo de Productos")
st.write("Sube tu archivo Excel con tu catálogo de productos y obtén un archivo limpio listo para el ERP.")

with st.container():
    st.markdown("### 📌 Instrucciones rápidas")
    st.markdown(
        """
        - Asegúrate de que tu archivo Excel tenga al menos las columnas:
          `SKU`, `Nombre`, `Categoria`, `Modelo`, `Precio`, `Costo1`, `Proveedor1`, `Estado`.
        - Usa los nombres **exactos**, sin espacios ni acentos.
        - Campos vacíos se rellenan o se marcan en amarillo en el archivo de salida.
        """
    )

uploaded_file = st.file_uploader(
    "Sube tu archivo Excel (.xlsx)",
    type=["xlsx"],
    accept_multiple_files=False,
)

if uploaded_file:
    st.info("Archivo subido. Validando estructura...")

    # Validar archivo
    is_valid, df = validar_archivo_excel(uploaded_file)
    if not is_valid:
        st.error(f"Error de validación: {df}")
    else:
        st.success("Estructura básica válida.")
        st.write("Vista previa de los primeros registros:")
        st.dataframe(df.head())

        if st.button("Procesar catálogo"):
            with st.spinner("Limpiando catálogo..."):
                success, output_path, df_limpio = procesar_catalogo(uploaded_file)
                if success:
                    st.success("✅ Catálogo limpio generado correctamente.")
                    st.download_button(
                        label="📥 Descargar archivo limpio (.xlsx)",
                        data=open(output_path, "rb").read(),
                        file_name="catalogo_limpio.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    )
                else:
                    st.error("No se pudo generar el archivo limpio.")
