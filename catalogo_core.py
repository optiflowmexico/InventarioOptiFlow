import pandas as pd


def analizar_y_limpiar_excel(input_path, output_path):
    df = pd.read_excel(input_path)
    cols = {c.lower(): c for c in df.columns}

    sku = cols.get("sku")
    nombre = cols.get("nombre")
    desc = cols.get("descripcion")
    cat = cols.get("categoria")
    precio = cols.get("precio")

    problemas = []
    if desc:
        problemas.append(f"Sin descripción: {int(df[desc].isna().sum())}")
    if precio:
        problemas.append(f"Sin precio: {int(df[precio].isna().sum())}")
    if sku:
        problemas.append(f"Duplicados SKU: {int(df.duplicated(subset=[sku]).sum())}")
    if cat:
        problemas.append(f"Categorías vacías: {int(df[cat].isna().sum())}")

    df2 = df.copy()

    if cat:
        df2[cat] = df2[cat].fillna("Sin asignar")

    if desc:
        if nombre:
            df2[desc] = df2[desc].fillna(df2[nombre].astype(str).apply(lambda x: f"Producto {x}"))
        else:
            df2[desc] = df2[desc].fillna("Descripción pendiente")

    if precio and cat:
        df2[precio] = df2.groupby(cat)[precio].transform(lambda s: s.fillna(s.mean()))

    if sku:
        df2 = df2.drop_duplicates(subset=[sku], keep="first")

    with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
        df2.to_excel(writer, index=False, sheet_name="catalogo_limpio")

    resumen = "Análisis terminado:\n" + "\n".join(f"  - {p}" for p in problemas)
    resumen += f"\n\nFilas originales: {len(df)}\nFilas finales: {len(df2)}"
    return resumen
