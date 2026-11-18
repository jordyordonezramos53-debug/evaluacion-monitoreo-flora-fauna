# Práctica: Base de datos, secuestro de carbono e inteligencia artificial

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.24328237.svg)](https://doi.org/10.5281/zenodo.24328237)

Repositorio del grupo para la práctica de curaduría de datos ambientales institucionales, evaluación FAIR, trazabilidad en GitHub y formulación de un proyecto de investigación sobre carbono en ecosistemas terrestres.

**Asignatura:** Evaluación y Monitoreo de Flora, Fauna y Sistemas Ecológicos
**Docente:** Ing. Cuya Matos, Oscar Alejandro
**Grupo:** Las Abejitas

| N.º | Integrante | Código |
|---|---|---|
| 1 | Guardia Romero, Ángel David | 2024021549 |
| 2 | Ordoñez Ramos, Esthif Jordy | 2024021736 |
| 3 | Paucar Donayre, Mathias Salvador | 2024021772 |
| 4 | Paucar Quispe, Cielo Margoth | 2024021763 |
| 5 | Ramirez Pastrana, Katerin Yasuri | 2024021852 |
| 6 | Salvatierra Quispe, Giuliana Anais Amalia | 2024021914 |
| 7 | Sotomayor Acosta, Raulino Matsue | 2024034643 |
| 8 | Villegas Estrella, Lesli Sandra | 2024022056 |

**DOI (Zenodo):** [10.5281/zenodo.24328237](https://doi.org/10.5281/zenodo.24328237) · todas las versiones; la v1.1 tiene el DOI [10.5281/zenodo.24328238](https://doi.org/10.5281/zenodo.24328238)

**Herramienta de IA utilizada:** Claude (Anthropic); ver el [registro de uso de IA](docs/registro_uso_ia.md)

## Flujo de trabajo

Repositorio institucional → recuperación de datos → diagnóstico de calidad → curaduría → evaluación FAIR → trazabilidad en GitHub → análisis con apoyo de IA → identificación de brechas → proyecto de investigación

## Estructura del repositorio

```
├── README.md                  ← este archivo
├── requirements.txt           ← versiones de Python y librerías
├── data/
│   ├── inventario/            ← inventario de repositorios (Entregable 1)
│   ├── raw/                   ← ficha de procedencia (los originales no se publican: tienen DNI)
│   └── processed/             ← base curada, tablas de revisión taxonómica y exportación Darwin Core
├── docs/                      ← informes, matrices, diccionario y registros
├── scripts/                   ← curaduría, análisis exploratorio y exportación Darwin Core, en orden
├── figures/                   ← gráficos generados por los scripts
├── CITATION.cff               ← cómo citar este repositorio
└── LICENSE                    ← licencia del código (MIT)
```

## Entregables

| N.º | Entregable | Archivo |
|---|---|---|
| 1 | Inventario de repositorios institucionales | [docs/01_inventario_repositorios.md](docs/01_inventario_repositorios.md) |
| 2 | Base de datos original y curada | [data/raw/FUENTE.md](data/raw/FUENTE.md) (original referenciado) · [data/processed/](data/processed/) |
| 3 | Informe de curaduría | [docs/03_informe_curaduria.md](docs/03_informe_curaduria.md) |
| 4 | Matriz FAIR | [docs/04_matriz_fair.md](docs/04_matriz_fair.md) |
| 5 | Diccionario de datos y metadatos | [docs/05_diccionario_datos.md](docs/05_diccionario_datos.md) |
| 6 | Repositorio GitHub | [github.com/jordyordonezramos53-debug/practica-carbono-plantaciones](https://github.com/jordyordonezramos53-debug/practica-carbono-plantaciones) |
| 7 | Registro de uso de IA | [docs/registro_uso_ia.md](docs/registro_uso_ia.md) |
| 8 | Matriz comparativa de metodologías de carbono | [docs/08_matriz_metodologias_carbono.md](docs/08_matriz_metodologias_carbono.md) |
| 9 | Análisis exploratorio de datos | [docs/09_analisis_exploratorio.md](docs/09_analisis_exploratorio.md) · [figures/](figures/) |
| 10 | Proyecto de investigación | [docs/10_proyecto_investigacion.md](docs/10_proyecto_investigacion.md) |

## Datos utilizados

**Plantaciones forestales inscritas en el Registro Nacional de Plantaciones Forestales, por especie** (SERFOR), con corte al 11/06/2025: 32 754 registros de 16 204 plantaciones (110 852 ha), de 2014 a 2025. Los archivos originales no se suben porque contienen nombres y DNI; su procedencia y huella están en [data/raw/FUENTE.md](data/raw/FUENTE.md).

## Cómo reproducir

1. Instalar Python 3.13 y las dependencias:
   ```bash
   pip install -r requirements.txt
   ```
2. Descargar los originales en `data/raw/` siguiendo [data/raw/FUENTE.md](data/raw/FUENTE.md).
3. Ejecutar los scripts en orden desde la carpeta raíz del repositorio:
   ```bash
   python scripts/01_diagnostico.py
   python scripts/02_taxonomia_gbif.py
   python scripts/03_curaduria.py
   python scripts/04_analisis_exploratorio.py
   python scripts/05_exportar_darwin_core.py
   ```
   `02_taxonomia_gbif.py` reutiliza `data/processed/tabla_taxonomica.csv` si ya existe. Para volver a consultar GBIF hay que borrar ese archivo antes.

## Fuentes y licencias

Los datos provienen de la Plataforma Nacional de Datos Abiertos del Perú y se distribuyen bajo la licencia indicada en cada ficha (en su mayoría, Open Data Commons Attribution). Los datos personales que contengan las fuentes originales no se publican en este repositorio.

| Contenido | Licencia |
|---|---|
| Datos curados (`data/`) | ODC-BY 1.0, la misma de la fuente. Citar al SERFOR |
| Código (`scripts/`) | MIT (ver `LICENSE`) |
| Documentos (`docs/`) y figuras | CC BY 4.0 |

Para citar este trabajo, usar el botón *Cite this repository* de GitHub (archivo `CITATION.cff`) o el DOI de Zenodo: Guardia Romero, Á. D., Ordoñez Ramos, E. J., Paucar Donayre, M. S., Paucar Quispe, C. M., Ramirez Pastrana, K. Y., Salvatierra Quispe, G. A. A., Sotomayor Acosta, R. M., & Villegas Estrella, L. S. (2026). *Remociones potenciales de CO2 de las plantaciones forestales inscritas en el Perú: curaduría FAIR del registro del SERFOR* (v1.1) [Software y datos]. Zenodo. https://doi.org/10.5281/zenodo.24328237
