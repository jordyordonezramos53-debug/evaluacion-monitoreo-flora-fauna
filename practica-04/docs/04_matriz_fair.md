# Entregable 4. Matriz de evaluación FAIR

Referencia: Wilkinson, M. D., Dumontier, M., Aalbersberg, I. J., … Mons, B. (2016). The FAIR Guiding Principles for scientific data management and stewardship. *Scientific Data, 3*, 160018. https://doi.org/10.1038/sdata.2016.18

**Escala:** 0 = no cumple · 1 = cumple parcialmente · 2 = cumple

| Principio | Criterio (Wilkinson et al., 2016) | Fuente original (SERFOR) | Puntaje | Base curada (este repositorio) | Puntaje |
|---|---|---|---|---|---|
| **F1** | Identificador único y persistente | La ficha tiene un identificador interno (`8ee450b1-…`), pero no un DOI. Los 214 archivos no tienen identificador de versión | 1 | **DOI de Zenodo** (10.5281/zenodo.24328237, todas las versiones; 10.5281/zenodo.24328238, v1.1), huella SHA-256 del original y versiones etiquetadas en GitHub | 2 |
| **F2** | Metadatos ricos | Descripción breve en la ficha, sin diccionario de datos | 1 | Diccionario completo, metadatos e informe de curaduría | 2 |
| **F3** | Los metadatos incluyen el identificador de los datos | La ficha enlaza los archivos, pero no dice cuál está vigente | 1 | `FUENTE.md` registra el archivo exacto, su URL y su SHA-256 | 2 |
| **F4** | Registrado en un recurso que se pueda buscar | Indexado en la Plataforma Nacional de Datos Abiertos | 2 | Repositorio público en GitHub (lo indexan los buscadores) | 2 |
| **A1** | Recuperable por protocolo estándar | HTTPS, aunque bloquea descargas automáticas (HTTP 418) | 1 | HTTPS desde GitHub, sin bloqueos | 2 |
| **A1.1** | Protocolo abierto y gratuito | Sí | 2 | Sí | 2 |
| **A1.2** | Autenticación cuando corresponda | Acceso público, pero **expone nombres y DNI** | 1 | Datos personales retirados (seudonimización) | 2 |
| **A2** | Los metadatos siguen accesibles aunque los datos no | La ficha se mantiene | 2 | Si se retiran los datos, el diccionario y `FUENTE.md` siguen en el repositorio | 2 |
| **I1** | Lenguaje formal y compartido | Extensión `.xls` que en realidad es XLSX; el CSV antiguo está mal formado | 0 | CSV UTF-8 estándar y fechas ISO 8601 | 2 |
| **I2** | Vocabularios que cumplen FAIR | Nombres científicos sin estandarizar; UBIGEO del INEI | 1 | Taxonomía enlazada al GBIF Backbone (`usageKey`) y UBIGEO del INEI | 2 |
| **I3** | Referencias a otros datos | Ninguna | 0 | Exportación Darwin Core con `taxonID` (URI de GBIF por nombre) y `locationID` (UBIGEO), que permiten cruzar con GBIF y con capas del INEI o del MINAM | 2 |
| **R1** | Atributos precisos y relevantes | Faltan unidades y la definición de la superficie | 1 | Unidades, definiciones y advertencias (superficie repetida) | 2 |
| **R1.1** | Licencia clara | ODC-BY | 2 | ODC-BY, la misma de la fuente, con atribución al SERFOR | 2 |
| **R1.2** | Procedencia detallada | Solo la fecha de corte | 1 | Registro de cambios, scripts y huella del original | 2 |
| **R1.3** | Estándares de la comunidad | No | 0 | Nomenclatura según GBIF y **exportación en Darwin Core** (`darwin_core_ocurrencias.csv`, script `05_exportar_darwin_core.py`) | 2 |
| | **Total** | | **16 / 30** | | **30 / 30** |

## Mejoras implementadas

1. **Localizable:** diccionario de datos, metadatos y huella SHA-256 del archivo exacto usado.
2. **Accesible:** se retiraron los datos personales, lo que hace la base publicable de forma responsable, y la descarga desde GitHub no tiene bloqueos.
3. **Interoperable:** CSV UTF-8 bien formado, columnas en `snake_case`, fechas ISO 8601 y especies enlazadas a GBIF.
4. **Reutilizable:** licencia explícita, procedencia completa, scripts que se pueden reproducir y banderas de calidad en lugar de borrar datos.

5. **Estándar de la comunidad:** la base curada se exporta con términos de **Darwin Core** (`scientificName`, `taxonRank`, `family`, `taxonID`, `stateProvince`, `locationID`, `degreeOfEstablishment` = cultivated), el estándar de datos de biodiversidad que usa GBIF (I3, R1.3).
6. **Cita:** el archivo `CITATION.cff` hace que GitHub muestre el botón *Cite this repository* con los autores del grupo.
7. **Identificador persistente:** el repositorio está archivado en **Zenodo** con el DOI [10.5281/zenodo.24328237](https://doi.org/10.5281/zenodo.24328237), que siempre lleva a la versión más reciente. Cada nueva versión publicada en GitHub (*release*) recibe su propio DOI automáticamente (F1).

## Recomendación al SERFOR (fuera del alcance del grupo)

- Publicar una versión vigente identificada, con DOI, y un diccionario de datos oficial.
