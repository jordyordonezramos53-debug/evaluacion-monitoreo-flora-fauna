# Procedencia de los datos originales

Los archivos originales **no se publican en este repositorio** porque contienen datos personales: nombres y números de DNI o RUC de los titulares de las plantaciones. Para reproducir el trabajo hay que descargarlos de la fuente oficial y colocarlos en esta carpeta.

| Campo | Valor |
|---|---|
| Conjunto de datos | Plantaciones forestales inscritas en el Registro Nacional de Plantaciones Forestales, por especie [SERFOR] |
| Institución | Servicio Nacional Forestal y de Fauna Silvestre (SERFOR) |
| Repositorio | Plataforma Nacional de Datos Abiertos del Perú |
| Ficha | https://www.datosabiertos.gob.pe/dataset/plantaciones-forestales-inscritas-en-el-registro-nacional-de-plantaciones-forestales-por |
| Licencia | Open Data Commons Attribution License (ODC-BY) |
| Fecha de descarga | 2026-11-17 |

## Archivos

| Archivo | Enlace directo | Publicado | Tamaño (bytes) | SHA-256 | Uso |
|---|---|---|---|---|---|
| `Plantaciones_208.xls` | https://www.datosabiertos.gob.pe/sites/default/files/Plantaciones_208.xls | 12/06/2025 | 3 174 776 | `dc98fc142b13ac2191a370d1cc2320fad4b0ecc3aace00cdf506411f51e7b2c9` | **Base principal** (fecha de corte 11/06/2025) |
| `DataSetPlantaciones_0.csv` | https://www.datosabiertos.gob.pe/sites/default/files/DataSetPlantaciones_0.csv | 17/07/2024 | 3 460 212 | `a925960d9fc28d0b865e15b0e7b98baf66e108263c3950e05233b39af61138cd` | Comparación con la versión anterior (corte 17/02/2022) |

## Cómo descargarlos

1. Abrir la ficha en el navegador y descargar los dos archivos con el botón **Descargar**. El servidor bloquea descargas automáticas (por ejemplo con `curl` responde HTTP 418), por eso la descarga se hace a mano.
2. Guardarlos en `data/raw/` con los nombres de la tabla.
3. Comprobar la huella. Los scripts lo hacen solos y avisan si no coincide:
   ```bash
   sha256sum data/raw/Plantaciones_208.xls
   ```

## Observaciones sobre la fuente

- La ficha tiene **214 archivos**: el SERFOR publica cada actualización como un archivo nuevo sin retirar los anteriores ni indicar cuál está vigente. Se usó el más reciente según la fecha del servidor.
- `Plantaciones_208.xls` tiene extensión `.xls`, pero en realidad es un libro **XLSX** (Office Open XML).
- En la versión CSV de 2022, el campo del titular contiene comas sin comillas ("APELLIDO, NOMBRE"). Por eso 14 433 de 15 220 filas tienen más campos que la cabecera y no se pueden leer como CSV estándar.
