# Entregable 3. Informe de curaduría

**Base de datos:** Plantaciones forestales inscritas en el Registro Nacional de Plantaciones Forestales, por especie (SERFOR)
**Archivo original:** `Plantaciones_208.xls`, fecha de corte 11/06/2025 (procedencia y huella en [data/raw/FUENTE.md](../data/raw/FUENTE.md))
**Scripts:** [`01_diagnostico.py`](../scripts/01_diagnostico.py) → [`02_taxonomia_gbif.py`](../scripts/02_taxonomia_gbif.py) → [`03_curaduria.py`](../scripts/03_curaduria.py)

## 1. Diagnóstico inicial

Resultados de `01_diagnostico.py` sobre el archivo sin modificar. La tabla completa está en [`data/processed/diagnostico_inicial.csv`](../data/processed/diagnostico_inicial.csv).

| Aspecto | Resultado |
|---|---|
| Tamaño | 32 754 filas × 19 columnas |
| Unidad de registro | Plantación × especie (una plantación ocupa una fila por cada especie) |
| Plantaciones únicas | 16 204, de las cuales 5739 tienen más de una especie |
| Periodo de inscripción | 2014-2025 (2014 y 2015 con solo 3 y 25 filas) |
| Cobertura | 24 departamentos y 22 autoridades forestales (ARFFS) |
| Valores faltantes | 168 filas sin especie y 1 sin titular; ninguna otra columna tiene vacíos |
| Duplicados exactos | 0 |
| Códigos | UBIGEO: todos de 6 dígitos y coherentes con el departamento. DNI: todos de 8 dígitos. RUC: todos de 11 dígitos |
| Nombres de especie | 535 textos distintos: con y sin autor, epítetos con mayúscula, 33 identificados solo a género, 9 con espacios sobrantes |
| Datos personales | Nombre y número de documento de 12 921 titulares |

### Hallazgos principales

1. **La superficie se repite en cada especie de la misma plantación.** Ninguna plantación tiene superficies distintas entre sus filas, lo que confirma que el valor es de la plantación completa. Sumar todas las filas da **292 348 ha**, pero la superficie real, contando cada plantación una vez, es **110 852 ha**. El error infla el total **2,64 veces**. Es el error de análisis más importante que evita esta curaduría.
2. **Hay 68 filas con el mismo ID y la misma especie que no son duplicados.** Difieren en la finalidad (producción o protección) o en el tipo de plantación. Por eso se conservan y se marcan.
3. **Hay 16 filas con superficie = 0 ha**, un error verificable: una plantación inscrita no puede medir cero.
4. **1214 plantaciones tienen una superficie inusualmente grande** para la distribución (más de 13,78 ha, es decir, Q3 + 3·IQR). 22 superan las 500 ha y la mayor llega a 3587,7 ha. No hay evidencia de que sean errores, así que **no se eliminan**: se marcan para analizarlas por separado.
5. **La fuente tiene problemas de formato:** el archivo `.xls` es en realidad un XLSX, la ficha acumula 214 versiones sin indicar cuál está vigente, y el CSV de 2022 tiene 14 433 filas desalineadas por comas sin comillas.

## 2. Reglas aplicadas

Cada regla queda registrada con su número de casos en [`data/processed/registro_cambios.csv`](../data/processed/registro_cambios.csv).

| Regla | Qué se hizo | Casos | Tipo |
|---|---|---|---|
| R01 | Nombres de columnas a `snake_case` sin tildes | 19 columnas | Transformación |
| R02 | Quitar espacios sobrantes en los textos | 32 749 filas | Corrección |
| R03 | **Seudonimizar** a los titulares: nombre y documento se reemplazan por `TIT_00001`… y la tabla de correspondencia no se guarda | 12 921 titulares | Protección de datos |
| R04 | Periodo a entero, fecha de corte a ISO 8601 y superficie a número | 32 754 filas | Transformación |
| R05 | Marcar superficie = 0 (`flag_superficie_cero`) y excluirla de las sumas | 16 filas | Marca |
| R06 | Marcar superficies atípicas (`flag_superficie_atipica`, `flag_superficie_mayor_500ha`) | 1214 plantaciones | Marca |
| R07 | Agregar el nombre aceptado, la familia y el estado taxonómico según GBIF, sin borrar el nombre registrado | 32 586 filas | Transformación |
| R12 | **Revisión manual** de los 40 nombres que GBIF no resolvió: 32 identificados a género, 5 homónimos resueltos por autor, 2 errores de escritura y 1 híbrido ([`revision_taxonomica_manual.csv`](../data/processed/revision_taxonomica_manual.csv)) | 1111 filas | Corrección |
| R08 | Marcar las filas sin especie (`flag_sin_especie`) | 168 filas | Marca |
| R09 | Marcar el mismo ID y especie en varias filas (`flag_id_especie_repetido`) | 129 filas | Marca |
| R10 | Calcular el número de especies por plantación y documentar que la superficie no se suma por filas | 22 173 filas | Documentación |
| R11 | Marcar las plantaciones con más de una finalidad | 25 plantaciones | Marca |

**No se eliminó ninguna fila** (32 754 entran y 32 754 salen). Cada problema queda visible en una columna `flag_*` para que quien use la base decida si excluir esos casos.

## 3. Estandarización taxonómica

Cada uno de los 535 nombres distintos se consultó en el **GBIF Backbone Taxonomy** (`api.gbif.org/v1/species/match`, consulta del 17/11/2026). Las respuestas se guardaron en [`tabla_taxonomica.csv`](../data/processed/tabla_taxonomica.csv), que funciona como caché para que el resultado sea reproducible.

| Resultado | Nombres |
|---|---|
| Resueltos automáticamente (decisión ACEPTAR) | 495 |
| … de ellos, nombre ya aceptado | 436 |
| … de ellos, sinónimo actualizado al nombre aceptado | 58 |
| … de ellos, estado dudoso en GBIF | 1 |
| No resueltos por GBIF y **revisados a mano** (regla R12) | 40 |

En filas: 3746 filas tienen un nombre registrado que GBIF considera sinónimo, y 1111 filas tenían un nombre que GBIF no resolvió; todas quedaron resueltas con la revisión manual. **No queda ningún nombre pendiente.**

Ejemplos de sinónimos actualizados: *Caesalpinia spinosa* → *Tara spinosa* (tara), *Acacia nilotica* → *Vachellia nilotica*, *Cinnamomum zeylanicum* → *Cinnamomum verum*.

**Revisión manual (regla R12).** Los 40 nombres que GBIF no resolvió se decidieron uno por uno, consultando GBIF y World Flora Online (WFO). Cada decisión y su justificación están en [`revision_taxonomica_manual.csv`](../data/processed/revision_taxonomica_manual.csv):
- **32 nombres identificados solo a género** (por ejemplo, "*Pinus* sp." o "*Cedrela* sp"): es un nivel de identificación válido y se aceptan a género. *Hylocereus* se actualiza a *Selenicereus*, el género aceptado en GBIF.
- **5 homónimos resueltos por autor:** el mismo nombre existe con varios autores, y por eso GBIF no lo resolvió. Se eligió el autor neotropical o peruano: *Capparis flexuosa* (L.) L. → *Cynophalla flexuosa*; *Capparis ovalifolia* Ruiz & Pav. → *Beautempsia avicenniifolia*; *Pithecellobium multiflorum* (Kunth) Benth. → *Albizia multiflora*; *Ambrosia peruviana* Willd. → *Ambrosia cumanensis*; *Nectandra reticulata* (Ruiz & Pav.) Mez → *Nectandra villosa*. En 4 de ellos WFO acepta otro nombre; la diferencia queda anotada.
- **2 errores de escritura:** *Vainilla pompona* → *Vanilla pompona* y *Jatropa* sp → *Jatropha*.
- **1 híbrido comercial:** *Eucalyptus urograndis* → *Eucalyptus grandis* × *E. urophylla* (rango híbrido; sigue en el grupo *Eucalyptus* spp. del IPCC).

> Advertencia: GBIF es una referencia, no una autoridad única.
>
> **Verificación con World Flora Online (17/11/2026).** Se contrastaron 5 sinónimos con WFO. En 4 casos WFO coincide con GBIF: *Eucalyptus citriodora* → *Corymbia citriodora*, *Schizolobium amazonicum* → *S. parahyba*, *Tabebuia capitata* → *Handroanthus capitatus* y *T. incana* → *H. incanus*. En 1 caso difieren: **WFO acepta *Cedrela angustifolia* como especie**, mientras que GBIF la trata como sinónimo de *C. odorata*. Afecta a 188 plantaciones (1112 ha), que siguen en el mismo grupo del IPCC ("otras latifoliadas"), así que no cambia la estimación de carbono.
>
> **Decisión:** se mantiene GBIF como referencia única, porque así el proceso se puede repetir con una sola consulta automática. La discrepancia queda documentada, y la columna `especie_original` permite revertirla.
>
> **Contraste completo de los 58 sinónimos con WFO.** Resultado en [`contraste_wfo_sinonimos.csv`](../data/processed/contraste_wfo_sinonimos.csv): **45 coinciden** (en algunos casos con una variante ortográfica o precisando la subespecie), **11 difieren** (WFO acepta el nombre registrado o lo ubica en otro género) y **2 no tienen resultado** en WFO. Ninguna diferencia cambia el grupo de especies del IPCC, así que la estimación de carbono no se ve afectada. Para un análisis por especie, el usuario puede elegir la referencia con ese archivo.

## 4. Productos

| Archivo | Unidad | Filas | Uso |
|---|---|---|---|
| `plantaciones_especies_curada.csv` | Plantación × especie | 32 754 | Análisis por especie (frecuencia, composición) |
| `plantaciones_curada.csv` | Plantación | 16 204 | **Análisis de superficie**: suma correcta de hectáreas |
| `registro_cambios.csv` | Regla | 12 | Trazabilidad de la curaduría |
| `revision_taxonomica_manual.csv` | Nombre revisado | 40 | Decisión y justificación de la revisión manual |
| `contraste_wfo_sinonimos.csv` | Sinónimo | 58 | Comparación entre GBIF y World Flora Online |
| `darwin_core_ocurrencias.csv` | Plantación × especie | 32 586 | La base curada con términos de **Darwin Core** |
| `tabla_taxonomica.csv` | Nombre registrado | 535 | Equivalencias taxonómicas |

## 5. Evaluación de calidad y aptitud para investigación

| Criterio | Valoración | Comentario |
|---|---|---|
| Completitud | Alta | Menos del 1 % de vacíos (solo en especie) |
| Consistencia | Media | Superficie repetida por especie y varias finalidades en un mismo ID |
| Exactitud | No verificable | No hay forma de contrastar las superficies con campo ni con imágenes satelitales |
| Actualidad | Alta | Corte a junio de 2025 |
| Resolución espacial | Baja | Solo distrito (UBIGEO), sin coordenadas ni polígonos |

**Para qué sirve la base:**
- Superficie inscrita por especie, región, finalidad y año.
- Composición de especies.
- **Remociones potenciales** de CO₂, multiplicando la superficie por tasas de crecimiento por defecto, por ejemplo las del IPCC.

**Para qué NO sirve:**
- Calcular secuestro real ni tasas de secuestro: no hay edad, supervivencia, diámetros ni alturas.
- Saber cuánto de la superficie inscrita está plantada y en pie.
- Ubicar las plantaciones con precisión.
- Asignar la superficie a cada especie dentro de una plantación mixta, porque se desconoce la proporción de cada una.

## 6. Limitaciones de la curaduría

- El límite de atípico (Q3 + 3·IQR) es una decisión estadística: otro criterio marcaría otras plantaciones.
- La seudonimización es irreversible. Para reidentificar a un titular hay que volver a la fuente oficial.
- La consulta a GBIF depende de la versión del backbone en la fecha de consulta.
- No se verificó si una misma plantación aparece inscrita con otro ID.
