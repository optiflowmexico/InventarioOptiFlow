# Instrucciones para el uso del Chatbot ERP de Limpieza de Catálogo

Este archivo contiene las instrucciones necesarias para que puedas **subir tu archivo de Excel** y **entender el archivo Excel limpio** que recibes de vuelta.

---

## 📌 Resumen

- Asegúrate de que el archivo Excel tenga las columnas mínimas recomendadas.
- Asegúrate de que el nombre de las etiquetas de cada columna tengan los nombres aquí recomendados escritos sin espacios, sin caracteres especiales ni acentos.
- Asegúrate de que el formato de cada columna sea correcto.
- El archivo de salida será limpio y listo para cargar al ERP.

---

## 📌 Campos recomendados del Excel de entrada

Para que el chatbot funcione correctamente, tu archivo Excel debe incluir **las columnas mínimas recomendadas** y, para una mejor toma de decisiones, **las columnas adicionales recomendadas**. Es importante que las etiquetas que nombran las columnas tengan los nombres aquí recomendados escritos sin espacios ni acentos.

### Columnas mínimas recomendadas
- `SKU`
- `Nombre`
- `Categoria` (o `Categoría`)
- `Modelo`
- `Precio`
- `Costo1`
- `Proveedor1`
- `Estado`

### Columnas adicionales recomendadas
- `CodigoBarras`
- `Descripcion` (o `Descripción`)
- `Preciominimo`
- `Stock`
- `UnidadMedida`
- `UnidadEmpaque`
- `Contenido`
- `Leadtime1`
- `Proveedor2`
- `Costo2`
- `Leadtime2`
- `FechaUltimaVenta`

---

## 📌 Formato y uso de cada columna

### 1. `SKU` (Código de producto)

- **Tipo de dato**: `Texto` (String).
- **Qué hacer**:
  - Asegúrate de que cada SKU sea **único** (sin duplicados).
- **Qué pasa si no es único**:
  - El bot eliminará los duplicados y dejará solo uno por SKU.
- **Resultado esperado en salida**:
  - Todos los SKUs en el archivo limpio serán únicos; se conservará el primero por cada SKU repetido.

---

### 2. `Nombre` (Nombre del producto)

- **Tipo de dato**: `Texto` (String).
- **Qué hacer**:
  - Asegúrate de que el nombre sea claro y descriptivo.
- **Qué pasa si está vacío**:
  - Se asignará "Sin nombre" a todos los productos sin nombre y la celda se marca en amarillo.
- **Resultado esperado en salida**:
  - El nombre se conserva tal cual; si se detectan errores o inconsistencias, el bot puede limpiarlo (por ejemplo, quitar saltos de línea o espacios extra).

---

### 3. `Categoria` / `Categoría` (Categoría del producto)

- **Tipo de dato**: `Texto` (String).
- **Qué hacer**:
  - Agrupa los productos por categoría (por ejemplo, "Salas", "Recamaras").
- **Qué pasa si está vacío**:
  - Se asignará "Sin categoria" a todos los productos sin categoría y la celda se pone en amarillo .
- **Resultado esperado en salida**:
  - Cada fila tendrá una categoría asignada; si se encuentra vacía, se colocará "Sin categoria" y la celda se marca en amarillo.

---

### 4. `Modelo` (Modelo del producto)

- **Tipo de dato**: `Texto` (String).
- **Qué hacer**:
  - Indica el modelo o referencia interna del producto.
- **Qué pasa si está vacío**:
  - No se hace nada con el dato solo se marca la celda en amarillo.
- **Resultado esperado en salida**:
  - El campo se conserva sin cambios; si se detectan errores de formato, se limpian caracteres no permitidos.

---

### 5. `Precio` (Precio de venta)

- **Tipo de dato**: `Número` (Float o Int).
- **Formato**: `12.50`, `100.00`, etc.
- **Qué hacer**:
  - Asegúrate de que solo haya números en la columna `Precio`.
- **Qué pasa si no es numérico**:
  - Si hay algún valor no numérico, el bot no podrá calcular ni rellenar precios, y mostrará un mensaje de error.
  - Si todos los valores son no numéricos, no se rellenan precios.
- **Qué pasa si está vacío**:
  - No se hace nada con el dato solo se marca la celda en amarillo.
- **Resultado esperado en salida**:
  - Todos los valores de `Precio` serán numéricos; se rellenan los valores faltantes con el `Precio` a partir de `Costo1` y `Markup` (por ejemplo: `Precio = Costo1 * (1 + Markup/100)` cuando el `Markup` está en porcentaje).
. Si `Costo1` (Costo principal) o `Markup` esta vacío se deja vacío el `Costo1`

---

### 6. `Costo1` (Costo principal)

- **Tipo de dato**: `Número` (Float o Int).
- **Qué hacer**:
  - Indica el costo principal de este producto (proveedor 1 o principal).
- **Qué pasa si está vacío**:
  - No se hace nada con el dato solo se marca la celda en amarillo.
- **Resultado esperado en salida**:
  - El campo se conserva sin cambios; no se calcula promedio, solo se limpian errores.

---

### 7. `Proveedor1` (Proveedor principal)

- **Tipo de dato**: `Texto` (String).
- **Qué hacer**:
  - Nombre del proveedor principal.
- **Qué pasa si está vacío**:
  - Se asignará "Sin ProveedorPrincipal" a todos los productos sin Proveedor Principal y la celda se marca en amarillo.
- **Resultado esperado en salida**:
  - El nombre del proveedor se conserva sin cambios.

---

### 8. `Estado` (Estado del producto)

- **Tipo de dato**: `Texto` (String).
- **Valores sugeridos**:
  - `Activo`
  - `Inactivo`
- **Qué pasa si está vacío**:
  - No se hace nada con el dato solo se marca la celda en amarillo.
- **Resultado esperado en salida**:
  - El campo se conserva sin cambios.

---

### 9. `CodigoBarras` (Código de barras)

- **Tipo de dato**: `Texto` (String).
- **Qué hacer**:
  - Código de barras del producto (EAN, UPC, etc.).
- **Qué pasa si está vacío**:
  - No se hace nada con el dato solo se marca la celda en amarillo.
- **Resultado esperado en salida**:
  - El campo se conserva sin cambios.

---

### 10. `Descripcion` / `Descripción` (Descripción del producto)

- **Tipo de dato**: `Texto` (String).
- **Qué hacer**:
  - Describe brevemente el producto.
- **Qué pasa si está vacío**:
  - No se hace nada con el dato solo se marca la celda en amarillo.
- **Resultado esperado en salida**:
  - El campo se conserva sin cambios.

---

### 11. `Preciominimo` (Precio mínimo)

- **Tipo de dato**: `Número` (Float o Int).
- **Qué hacer**:
  - Precio mínimo sugerido.
- **Qué pasa si está vacío**:
  - No se hace nada con el dato solo se marca la celda en amarillo.
- **Resultado esperado en salida**:
  - El campo se conserva sin cambios.

---

### 12. `Stock` (Cantidad en inventario)

- **Tipo de dato**: `Número` (Float o Int).
- **Qué hacer**:
  - Indica la cantidad de inventario actual.
- **Qué pasa si está vacío**:
  - No se hace nada con el dato solo se marca la celda en amarillo.
- **Resultado esperado en salida**:
  - El campo se conserva sin cambios.

---

### 13. `UnidadMedida` (Unidad de medida)

- **Tipo de dato**: `Texto` (String).
- **Qué hacer**:
  - Unidad de medida (piezas, kilos, metros, etc.).
- **Qué pasa si está vacío**:
  - No se hace nada con el dato solo se marca la celda en amarillo.
- **Resultado esperado en salida**:
  - El campo se conserva sin cambios.

---

### 14. `UnidadEmpaque` (Unidad de empacado, por ejemplo, caja, rollo, juego, etc.).

- **Tipo de dato**: `Texto` (String).
- **Qué hacer**:
  - Cómo se empaqueta el producto (caja de 12, paquete de 10, etc.).
- **Qué pasa si está vacío**:
  - No se hace nada con el dato solo se marca la celda en amarillo.
- **Resultado esperado en salida**:
  - El campo se conserva sin cambios.

---

### 15. `Contenido` (Contenido del empaque)

- **Tipo de dato**: `Número` (Float o Int).
- **Qué hacer**:
  - Contenido del empaque (solo el numero, por ejemplo, 12 para representar 12 unidades por caja si la unidad de empaque es caja).
- **Qué pasa si está vacío**:
  - No se hace nada con el dato solo se marca la celda en amarillo.
- **Resultado esperado en salida**:
  - El campo se conserva sin cambios.

---

### 16. `Leadtime1` (Tiempo de entrega proveedor 1)

- **Tipo de dato**: `Número` (Días, Float o Int).
- **Qué hacer**:
  - Tiempo de entrega del proveedor 1 (en días).
- **Qué pasa si está vacío**:
  - No se hace nada con el dato solo se marca la celda en amarillo.
- **Resultado esperado en salida**:
  - El campo se conserva sin cambios.

---

### 17. `Proveedor2` (Proveedor alternativo)

- **Tipo de dato**: `Texto` (String).
- **Qué hacer**:
  - Nombre del proveedor alternativo.
- **Qué pasa si está vacío**:
  - No se hace nada con el dato solo se marca la celda en amarillo.
- **Resultado esperado en salida**:
  - El campo se conserva sin cambios.

---

### 18. `Costo2` (Costo proveedor 2)

- **Tipo de dato**: `Número` (Float o Int).
- **Qué hacer**:
  - Costo de proveedor alternativo.
- **Qué pasa si está vacío**:
  - No se hace nada con el dato solo se marca la celda en amarillo.
- **Resultado esperado en salida**:
  - El campo se conserva sin cambios.

---

### 19. `Leadtime2` (Tiempo de entrega proveedor 2)  

- **Tipo de dato**: `Número` (Días, Float o Int).
- **Qué hacer**:
  - Tiempo de entrega del proveedor 2 (en días).
- **Qué pasa si está vacío**:
  - No se hace nada con el dato solo se marca la celda en amarillo.
- **Resultado esperado en salida**:
  - El campo se conserva sin cambios.

---

### 20. `FechaUltimaVenta` (Fecha de la última venta)

- **Tipo de dato**: `Fecha` (DateTime).
- **Formato**: `DD-MM-YYYY`.
- **Qué hacer**:
  - Asegúrate de que la fecha sea correcta.
- **Qué pasa si está vacío**:
  - No se hace nada con el dato solo se marca la celda en amarillo.
- **Resultado esperado en salida**:
  - El campo se conserva sin cambios.

---

### 21. `Markup` (Margen de ganancia)

- **Tipo de dato**: `Número` (Float o Int).
- **Formato**: Porcentaje sin símbolo, por ejemplo `20` para 20%, o `1.2` para 120% (factor multiplicador).
- **Qué hacer**:
  - Indica el porcentaje de margen de ganancia deseado sobre el costo del producto.
  - Si tu ERP usa factor multiplicador (por ejemplo 1.3 para 30% de margen), usa ese formato.
- **Qué pasa si está vacío**:
  - No se hace nada con el dato solo se marca la celda en amarillo.
- **Qué pasa si no es numérico**:
  - El bot no podrá calcular el margen ni rellenar el precio a partir de `Costo1`, y se mostrará un mensaje de error.
- **Resultado esperado en salida**:
  - El campo se conserva tal cual, con valores numéricos limpios.
  - Si el usuario lo desea, el chatbot puede recalcular el `Precio` a partir de `Costo1` y `Markup` (por ejemplo: `Precio = Costo1 * (1 + Markup/100)` cuando el `Markup` está en porcentaje).

---

## 📌 Qué pasa si no se cumplen las condiciones

- **Si falta `SKU`**: No se pueden eliminar duplicados, pero el bot sigue funcionando.
- **Si falta `Precio` o `Costo1`**: No se rellenan precios ni costos, pero el bot sigue funcionando.
- **Si falta `Categoria`**: No se asigna categoría, pero el bot sigue funcionando.
- **Si `Precio` o `Costo1` no son numéricos**:
  - Se muestra un mensaje de error y no se rellenan precios ni costos.
  - El usuario debe corregir el archivo Excel (convertir texto a número).

---

## 📌 Resultados que debe esperar en el archivo de resultado

El archivo Excel de salida (`catalogo_limpio.xlsx`) contendrá:

- **SKU**: Único (sin duplicados).
- **Nombre**: Igual que el archivo de entrada o limpiado.
- **Categoria**: Limpia y completada (`Sin asignar` si estaba vacío).
- **Modelo**: Igual que el archivo de entrada o limpiado. En color amarillo si esta vacío.
- **Precio**: Limpio y rellenado con el promedio por categoría si es posible.
- **Costo1**: Limpio y sin cambios (no se calcula promedio).
- **Proveedor1**: Igual que el archivo de entrada o limpiado.
- **Estado**: Igual que el archivo de entrada o limpiado.
- **Columnas adicionales**: Conservadas tal cual, con cambios solo si el usuario así lo solicitó explícitamente.

---

## 📌 Mensajes de error posibles

- **`Columna 'Precio' contiene solo valores no numéricos`**:
  - Corrige tu Excel para que el campo `Precio` sea solo números.
- **`Columna 'Costo1' contiene solo valores no numéricos`**:
  - Corrige tu Excel para que el campo `Costo1` sea solo números.

---

## 📌 Soporte

Si tienes dudas o problemas, contacta a tu consultor ERP para más ayuda.
