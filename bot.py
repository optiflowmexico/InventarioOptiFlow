# bot.py
# =========================================
# Funciones de lectura, validación y proceso
# =========================================

import pandas as pd
import tempfile
from catalogo_core import limpiar_catalogo_excel, validar_estructura

# =========================================
# Validación del archivo Excel
# =========================================
def validar_archivo_excel(uploaded_file):
    """
    Lee el Excel, normaliza columnas y valida estructura.
    Devuelve (True, df) si todo está bien.
    Devuelve (False, mensaje_error) si falla.
    """
    try:
        df = pd.read_excel(uploaded_file)
        df = validar_estructura(df)
        return True, df
    except Exception as e:
        return False, str(e)

# =========================================
# Procesamiento del catálogo
# =========================================
def procesar_catalogo(uploaded_file):
    """
    Guarda temporalmente el archivo, lo limpia y regresa el resultado.
    Devuelve:
    - success (bool)
    - output_path o mensaje_error
    - df_limpio o None
    """
    try:
        with tempfile.NamedTemporaryFile(suffix=".xlsx", delete=False) as tmp_input:
            tmp_input.write(uploaded_file.getvalue())
            tmp_input_path = tmp_input.name

        with tempfile.NamedTemporaryFile(suffix="_limpio.xlsx", delete=False) as tmp_output:
            tmp_output_path = tmp_output.name

        df_limpio = limpiar_catalogo_excel(tmp_input_path, tmp_output_path)
        return True, tmp_output_path, df_limpio

    except Exception as e:
        return False, str(e), None