# app.py
# =========================================
# Chatbot ERP – Limpieza de Catálogo de Productos
# =========================================

import streamlit as st
from bot import procesar_catalogo, validar_archivo_excel
import pandas as pd
from catalogo_core import analizar_catalogo

# =========================================
# Configuración de la página
# =========================================
st.set_page_config(layout="wide")
st.title("📦 Chatbot ERP – Limpieza de Catálogo de Productos")
st.write("Sube tu archivo Excel con tu catálogo de productos y obtén un archivo limpio listo para el ERP.")

# =========================================
# Sección de instrucciones
# =========================================
with st.container():
    st.markdown("### 📌 Instrucciones rápidas")
    st.markdown(
    """
    - Asegúrate de que tu archivo Excel tenga al menos las columnas:
      `SKU`, `Nombre`, `Categoria`, `Modelo`, `Precio`, `Costo1`, `Proveedor1`, `Estado`.
    - Usa los nombres **exactos**, sin espacios ni acentos.
    - Campos vacíos se rellenan o se marcan en amarillo en el archivo de salida.
    
    📌 Para mayor detalle en las instrucciones, consulta el <a href="https://raw.githubusercontent.com/optiflowmexico/InventarioOptiFlow/main/instrucciones.md" target="_blank">instructivo</a>
    """
, unsafe_allow_html=True)

# =========================================
# Formulario de subida de archivo
# =========================================
# Usar st.form con clear_on_submit=True para resetear el file uploader
with st.form("upload_form", clear_on_submit=True):
    uploaded_file = st.file_uploader(
        "Sube tu archivo Excel (.xlsx)",
        type=["xlsx"],
        accept_multiple_files=False,
    )
    
    procesar_button = st.form_submit_button("Procesar catálogo")

# =========================================
# Validación y procesamiento del archivo
# =========================================
if procesar_button and uploaded_file:
    st.info("Archivo subido. Validando estructura...")

    # Validar archivo
    is_valid, df = validar_archivo_excel(uploaded_file)
    if not is_valid:
        # MENSAJE DE ERROR cuando la validación falla
        st.error(f"Error de validación: {df}")
        st.info("🔄 Puedes cargar otro archivo haciendo clic en 'Examinar archivos'")
        st.info("📌 Asegúrate de que tu archivo tenga las columnas mínimas: SKU, Nombre, Categoria, Modelo, Precio, Costo1, Proveedor1, Estado")
    else:
        st.success("Estructura básica válida.")

        # =========================================
        # Análisis previo del catálogo
        # =========================================
        st.markdown("### 🔍 Análisis previo del catálogo")
        hallazgos = analizar_catalogo(df)

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("📄 Filas originales", hallazgos["filas_originales"])
            st.metric("🔄 SKUs duplicados", hallazgos["skus_duplicados"])
            st.metric("🚫 Sin SKU", hallazgos["sin_sku"])
        with col2:
            st.metric("💰 Sin precio", hallazgos["sin_precio"])
            st.metric("📂 Sin categoría", hallazgos["sin_categoria"])
        with col3:
            st.metric("📝 Sin nombre", hallazgos["sin_nombre"])
            st.metric("🏭 Sin proveedor", hallazgos["sin_proveedor"])

        st.write("Vista previa de los primeros registros:")
        st.dataframe(df.head())

        # =========================================
        # Procesamiento del catálogo
        # =========================================
        with st.spinner("Limpiando catálogo..."):
            success, output_path, df_limpio = procesar_catalogo(uploaded_file)
            if success:
                st.success("✅ Catálogo limpio generado correctamente.")

                # =========================================
                # Resumen de filas
                # =========================================
                st.markdown("### 📊 Resumen de filas")
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("📄 Filas originales", hallazgos["filas_originales"])
                with col2:
                    st.metric("📄 Filas finales (limpias)", len(df_limpio))

                st.download_button(
                    label="📥 Descargar archivo limpio (.xlsx)",
                    data=open(output_path, "rb").read(),
                    file_name="catalogo_limpio.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                )
                st.info("🔄 Para procesar otro archivo, carga un nuevo Excel")
            else:
                # MENSAJE DE ERROR cuando no se puede generar el archivo
                st.error("No se pudo generar el archivo limpio.")
                st.info("🔄 Puedes cargar otro archivo haciendo clic en 'Examinar archivos'")
                st.info("📌 Asegúrate de que tu archivo tenga las columnas mínimas: SKU, Nombre, Categoria, Modelo, Precio, Costo1, Proveedor1, Estado")

# =========================================
# Mensaje si no se sube archivo
# =========================================
elif procesar_button and not uploaded_file:
    st.warning("⚠️ Por favor, sube un archivo Excel primero.")
