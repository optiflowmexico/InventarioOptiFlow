# catalogo_core.py
import pandas as pd
from openpyxl import Workbook, load_workbook
from openpyxl.styles import PatternFill

# Colores de relleno
YELLOW_FILL = PatternFill(start_color="FFFF00", end_color="FFFF00", fill_type="solid")


def validar_estructura(df):
    """Valida que el dataframe tenga al menos las columnas mínimas requeridas."""
    columnas_minimas = [
        "SKU",
        "Nombre",
        "Categoria",
        "Modelo",
        "Precio",
        "Costo1",
        "Proveedor1",
        "Estado",
    ]
    faltantes = [col for col in columnas_minimas if col not in df.columns]
    if faltantes:
        raise ValueError(f"Faltan columnas mínimas: {faltantes}")
    return True


def limpiar_fila(row):
    """Limpieza básica de valores de texto."""
    for col in ["SKU", "Nombre", "Categoria", "Modelo", "Proveedor1", "Estado"]:
        if col in row and pd.isna(row[col]):
            row[col] = "Sin asignar"
    return row


def marcar_vacios_en_amarillo(ws, column_name, column_index, df):
    """Marca en amarillo las celdas vacías de una columna."""
    df = df.reset_index(drop=True)
    for idx, value in enumerate(df[column_name], start=2):  # empieza en fila 2 (después del header)
        if pd.isna(value) or (isinstance(value, str) and value.strip() == ""):
            ws.cell(row=idx, column=column_index).fill = YELLOW_FILL


def recalcular_precio(df):
    """Recalcula Precio a partir de Costo1 y Markup si es posible."""
    if "Costo1" in df.columns and "Markup" in df.columns and "Precio" in df.columns:
        df["Precio"] = df.apply(
            lambda row: row["Costo1"] * (1 + row["Markup"] / 100)
            if pd.notna(row["Costo1"]) and pd.notna(row["Markup"]) and row["Costo1"] > 0
            else row["Precio"],
            axis=1,
        )
    return df


def limpiar_catalogo_excel(input_path, output_path):
    """
    Lee el archivo Excel de entrada, limpia según las reglas y escribe el archivo limpio.
    Marca celdas vacías en amarillo usando openpyxl.
    """
    df = pd.read_excel(input_path)

    # Validar estructura
    validar_estructura(df)

    # Reemplazar acentos por sin acentos y normalizar nombres de columnas
    df.rename(
        columns={
            "Categoría": "Categoria",
            "Descripción": "Descripcion",
        },
        inplace=True,
    )

    # 1. Valores vacíos mínimos con relleno
    df["Nombre"] = df["Nombre"].fillna("Sin nombre")
    df["Categoria"] = df["Categoria"].fillna("Sin categoria")
    df["Proveedor1"] = df["Proveedor1"].fillna("Sin ProveedorPrincipal")

    # 2. Marcar campos vacíos con "Sin asignar" y dejar en amarillo
    # Si el campo es obligatorio pero se deja vacío, se marca con relleno
    # La función de relleno lo hace directamente en el archivo de salida

    # 3. Eliminar SKUs duplicados (dejar el primero)
    df = df.drop_duplicates(subset=["SKU"], keep="first")

    # 4. Recalcular Precio si es posible
    df = recalcular_precio(df)

    # 5. Escribir a Excel con estilos
    df.to_excel(output_path, index=False, engine="openpyxl")

    # 6. Abrir el archivo para marcar en amarillo las celdas vacías
    wb = Workbook()
    wb = load_workbook(output_path)
    ws = wb.active

    # Diccionario de índice de columna por nombre
    col_indices = {cell.value: cell.column for cell in ws[1]}

    for col_name in col_indices.keys():
        if col_name in df.columns:
            # Marcamos celdas vacías
            marcar_vacios_en_amarillo(ws, col_name, col_indices[col_name], df)

    wb.save(output_path)
    return df

def analizar_catalogo(df_original):
    """
    Genera un resumen de hallazgos antes de limpiar el catálogo.
    Devuelve un diccionario con los hallazgos.
    """
    df = df_original.copy()

    # Normalizar nombres de columnas
    df.rename(
        columns={
            "Categoría": "Categoria",
            "Descripción": "Descripcion",
        },
        inplace=True,
    )

    # Hallazgos
    hallazgos = {}

    # Total de filas originales
    hallazgos["filas_originales"] = len(df)

    # SKUs duplicados
    if "SKU" in df.columns:
        total_skus = df["SKU"].count()
        skus_unicos = df["SKU"].nunique()
        hallazgos["skus_duplicados"] = total_skus - skus_unicos
    else:
        hallazgos["skus_duplicados"] = 0

    # Sin precio
    if "Precio" in df.columns:
        hallazgos["sin_precio"] = df["Precio"].isna().sum()
    else:
        hallazgos["sin_precio"] = "Columna no existe"

    # SKUs en blanco
    if "SKU" in df.columns:
        hallazgos["sin_sku"] = df["SKU"].isna().sum()
    else:
        hallazgos["sin_sku"] = "Columna no existe"

    # Sin categoría
    if "Categoria" in df.columns:
        hallazgos["sin_categoria"] = df["Categoria"].isna().sum()
    else:
        hallazgos["sin_categoria"] = "Columna no existe"

    # Sin nombre
    if "Nombre" in df.columns:
        hallazgos["sin_nombre"] = df["Nombre"].isna().sum()
    else:
        hallazgos["sin_nombre"] = "Columna no existe"

    # Sin Proveedor1
    if "Proveedor1" in df.columns:
        hallazgos["sin_proveedor"] = df["Proveedor1"].isna().sum()
    else:
        hallazgos["sin_proveedor"] = "Columna no existe"

    # Sin Costo1
    if "Costo1" in df.columns:
        hallazgos["sin_costo"] = df["Costo1"].isna().sum()
    else:
        hallazgos["sin_costo"] = "Columna no existe"

    # Sin Modelo
    if "Modelo" in df.columns:
        hallazgos["sin_modelo"] = df["Modelo"].isna().sum()
    else:
        hallazgos["sin_modelo"] = "Columna no existe"

    # Sin Estado
    if "Estado" in df.columns:
        hallazgos["sin_estado"] = df["Estado"].isna().sum()
    else:
        hallazgos["sin_estado"] = "Columna no existe"

    return hallazgos
