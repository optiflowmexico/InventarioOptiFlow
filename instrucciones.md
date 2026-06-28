# 📖 Manual de Operación - OptiFlow ERP

Bienvenido al sistema de preparación y limpieza de catálogos para **OptiFlow ERP**. Este módulo te permite procesar y validar tus plantillas de Excel, asegurando que los datos cumplan estrictamente con las reglas de negocio antes de ser integrados al sistema central. 🚀

---

## 💻 ¿Cómo usar la aplicación?
1. **Navegación:** Abre la aplicación web y utiliza el menú lateral izquierdo para seleccionar el módulo deseado.
2. **Carga:** Sube tu archivo Excel en formato `.xlsx`.
3. **Procesamiento:** Haz clic en el botón **Procesar catálogo**.
4. **Validación:** Revisa el análisis estadístico y los gráficos de resumen generados automáticamente en pantalla.
5. **Descarga:** Si el procesamiento es exitoso, haz clic en el botón **📥 Descargar archivo limpio (.xlsx)**.

---

## 📦 1. Módulo: Catálogo de Productos
Este componente valida la información comercial y logística de los artículos terminados destinados a la venta.

### 📌 Columnas Obligatorias (Estructura Base)
El archivo de Excel debe contar con los siguientes encabezados. El sistema es inteligente y los reconocerá aunque tengan variaciones en mayúsculas/minúsculas, espacios o guiones bajos:
* `SKU`: Identificador único del producto (alfanumérico, sin espacios). ¡No debe haber duplicados!
* `Nombre`: Título o descripción comercial corta del artículo.
* `Categoria`: Agrupación lógica de mercado (ej. *Línea Blanca, Electrónica*).
* `Modelo`: Código de fábrica o variante específica del modelo.
* `Precio`: Precio final de venta al público (numérico).
* `Costo1`: Costo base de adquisición del proveedor principal (numérico).
* `Proveedor1`: Nombre completo o razón social del proveedor asignado.
* `Estado`: Situación operativa del producto (ej. *Activo, Descontinuado*).

### 🔍 Columnas Adicionales Soportadas
Si tu archivo incluye las siguientes columnas, el sistema las conservará y procesará en el archivo de salida:
`CodigoBarras`, `Descripcion`, `Preciominimo`, `Stock`, `UnidadMedida`, `UnidadEmpaque`, `Contenido`, `Leadtime1`, `Proveedor2`, `Costo2`, `Leadtime2`, `FechaUltimaVenta`.

### 🛠️ Reglas de Limpieza y Automatización de Productos
* **Corrección de Textos:** Se eliminan espacios duplicados innecesarios al inicio y al final de cada celda.
* **Tratamiento de Vacíos Críticos ⚠️:** * Si `Nombre` está vacío, se rellenará automáticamente con el texto **"SIN NOMBRE"**.
  * Si `Categoria` está vacía, se rellenará automáticamente con **"Sin asignar"**.
  * Si `Modelo` o `Estado` están vacíos, se mantendrán en blanco y sus celdas se resaltarán en **Amarillo** en el Excel de salida indicando una anomalía para tu revisión.
* **Inteligencia de Precios Vacíos (Promedios) 📊:** Si el campo `Precio` viene vacío, el sistema calculará dinámicamente el precio promedio de los demás productos que pertenezcan a su **misma categoría** para rellenar el hueco de forma automática. Si no hay más productos en esa categoría, se dejará vacío y se pintará en amarillo.
* **Restricción de Costos:** Si el `Costo1` está vacío, no se calcula ningún promedio; se mantendrá en blanco y se marcará en amarillo.

---

## 🧪 2. Módulo: Catálogo de Materias Primas
Este componente gestiona los insumos puros, materiales de embalaje y componentes utilizados en el área de producción.

### 📌 Columnas Obligatorias (Estructura Base)
El archivo de Excel debe contener obligatoriamente las siguientes columnas:
* `Nombre`: Identificador único o descripción del insumo.
* `UnidadMedida`: Unidad base de consumo interno (ej. *Kg, Litros, Piezas*).
* `UnidadCompra`: Unidad en la que el proveedor surte el material (ej. *Caja, Tambor, Rollo*).
* `Contenido`: Cantidad de unidades de medida por unidad de compra (ej. *20*).
* `Proveedor1`: Nombre del distribuidor del insumo.
* `Costo1`: Costo económico por unidad de compra (numérico).
* `Stock`: Cantidad física actualmente disponible en el almacén (numérico).

### 🔍 Columnas Opcionales Soportadas
* `Descripcion`: Se puede incluir como referencia informativa, pero no es obligatoria para las operaciones lógicas del sistema.

### 🛠️ Reglas de Limpieza y Automatización de Materias Primas
* **Generación de Descripción de Compra 📝:** El sistema genera de forma automática una nueva columna compuesta llamada `DescripcionCompra` siguiendo la regla:  
  `[UnidadCompra] con [Contenido] [UnidadMedida]` *(Ejemplo: UnidadCompra "Caja", Contenido "20" y UnidadMedida "Piezas" generará de forma automática: "Caja con 20 Piezas")*.
* **Optimización Inteligente:** Si la `UnidadCompra` coincide exactamente con la `UnidadMedida` (ej. se compra por pieza y se mide por pieza), el sistema omitirá la descripción compuesta para evitar textos redundantes como *"Piezas con 1 Piezas"*.
* **Homologación Automática de Vacíos:** Si `UnidadCompra` y `Contenido` vienen vacíos, pero la `UnidadMedida` sí tiene valor, el motor asume por defecto la equivalencia 1:1 (`UnidadCompra = UnidadMedida` y `Contenido = 1`). Si `UnidadMedida` está vacía, no se construye la descripción compuesta.

---

## 🚨 Consideraciones Generales y Errores Comunes

### 1. Celdas en Amarillo (Anomalías) 🟨
Al descargar el archivo procesado (`catalogo_limpio.xlsx` o `catalogo_materias_primas_limpio.xlsx`), revisa minuciosamente las celdas iluminadas en amarillo. Indican que el sistema detectó datos faltantes y aplicó reglas automáticas de contingencia para salvar el registro, por lo que requieren tu validación visual.

### 2. Archivos Bloqueados o Abiertos 🔒
Asegúrate de **cerrar el archivo Excel en tu computadora** antes de cargarlo a la plataforma web. Si lo tienes abierto en programas como Microsoft Excel, el sistema no podrá procesarlo y arrojará un error de *Permiso Denegado*.

### 3. Resultados del Análisis en Pantalla 📊
La aplicación te mostrará un panel con:
* **Filas originales vs Filas finales:** Para asegurar que no se perdió ningún registro.
* **Conteo de campos vacíos o duplicados:** Evaluando columnas clave como `SKU` (en productos) o `Nombre` (en materias primas) para garantizar la integridad de tu base de datos.

### 4. Guía de Solución a Mensajes de Error Comunes 🛑
* **`Faltan columnas obligatorias: [Nombre_Columna]`**: Verifica la ortografía de tus encabezados en el Excel. No importa si están en mayúsculas o minúsculas, pero la palabra debe estar bien escrita.
* **`Columna 'Precio' contiene solo valores no numéricos`**: Asegúrate de que en las columnas de `Precio` o `Costo1` no existan letras, signos de pesos escritos a mano (`$`) o textos como "N/A". Deben ser celdas con formato de número puro.
* **`KeyError` / `AttributeError`**: Este error suele ocurrir si el archivo Excel sufrió un cambio estructural severo o si se interrumpió la conexión. Refresca la página con `F5` e intenta de nuevo.