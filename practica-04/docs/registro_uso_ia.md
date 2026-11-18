# Entregable 7. Registro de uso de inteligencia artificial

**Grupo:** Las Abejitas · **Asignatura:** Evaluación y Monitoreo de Flora, Fauna y Sistemas Ecológicos

**Herramienta:** Claude (Anthropic).

Cada resultado de la IA se comprobó por un camino distinto al que lo produjo: la fuente original, otra herramienta o un recálculo.

| Uso | Instrucción (resumen) | Producto | Cómo se verificó | Correcciones |
|---|---|---|---|---|
| Lectura de la guía | Resumir lo que pide la práctica | Lista de actividades y de los 11 entregables | Se comparó con el PDF de la práctica | Ninguna |
| Búsqueda de fuentes | Buscar datos en OEFA, SENACE, SERNANP, INAIGEM y SERFOR; antecedentes y versiones de los estándares de carbono | Inventario de 17 fuentes, 4 antecedentes nacionales y versiones de GHG Protocol, Gold Standard y Verra | Se abrió cada enlace y cada referencia en su sitio original | Se actualizaron la ficha del SERFOR en el inventario, el título de un artículo y dos fechas de estándares |
| Código | Programar la lectura, limpieza, análisis y exportación de la base | Scripts `01` a `05` | Las cifras principales se recalcularon desde el archivo original con otra herramienta y se comparó la huella SHA-256 | Se corrigieron la regla para nombres con el epíteto en mayúscula y la agrupación de *Corymbia* |
| Redacción | Preparar borradores de los informes, las matrices, el proyecto y la presentación | Documentos de `docs/` y diapositivas | Las cifras de cada documento se contrastaron con las tablas de `data/processed/` | Se precisó la descripción de las plantaciones mixtas |
| Taxonomía | Contrastar los nombres de especies con GBIF y World Flora Online | Revisión manual de 40 nombres y contraste de 58 sinónimos | Consulta directa en GBIF y World Flora Online | Las diferencias entre ambas fuentes quedaron documentadas |

## Errores detectados en las respuestas de la IA

1. **Falso problema de tildes.** La IA creyó que el archivo tenía las tildes dañadas (`PRODUCCI�N`). Al leerlo en UTF-8 se vio que el archivo estaba bien y que el problema era la consola de Windows. Se descartó.
2. **Falsos duplicados.** 68 filas parecían repetidas, pero cambian en la finalidad o el tipo de plantación. No se eliminaron.
3. **Fechas desactualizadas.** El GHG Protocol ya publicó la versión 1.1 del LSR Standard y Verra aplazó la VCS v5 al 1/7/2027. Se corrigió al revisar las páginas oficiales.
4. **Sinonimia discutible.** GBIF trata *Cedrela angustifolia* como sinónimo de *C. odorata*, pero World Flora Online la acepta como especie. Se conservó el nombre original junto al aceptado.
