# catalogo_core.py
# =========================================
# Lógica de limpieza y análisis de catálogo
# =========================================

import pandas as pd
from openpyxl import Workbook, load_workbook
from openpyxl.styles import PatternFill

# =========================================
# Configuración de estilos
# =========================================
YELLOW_FILL = PatternFill(start_color="FFFF00", end_color="FFFF00", fill_type="solid")

# =========================================
# Configuración de columnas
# =========================================
COLUMN_MAP = {
    "sku": "SKU",
    "nombre": "Nombre",
    "categoria": "Categoria",
    "categoría": "Categoria",
    "modelo": "Modelo",
    "precio": "Precio",
    "costo1": "Costo1",
    "proveedor1": "Proveedor1",
    "estado": "Estado",
    "descripcion": "Descripcion",
}

COLUMNAS_MINIMAS = [
    "SKU",
    "Nombre",
    "Categoria",
    "Modelo",
    "Precio",
    "Costo1",
    "Proveedor1",
    "Estado",
]

# =========================================
# Normalización de columnas
# =========================================
def normalizar_columnas(df):
    """
    Convierte encabezados a minúsculas, quita espacios y aplica nombres estándar.
    """
    df = df.copy()
    df.columns = df.columns.astype(str).str.strip().str.lower()
    df = df.rename(columns=COLUMN_MAP)
    return df

# =========================================
# Validación de estructura
# =========================================
def validar_estructura(df):
    """
    Valida que el dataframe tenga al menos las columnas mínimas requeridas.
    Acepta mayúsculas/minúsculas porque normaliza antes de validar.
    """
    df = normalizar_columnas(df)
    faltantes = [col for col in COLUMNAS_MINIMAS if col not in df.columns]
    if faltantes:
        raise ValueError(f"Faltan columnas mínimas: {faltantes}")
    return df

# =========================================
# Limpieza de filas
# =========================================
def limpiar_fila(row):
    """
    Limpieza básica de valores de texto.
    """
    for col in ["SKU", "Nombre", "Categoria", "Modelo", "Proveedor1", "Estado"]:
        if col in row and pd.isna(row[col]):
            row[col] = "Sin asignar"
    return row

# =========================================
# Marcar vacíos en amarillo
# =========================================
def marcar_vacios_en_amarillo(ws, column_name, column_index, df):
    """
    Marca en amarillo las celdas vacías de una columna.
    """
    df = df.reset_index(drop=True)
    for idx, value in enumerate(df[column_name], start=2):
        if pd.isna(value) or (isinstance(value, str) and value.strip() == ""):
            ws.cell(row=idx, column=column_index).fill = YELLOW_FILL

# =========================================
# Recalcular precio
# =========================================
def recalcular_precio(df):
    """
    Recalcula Precio a partir de Costo1 y Markup si es posible.
    """
    if "Costo1" in df.columns and "Markup" in df.columns and "Precio" in df.columns:
        df["Precio"] = df.apply(
            lambda row: row["Costo1"] * (1 + row["Markup"] / 100)
            if pd.notna(row["Costo1"]) and pd.notna(row["Markup"]) and row["Costo1"] > 0
            else row["Precio"],
            axis=1,
        )
    return df

# =========================================
# Limpieza principal del catálogo
# =========================================
def limpiar_catalogo_excel(input_path, output_path):
    """
    Lee el archivo Excel de entrada, limpia según las reglas y escribe el archivo limpio.
    Marca celdas vacías en amarillo usando openpyxl.
    """
    df = pd.read_excel(input_path)

    # Normalizar columnas antes de validar
    df = normalizar_columnas(df)

    # Validar estructura
    df = validar_estructura(df)

    # 1. Valores vacíos mínimos con relleno
    df["Nombre"] = df["Nombre"].fillna("Sin nombre")
    df["Categoria"] = df["Categoria"].fillna("Sin categoria")
    df["Proveedor1"] = df["Proveedor1"].fillna("Sin ProveedorPrincipal")

    # 2. Eliminar SKUs duplicados (dejar el primero)
    df = df.drop_duplicates(subset=["SKU"], keep="first")

    # 3. Recalcular Precio si es posible
    df = recalcular_precio(df)

    # 4. Escribir a Excel con estilos
    df.to_excel(output_path, index=False, engine="openpyxl")

    # 5. Abrir el archivo para marcar en amarillo las celdas vacías
    wb = load_workbook(output_path)
    ws = wb.active

    # Diccionario de índice de columna por nombre
    col_indices = {cell.value: cell.column for cell in ws[1]}

    for col_name in col_indices.keys():
        if col_name in df.columns:
            marcar_vacios_en_amarillo(ws, col_name, col_indices[col_name], df)

    wb.save(output_path)
    return df

# =========================================
# Análisis previo del catálogo
# =========================================
def analizar_catalogo(df_original):
    """
    Genera un resumen de hallazgos antes de limpiar el catálogo.
    Devuelve un diccionario con los hallazgos.
    """
    df = normalizar_columnas(df_original)

    hallazgos = {}
    hallazgos["filas_originales"] = len(df)

    # SKUs duplicados
    if "SKU" in df.columns:
        sku_limpio = df["SKU"].astype(str).str.strip()
        sku_no_vacios = sku_limpio[sku_limpio.ne("") & sku_limpio.ne("nan")]
        hallazgos["skus_duplicados"] = sku_no_vacios.duplicated().sum()
    else:
        hallazgos["skus_duplicados"] = "Columna no existe"

    # SKUs en blanco
    if "SKU" in df.columns:
        sku_limpio = df["SKU"].astype(str).str.strip()
        hallazgos["sin_sku"] = df["SKU"].isna().sum() + sku_limpio.eq("").sum()
    else:
        hallazgos["sin_sku"] = "Columna no existe"

    # Otras columnas
    columnas_a_revisar = {
        "sin_precio": "Precio",
        "sin_categoria": "Categoria",
        "sin_nombre": "Nombre",
        "sin_proveedor": "Proveedor1",
        "sin_costo": "Costo1",
        "sin_modelo": "Modelo",
        "sin_estado": "Estado",
    }

    for key, col in columnas_a_revisar.items():
        hallazgos[key] = df[col].isna().sum() if col in df.columns else "Columna no existe"

    return hallazgos