# Instrucciones de uso - OptiFlow ERP

## 1. Objetivo

Esta herramienta permite limpiar y validar archivos Excel para dos catálogos:

- Catálogo de productos.
- Catálogo de materias primas.

El sistema revisa columnas obligatorias, completa ciertos campos cuando es posible y genera un archivo limpio para descarga.

---

## 2. Cómo usar la aplicación

1. Abre la aplicación en Streamlit.
2. Selecciona el módulo que deseas usar.
3. Carga tu archivo Excel `.xlsx`.
4. Da clic en **Procesar catálogo**.
5. Revisa el análisis mostrado en pantalla.
6. Descarga el archivo limpio generado.

---

## 3. Reglas generales

- El archivo debe ser un Excel `.xlsx`.
- Los nombres de las columnas deben coincidir con los esperados.
- Los campos obligatorios vacíos se marcarán en amarillo.
- El archivo limpio conservará la información original y agregará o corregirá campos según las reglas del módulo.

---

## 4. Catálogo de productos

### 4.1 Columnas obligatorias

El archivo debe contener, como mínimo:

- `SKU`
- `Nombre`
- `Categoria`
- `Modelo`
- `Precio`
- `Costo1`
- `Proveedor1`
- `Estado`

### 4.2 Reglas de limpieza

- Si `Nombre` está vacío, se reemplaza por `SIN NOMBRE`.
- Si `Categoria` está vacía, se reemplaza por `SIN CATEGORIA`.
- Si `Modelo` está vacío, se reemplaza por `SIN MODELO`.
- Si `Estado` está vacío, se reemplaza por `ACTIVO`.
- Los campos obligatorios vacíos se resaltan en amarillo.
- Se genera un análisis previo con conteo de faltantes y duplicados.

---

## 5. Catálogo de materias primas

### 5.1 Columnas obligatorias

El archivo debe contener, como mínimo:

- `Nombre`
- `UnidadMedida`
- `UnidadCompra`
- `Contenido`
- `Proveedor1`
- `Costo1`
- `Stock`

### 5.2 Reglas de limpieza

- `Descripcion` ya no es obligatoria.
- Se genera un nuevo campo llamado `DescripcionCompra`.
- `DescripcionCompra` solo se escribe cuando existe información suficiente.

### 5.3 Reglas para `DescripcionCompra`

La descripción se construye con esta lógica:

- Se usa el valor de `UnidadCompra`.
- Se usa el valor de `Contenido`.
- Se usa el valor de `UnidadMedida`.

Formato final esperado:

`UnidadCompra con Contenido UnidadMedida`

Ejemplo:

- `UnidadCompra = Cubeta`
- `Contenido = 19`
- `UnidadMedida = Litros`

Resultado:

- `DescripcionCompra = Cubeta con 19 Litros`

### 5.4 Reglas adicionales

- Si `UnidadCompra` y `Contenido` vienen vacíos, se llenan con:
  - `UnidadCompra = UnidadMedida`
  - `Contenido = 1`
  pero solo si `UnidadMedida` sí tiene valor.
- Si `UnidadMedida` está vacía, no se construye `DescripcionCompra`.
- Si `UnidadCompra` y `UnidadMedida` son iguales, no se construye `DescripcionCompra`.
- Si falta cualquier dato necesario, `DescripcionCompra` se deja vacía.
- `DescripcionCompra` no se marca en amarillo.

---

## 6. Resultados del análisis

La aplicación muestra un resumen con el número de filas originales y el conteo de columnas vacías o duplicadas, según el módulo seleccionado.

En productos se revisa:

- `SKU`
- `Nombre`
- `Categoria`
- `Modelo`
- `Precio`
- `Costo1`
- `Proveedor1`
- `Estado`

En materias primas se revisa:

- `Nombre`
- `UnidadMedida`
- `UnidadCompra`
- `Contenido`
- `Proveedor1`
- `Costo1`
- `Stock`
- `Descripcion` solo como referencia, no como campo obligatorio.

---

## 7. Descarga del archivo limpio

Al terminar el procesamiento, la aplicación genera un archivo Excel limpio listo para descargar.

- Productos: `catalogo_limpio.xlsx`
- Materias primas: `catalogo_materias_primas_limpio.xlsx`

---

## 8. Recomendaciones

- Verifica que tus columnas no tengan espacios extra.
- Evita cambiar los nombres de columna esperados.
- Si el archivo no se procesa, revisa primero que sea `.xlsx`.
- Si una columna obligatoria falta, la aplicación te lo informará en pantalla.
