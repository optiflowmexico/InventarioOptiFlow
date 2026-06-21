 # bot.py
import pandas as pd
from catalogo_core import limpiar_catalogo_excel, analizar_catalogo, validar_estructura
import streamlit as st
from pathlib import Path

def validar_archivo_excel(uploaded_file):
    """Valida el archivo Excel cargado por el usuario."""
    try:
        df = pd.read_excel(uploaded_file)
        from catalogo_core import validar_estructura
        validar_estructura(df)
        return True, df
    except Exception as e:
        return False, str(e)


def procesar_catalogo(uploaded_file, output_dir="output"):
    """
    Procesa el archivo Excel de entrada y genera el archivo limpio.
    """
    Path(output_dir).mkdir(exist_ok=True)

    input_path = Path(output_dir) / "catalogo_original.xlsx"
    output_path = Path(output_dir) / "catalogo_limpio.xlsx"

    # Guardar el archivo subido
    with open(input_path, "wb") as f:
        f.write(uploaded_file.getvalue())

    try:
        # Ejecutar limpieza
        df = limpiar_catalogo_excel(input_path, output_path)
        return True, output_path, df
    except Exception as e:
        st.error(f"Error al procesar el archivo: {str(e)}")
        return False, None, None
