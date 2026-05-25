# Catálogo de Productos – Chatbot ERP de Limpieza de Catálogo

Este repositorio contiene una aplicación de Streamlit que permite limpiar y estructurar archivos Excel de catálogo de productos para cargarse directamente en un ERP.

## 🎯 Objetivo del programa

- Validar que el archivo Excel de entrada cumpla con ciertas columnas mínimas y adicionales.
- Aplicar reglas de limpieza de datos (duplicados, valores faltantes, formatos).
- Marcar celdas en amarillo cuando un campo obligatorio está vacío o mal formateado.
- Generar un archivo Excel limpio listo para cargar al ERP.

## 📌 Reglas clave del archivo Excel

- Las columnas del archivo de entrada deben tener **exactamente los nombres recomendados**, sin espacios ni acentos.
- Columnas mínimas recomendadas:
  - `SKU`, `Nombre`, `Categoria`, `Modelo`, `Precio`, `Costo1`, `Proveedor1`, `Estado`.
- Columnas adicionales recomendadas:
  - `CodigoBarras`, `Descripcion`, `Preciominimo`, `Stock`, `UnidadMedida`, `UnidadEmpaque`, `Contenido`, `Leadtime1`, `Proveedor2`, `Costo2`, `Leadtime2`, `FechaUltimaVenta`, `Markup`.
- El bot:
  - Elimina SKUs duplicados.
  - Rellena campos faltantes (`Categoria` → "Sin categoria", `Proveedor1` → "Sin ProveedorPrincipal", etc.).
  - Recalcula el `Precio` a partir de `Costo1` y `Markup` cuando es posible.
  - Marca en amarillo las celdas vacías o mal formateadas.

## 📁 Estructura básica del repositorio

- `app.py` – Aplicación principal de Streamlit donde el usuario carga el Excel.
- `bot.py` – Lógica del chatbot y reglas de validación.
- `catalogo_core.py` – Funciones de limpieza, validación y escritura de Excel.
- `requirements.txt` – Dependencias de Python necesarias.
- `instrucciones.md` – Documento detallado de reglas para el usuario.

## 🚀 Cómo correr el programa

1. Asegúrate de tener Python >= 3.9 instalado.
2. Crea un entorno virtual:
   python -m venv venv
   source venv/bin/activate      # Linux/Mac
   venv\Scripts\activate         # Windows
3. Instala las dependencias:
   pip install -r requirements.txt
4. Ejecuta la app de Streamlit:
   streamlit run app.py
5. Sigue las instrucciones en la interfaz para cargar tu archivo Excel.

## 📧 Soporte

Si tienes dudas o problemas con el formato del Excel, contacta a tu consultor ERP.
