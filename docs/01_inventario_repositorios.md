# Entregable 1. Inventario comparativo de repositorios institucionales

**Fecha de revisión:** 17 de noviembre de 2026
**Tabla completa (17 fuentes, 20 campos):** [`data/inventario/inventario_repositorios.csv`](../data/inventario/inventario_repositorios.csv)

## 1. Método de búsqueda

1. Se revisó la **Plataforma Nacional de Datos Abiertos** (datosabiertos.gob.pe) buscando por el nombre de cada institución (OEFA, SENACE, SERNANP, INAIGEM y SERFOR) y por palabras clave del tema (*carbono*, *biomasa*, *bosque*, *flora*, *fauna*, *vegetación*, *cobertura vegetal*).
2. Se revisaron los portales propios de cada institución: GEOSERFOR, GEO ANP (SERNANP), el Repositorio Digital del INAIGEM y la plataforma PIFA del OEFA.
3. En los conjuntos con mayor potencial se abrió el archivo de datos para comprobar las columnas, el número de registros y los problemas visibles. No se trabajó solo con la descripción del portal.
4. Para cada fuente se registró: el repositorio, la naturaleza de los datos, el periodo, la unidad de observación, el formato, las condiciones de descarga, la licencia y las restricciones de uso, como pide la guía (actividad A).

## 2. Resultados por institución

| Institución | Conjuntos en datos abiertos | Lo más útil para el tema carbono | Formato y licencia | Valoración |
|---|---|---|---|---|
| **SERNANP** | 6 | **Deforestación en ANP 2021-2023** (5129 polígonos, 31 ANP, causa, tipo de bosque, área en ha) | CSV + diccionario + metadatos · ODC-BY | ⭐⭐⭐ Alta |
| **SERFOR** | 8 | **Plantaciones forestales por especie 2014-2025** (32 754 filas en el XLSX con corte al 11/06/2025; la versión CSV de 2022 tiene 15 220; superficie en ha, especie, finalidad) | CSV/XLS · ODC-BY | ⭐⭐⭐ Alta, con datos personales que hay que proteger |
| **OEFA** | 92 (la mayoría administrativos) | **EAT Biota (flora y fauna)**: 18 445 registros taxonómicos | CSV + diccionario + metadatos · ODC-BY | ⭐⭐ Media (biodiversidad; sin biomasa) |
| **INAIGEM** | 22 | Humedad del suelo en bofedales; carbono negro (aerosol) | CSV + diccionario + metadatos · ODC-BY | ⭐ Baja para carbono del ecosistema |
| **SENACE** | 23 (administrativos) | Certificaciones ambientales; las líneas base biológicas están en expedientes PDF | CSV · ODC-BY | ⭐ Baja como datos tabulares |

### Observaciones clave

- **El "carbono negro" del INAIGEM no es carbono almacenado.** Es hollín en la atmósfera, medido con un aetalómetro. No sirve para estimar reservas ni secuestro, aunque el nombre pueda confundir.
- **SENACE** publica en datos abiertos solo registros administrativos. Los inventarios de flora y fauna de las líneas base están dentro de los EIA en PDF y extraerlos llevaría semanas.
- **OEFA** tiene muchos datos de calidad de agua, suelo y aire. Para flora y fauna, la base EAT Biota está bien estructurada, pero no tiene coordenadas, abundancia ni biomasa.
- **SERFOR, plantaciones:** el archivo trae **nombres y DNI de los titulares**, que son datos personales. No deben republicarse en GitHub; se seudonimizarán. Además se detectaron dos problemas que servirán para la curaduría:
  - la superficie de una plantación se repite en cada fila de especie, así que sumarla directamente la cuenta varias veces;
  - el campo `TX_TITULAR` contiene comas sin comillas (por ejemplo, "APELLIDO, NOMBRE"), lo que desalinea las columnas del CSV.
- **SERNANP, deforestación:** es la base más limpia y tiene diccionario y metadatos oficiales, lo que facilita la evaluación FAIR. Registra pérdida de bosque, es decir, **emisiones**, y **no secuestro**.

## 3. Bases de datos candidatas

| | Opción A (recomendada) | Opción B | Opción C |
|---|---|---|---|
| **Base** | SERNANP: deforestación en ANP | SERFOR: plantaciones forestales | OEFA: EAT Biota (flora y fauna) |
| **Pregunta posible** | ¿Cuánto carbono se emitió por deforestación en las ANP entre 2021 y 2023, según causa y tipo de bosque? | ¿Cuál es el potencial de remoción de CO₂ de las plantaciones inscritas, por especie y región? | ¿Cómo varía la riqueza de especies entre evaluaciones y métodos de muestreo? |
| **Magnitud de carbono** | Emisiones por pérdida de existencias (área × factor de emisión) | Remociones potenciales (área × tasa de crecimiento IPCC) | Ninguna (tema de biodiversidad) |
| **Tamaño** | 5129 registros, 11 columnas | 32 754 filas, 19 columnas (XLSX, corte 11/06/2025) | 18 445 registros, 14 columnas |
| **Esfuerzo de curaduría** | Bajo-medio | Alto (datos personales, CSV roto, áreas repetidas) | Medio (estandarización taxonómica) |
| **Encaje con GHG / Gold Standard / Verra** | Bueno: REDD+ y datos de actividad | Bueno: forestación y reforestación (A/R) | Débil |
| **Riesgo** | Necesita factores de emisión externos | No tiene edad ni supervivencia de las plantaciones: solo da un potencial | No responde al tema carbono |

**Recomendación:** la **Opción A** como base principal. Es la más viable para el plazo de esta semana porque viene limpia, con diccionario y licencia abierta, y se relaciona directamente con el carbono. La base **C01 del MINAM (bosque/no bosque)** queda como complemento opcional para comparar la pérdida dentro y fuera de las ANP. Si el grupo prefiere hablar de **secuestro** y no de emisiones, conviene la **Opción B**, que exige más curaduría.

### Decisión del grupo (17/11/2026)

El grupo eligió la **Opción B (SERFOR, plantaciones forestales)** para abordar el **secuestro** (remociones) de carbono, y no solo las emisiones. A cambio acepta un trabajo de curaduría mayor. Ver [`decisiones_metodologicas.md`](decisiones_metodologicas.md).

## 4. Limitaciones de este inventario

- Para las fuentes marcadas como "No verificado" en la tabla, no se descargó ni abrió el archivo; los datos salen solo de la ficha del portal.
- No se exploró en detalle la PIFA del OEFA (es una aplicación web que no carga contenido legible de forma automática) ni el buscador de expedientes del SENACE.
- La licencia ODC-BY permite reutilizar y redistribuir **citando la fuente**. Se confirmó en las fichas de las tres bases candidatas (SERNANP, SERFOR y OEFA) el 17/11/2026.
