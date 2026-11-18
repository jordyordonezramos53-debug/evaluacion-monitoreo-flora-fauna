# Entregable 5. Diccionario de datos y metadatos

## Metadatos del conjunto curado

| Elemento | Valor |
|---|---|
| Título | Plantaciones forestales inscritas en el Perú (SERFOR), base curada y seudonimizada |
| Descripción | Registro Nacional de Plantaciones Forestales con corte al 11/06/2025, curado para investigación: seudonimizado, con taxonomía estandarizada según GBIF y banderas de calidad |
| Fuente original | SERFOR, Plataforma Nacional de Datos Abiertos ([ficha](https://www.datosabiertos.gob.pe/dataset/plantaciones-forestales-inscritas-en-el-registro-nacional-de-plantaciones-forestales-por)) |
| Archivo de origen | `Plantaciones_208.xls`, SHA-256 `dc98fc14…f51e7b2c9` |
| Cobertura temporal | Inscripciones de 2014 a 2025 |
| Cobertura espacial | Perú: 24 departamentos, con resolución distrital (UBIGEO INEI) |
| Formato | CSV, UTF-8, separador coma, punto decimal |
| Licencia | ODC-BY, la misma de la fuente. Citar al SERFOR |
| Procesamiento | `scripts/01_diagnostico.py`, `02_taxonomia_gbif.py`, `03_curaduria.py`, `05_exportar_darwin_core.py` |
| Versión | 1.1 (2026-11-17): revisión taxonómica manual y exportación Darwin Core |
| Identificador persistente | DOI [10.5281/zenodo.24328237](https://doi.org/10.5281/zenodo.24328237) (Zenodo) |
| Contacto | Grupo Las Abejitas (integrantes en el README) |

## Archivo `plantaciones_especies_curada.csv` (una fila por plantación × especie)

| Variable | Tipo | Unidad / formato | Definición | Origen | Criterio de calidad |
|---|---|---|---|---|---|
| `id_plantacion` | entero | — | Identificador de la plantación en el registro del SERFOR | `ID PLANTACION` | Se repite en cada especie de la plantación |
| `periodo` | entero | año | Año de inscripción en el registro (no es el año de plantación) | `PERIODO` | 2014-2025 |
| `fecha_corte` | fecha | AAAA-MM-DD | Fecha de corte de la información | `FECHA CORTE` | Única: 2025-06-11 |
| `departamento`, `provincia`, `distrito` | texto | — | Ubicación político-administrativa | Original | Coherentes con el UBIGEO |
| `ubigeo` | texto | 6 dígitos | Código de distrito (INEI) | `UBIGEO` | Se guarda como texto para conservar el cero inicial |
| `arffs` | texto | — | Autoridad Regional Forestal (GORE) o Administración Técnica Forestal (ATFFS) que inscribió | `ARFFS` | 22 valores |
| `sede` | texto | — | Sede de la autoridad forestal | `SEDE` | — |
| `numero_certificado` | texto | — | Número del certificado de inscripción | `NUMERO CERTIFICADO` | Permite rastrear el registro hasta la fuente |
| `id_titular` | texto | `TIT_nnnnn` | Seudónimo del titular | Derivado (R03) | Irreversible; la correspondencia no se guarda |
| `tipo_persona` | categoría | — | PERSONA NATURAL, PERSONA JURÍDICA, OTROS | `TIPO PERSONA` | — |
| `tipo_documento` | categoría | — | DNI, RUC, CARNET DE EXTRANJERIA, PASAPORTE, OTROS | `TIPO DOCUMENTO` | El número de documento se eliminó |
| `regimen_tenencia` | categoría | — | Predio privado, comunidad nativa o campesina, dominio público | `REGIMEN TENENCIA` | 1 fila con "COMUNIDAD" sin especificar |
| `finalidad` | categoría | — | PRODUCCIÓN, PROTECCIÓN, RESTAURACIÓN | `FINALIDAD` | Puede variar dentro de una misma plantación |
| `tipo_plantacion` | categoría | — | ARBOLES, MATAS, ARBORESCENTE, CEPAS | `TIPO PLANTACION` | — |
| `especie_original` | texto | — | Nombre científico tal como se registró (sin espacios sobrantes) | `ESPECIE` | Se conserva para trazabilidad |
| `nombre_aceptado` | texto | — | Nombre aceptado según GBIF (especie, o género si no se identificó a especie) | Derivado (R07) | Ver `decision_taxonomica` |
| `familia` | texto | — | Familia botánica según GBIF | Derivado (R07) | — |
| `estado_taxonomico_gbif` | categoría | — | ACCEPTED, SYNONYM o DOUBTFUL | GBIF | — |
| `rango_taxonomico` | categoría | — | SPECIES, SUBSPECIES, VARIETY, GENUS o HYBRID | GBIF o revisión manual (R12) | — |
| `coincidencia_gbif` | categoría | — | EXACT, FUZZY o HIGHERRANK | GBIF | — |
| `decision_taxonomica` | categoría | — | ACEPTAR (resuelto por GBIF) o REVISADO_MANUAL (regla R12) | Derivado | `02_taxonomia_gbif.py` y `revision_taxonomica_manual.csv` |
| `nivel_identificacion` | categoría | — | especie, género o superior, híbrido, sin dato | Derivado | — |
| `superficie_plantacion_ha` | decimal | hectáreas (ha) | Superficie **de la plantación completa** | `SUPERFICIE PLANTACION` | ⚠️ Se repite en cada especie: **no sumar en este archivo** |
| `n_especies_plantacion` | entero | — | Número de especies distintas (nombre aceptado) en la plantación | Derivado (R10) | — |
| `flag_superficie_cero` | lógico | — | Verdadero si la superficie es 0 ha | Derivado (R05) | Excluir de las sumas |
| `flag_superficie_atipica` | lógico | — | Verdadero si la superficie es > 13,78 ha (Q3 + 3·IQR) | Derivado (R06) | Valor inusual, no error |
| `flag_superficie_mayor_500ha` | lógico | — | Verdadero si la superficie es > 500 ha | Derivado (R06) | — |
| `flag_sin_especie` | lógico | — | Verdadero si la fila no tiene especie | Derivado (R08) | — |
| `flag_id_especie_repetido` | lógico | — | Verdadero si el mismo ID y especie aparecen en varias filas | Derivado (R09) | No son duplicados |

## Archivo `plantaciones_curada.csv` (una fila por plantación)

Tiene las mismas variables de ubicación, autoridad, titular y banderas que el archivo anterior, más estas:

| Variable | Tipo | Definición |
|---|---|---|
| `finalidades` | texto | Todas las finalidades de la plantación, separadas por `\|` |
| `tipos_plantacion` | texto | Todos los tipos de plantación, separados por `\|` |
| `especies_aceptadas` | texto | Nombres aceptados de las especies, separados por `\|` |
| `n_especies` | entero | Número de especies distintas |
| `superficie_ha` | decimal (ha) | Superficie de la plantación, contada **una sola vez**. Es el archivo correcto para sumar superficies |
| `flag_varias_finalidades` | lógico | Verdadero si la plantación tiene más de una finalidad |

## Archivos auxiliares

- **`tabla_taxonomica.csv`**: una fila por nombre registrado, con la respuesta de GBIF (nombre canónico, nombre científico con autor, estado, rango, nombre aceptado, género, familia, tipo de coincidencia, confianza, `usageKey`, decisión y fecha de consulta).
- **`registro_cambios.csv`**: una fila por regla, con la columna afectada, el número de casos, la unidad, el tipo de cambio y la justificación.
- **`diagnostico_inicial.csv`**: los indicadores de calidad del archivo original.
- **`revision_taxonomica_manual.csv`**: una fila por cada uno de los 40 nombres revisados a mano, con el nombre aceptado, la familia, el rango, el motivo (IDENTIFICADO_A_GENERO, HOMONIMO_RESUELTO, ERROR_DE_ESCRITURA o HIBRIDO_COMERCIAL), el autor elegido, el nombre en World Flora Online y la justificación.
- **`contraste_wfo_sinonimos.csv`**: los 58 sinónimos de GBIF comparados con World Flora Online (COINCIDE, DIFIERE o SIN_RESULTADO_WFO).

## Archivo `darwin_core_ocurrencias.csv` (términos de Darwin Core)

Una fila por plantación × especie identificada (32 586 filas; se omiten las 168 filas sin especie porque Darwin Core exige un nombre científico). No contiene datos de titulares. Términos según https://dwc.tdwg.org/terms/.

**Valores comunes a todo el archivo** (no se repiten en cada fila): *datasetName* = Registro Nacional de Plantaciones Forestales del Perú, base curada (grupo Las Abejitas); *license* = ODC-BY 1.0 (https://opendatacommons.org/licenses/by/1-0/); *rightsHolder* = Servicio Nacional Forestal y de Fauna Silvestre (SERFOR).

| Término Darwin Core | Variable de la base curada | Observación |
|---|---|---|
| `occurrenceID` | `id_plantacion` + número de fila | Identificador único: `SERFOR-RNPF-<id>-<n>` |
| `basisOfRecord` | — | `HumanObservation` |
| `degreeOfEstablishment` | — | `cultivated` (plantación) |
| `institutionCode`, `collectionCode` | — | `SERFOR`, `RNPF` |
| `year` | `periodo` | **Año de inscripción**, no de plantación |
| `country`, `countryCode` | — | Peru, PE |
| `stateProvince`, `county`, `municipality` | `departamento`, `provincia`, `distrito` | — |
| `locationID` | `ubigeo` | `UBIGEO:<código INEI>` |
| `scientificName` | `nombre_aceptado` | — |
| `verbatimIdentification` | `especie_original` | Nombre tal como se registró |
| `taxonRank` | `rango_taxonomico` | species, subspecies, variety, genus o nothospecies (híbrido) |
| `family`, `kingdom` | `familia`, — | kingdom = Plantae |
| `taxonID` | `gbif_usage_key` | URI de GBIF; vacío en los nombres revisados a mano |
| `identificationRemarks` | `decision_taxonomica` | GBIF o revisión manual (R12) |
| `occurrenceRemarks` | `flag_*` | Banderas de calidad en texto |
| `dynamicProperties` | `id_plantacion`, `superficie_plantacion_ha`, `finalidad`, `tipo_plantacion` | JSON |
