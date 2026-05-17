# InventarioOptiFlow

Chatbot ERP para analizar y limpiar catálogos de productos en Excel.

## Qué hace
- Detecta productos sin descripción.
- Detecta productos sin precio.
- Encuentra duplicados por SKU.
- Completa campos vacíos básicos.
- Devuelve un Excel limpio descargable.

## Estructura
- `app.py`: demo web en Streamlit.
- `bot.py`: bot de Telegram.
- `catalogo_core.py`: lógica de análisis y limpieza.
- `requirements.txt`: dependencias de Python.

## Campos recomendados del Excel
- SKU
- Nombre
- Descripcion
- Categoria
- Precio
- Stock
- UnidadMedida
- Proveedor
- FechaUltimaVenta
- Estado

## Instalación local
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Flujo de uso
1. El usuario sube un archivo Excel.
2. El sistema analiza problemas del catálogo.
3. El sistema limpia datos básicos.
4. El usuario descarga el archivo corregido.

## Objetivo del MVP
Validar si el cliente realmente necesita limpieza de catálogo antes de agregar IA avanzada y automatización completa.

## Próximos pasos
- Integrar Telegram.
- Agregar reglas de negocio por categoría.
- Generar descripciones con IA.
- Conectar con ERP.
