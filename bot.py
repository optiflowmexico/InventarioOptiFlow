# bot.py
# =========================================
# Orquestación de carga, validación,
# procesamiento y exportación de catálogos
# =========================================

import os
import tempfile
from typing import Tuple

import pandas as pd

from catalogo_core import (
    exportar_excel_con_estilo,
    limpiar_catalogo_productos,
    limpiar_materias_primas,
)


# =========================================
# Lectura de archivo
# =========================================
def cargar_excel(uploaded_file) -> pd.DataFrame:
    return pd.read_excel(uploaded_file, engine="openpyxl")


# =========================================
# Validación de columnas
# =========================================
def validar_columnas(df: pd.DataFrame, columnas_obligatorias: list) -> Tuple[bool, str]:
    mapping = {c.lower().replace(" ", "").replace("_", ""): c for c in df.columns}
    faltantes = []
    for col in columnas_obligatorias:
        key = col.lower().replace(" ", "").replace("_", "")
        if key not in mapping:
            faltantes.append(col)

    if faltantes:
        return False, f"Faltan columnas obligatorias: {', '.join(faltantes)}"

    return True, "OK"


# =========================================
# Validación de productos
# =========================================
def validar_archivo_excel(uploaded_file):
    try:
        df = cargar_excel(uploaded_file)
        obligatorias = ["SKU", "Nombre", "Categoria", "Modelo", "Precio", "Costo1", "Proveedor1", "Estado"]
        ok, msg = validar_columnas(df, obligatorias)
        if not ok:
            return False, msg
        return True, df
    except Exception as e:
        return False, f"No se pudo leer el archivo: {e}"


# =========================================
# Validación de materias primas
# =========================================
def validar_archivo_materias_primas(uploaded_file):
    try:
        df = cargar_excel(uploaded_file)
        obligatorias = ["Nombre", "UnidadMedida", "UnidadCompra", "Contenido", "Proveedor1", "Costo1", "Stock"]
        ok, msg = validar_columnas(df, obligatorias)
        if not ok:
            return False, msg
        return True, df
    except Exception as e:
        return False, f"No se pudo leer el archivo: {e}"


# =========================================
# Procesamiento de productos
# =========================================
def procesar_catalogo(uploaded_file):
    try:
        df = cargar_excel(uploaded_file)
        df_limpio = limpiar_catalogo_productos(df)

        output_dir = os.path.join(tempfile.gettempdir(), "optiflow")
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, "catalogo_limpio.xlsx")

        exportar_excel_con_estilo(
            df_limpio,
            output_path,
            ["SKU", "Nombre", "Categoria", "Modelo", "Precio", "Costo1", "Proveedor1", "Estado"],
        )

        return True, output_path, df_limpio
    except Exception as e:
        return False, str(e), None


# =========================================
# Procesamiento de materias primas
# =========================================
def procesar_materias_primas(uploaded_file):
    try:
        df = cargar_excel(uploaded_file)
        df_limpio = limpiar_materias_primas(df)

        output_dir = os.path.join(tempfile.gettempdir(), "optiflow")
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, "catalogo_materias_primas_limpio.xlsx")

        exportar_excel_con_estilo(
            df_limpio,
            output_path,
            ["Nombre", "UnidadMedida", "UnidadCompra", "Contenido", "Proveedor1", "Costo1", "Stock"],
        )

        return True, output_path, df_limpio
    except Exception as e:
        return False, str(e), None