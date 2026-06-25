# pages/2_catalogo_materias_primas.py
# =========================================
# Chatbot ERP – Limpieza de Catálogo de Materias Primas
# =========================================

import streamlit as st
from bot import procesar_materias_primas, validar_archivo_materias_primas
from catalogo_core import analizar_materias_primas


# =========================================
# Configuración de la página
# =========================================
st.set_page_config(
    layout="wide",
    page_title="Catálogo de Materias Primas",
    page_icon="🧪",
)

st.title("🧪 Chatbot ERP – Limpieza de Catálogo de Materias Primas")
st.write("Sube tu archivo Excel con tu catálogo de materias primas y obtén un archivo limpio listo para el ERP.")


# =========================================
# Navegación
# =========================================
st.page_link("app.py", label="🔙 Volver a la portada", icon="🏠")


# =========================================
# Sección de instrucciones
# =========================================
with st.container():
    st.markdown("### 📌 Instrucciones rápidas")
    st.markdown(
        """
        - Asegúrate de que tu archivo Excel tenga al menos las columnas:
          `Nombre`, `UnidadMedida`, `UnidadCompra`, `Contenido`, `Proveedor1`, `Costo1`, `Stock`.
        - `Descripcion` ya no es obligatoria.
        - Se generará el campo `DescripcionCompra` cuando exista información suficiente.
        - Los campos obligatorios vacíos se marcarán en amarillo en el archivo de salida.

        📌 Para mayor detalle en las instrucciones, consulta el [instructivo](https://raw.githubusercontent.com/optiflowmexico/InventarioOptiFlow/main/instrucciones.md)
        """
    )


# =========================================
# Formulario de subida de archivo
# =========================================
with st.form("upload_form_materias_primas", clear_on_submit=True):
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

    is_valid, resultado = validar_archivo_materias_primas(uploaded_file)

    if not is_valid:
        st.error(f"Error de validación: {resultado}")
        st.info("🔄 Puedes cargar otro archivo haciendo clic en 'Examinar archivos'")
        st.info("📌 Asegúrate de que tu archivo tenga las columnas mínimas: Nombre, UnidadMedida, UnidadCompra, Contenido, Proveedor1, Costo1, Stock")
    else:
        df = resultado
        st.success("Estructura básica válida.")

        # =========================================
        # Análisis previo del catálogo
        # =========================================
        st.markdown("### 🔍 Análisis previo del catálogo")
        hallazgos = analizar_materias_primas(df)

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("📄 Filas originales", hallazgos["filas_originales"])
            st.metric("📝 Sin nombre", hallazgos["sin_nombre"])
            st.metric("📘 Sin unidad medida", hallazgos["sin_unidadmedida"])
        with col2:
            st.metric("📦 Sin unidad compra", hallazgos["sin_unidadcompra"])
            st.metric("🔢 Sin contenido", hallazgos["sin_contenido"])
            st.metric("🏭 Sin proveedor", hallazgos["sin_proveedor"])
        with col3:
            st.metric("💰 Sin costo", hallazgos["sin_costo"])
            st.metric("📦 Sin stock", hallazgos["sin_stock"])
            st.metric("📄 Sin descripción", hallazgos["sin_descripcion"])

        st.write("Vista previa de los primeros registros:")
        st.dataframe(df.head())

        # =========================================
        # Procesamiento del catálogo
        # =========================================
        with st.spinner("Limpiando catálogo de materias primas..."):
            success, output_path, df_limpio = procesar_materias_primas(uploaded_file)

            if success:
                st.success("✅ Catálogo de materias primas generado correctamente.")

                # =========================================
                # Resumen de filas
                # =========================================
                st.markdown("### 📊 Resumen de filas")
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("📄 Filas originales", hallazgos["filas_originales"])
                with col2:
                    st.metric("📄 Filas finales (limpias)", len(df_limpio))

                with open(output_path, "rb") as f:
                    st.download_button(
                        label="📥 Descargar archivo limpio (.xlsx)",
                        data=f.read(),
                        file_name="catalogo_materias_primas_limpio.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    )
                st.info("🔄 Para procesar otro archivo, carga un nuevo Excel")
            else:
                st.error("No se pudo generar el archivo limpio.")
                st.info("🔄 Puedes cargar otro archivo haciendo clic en 'Examinar archivos'")
                st.info("📌 Asegúrate de que tu archivo tenga las columnas mínimas: Nombre, UnidadMedida, UnidadCompra, Contenido, Proveedor1, Costo1, Stock")


# =========================================
# Mensaje si no se sube archivo
# =========================================
elif procesar_button and not uploaded_file:
    st.warning("⚠️ Por favor, sube un archivo Excel primero.")