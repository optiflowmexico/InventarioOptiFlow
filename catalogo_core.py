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
