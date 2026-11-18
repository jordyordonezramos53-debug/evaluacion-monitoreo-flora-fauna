# Registro de decisiones metodológicas

| N.º | Fecha | Decisión | Alternativas consideradas | Justificación |
|---|---|---|---|---|
| D1 | 2026-11-17 | Usar la base de **plantaciones forestales del SERFOR** | Deforestación en ANP (SERNANP); flora y fauna (OEFA) | Permite abordar las **remociones (secuestro) potenciales**, el tema central de la práctica, y ofrece mucho material de curaduría |
| D2 | 2026-11-17 | Usar `Plantaciones_208.xls` (corte 11/06/2025) como base principal | CSV de 2022 | Es la versión más reciente según la fecha del servidor. El CSV de 2022 está mal formado (comas sin comillas) |
| D3 | 2026-11-17 | **No publicar los archivos originales** en GitHub y seudonimizar a los titulares | Publicar tal cual; eliminar las columnas sin seudónimo | Contienen nombres y DNI de personas naturales. El seudónimo permite contar plantaciones por titular sin identificarlo |
| D4 | 2026-11-17 | La superficie se analiza **una vez por plantación** (tabla `plantaciones_curada.csv`) | Repartir la superficie entre especies en partes iguales | La fuente no informa la proporción de cada especie. Repartirla sería inventar un dato; se documenta como limitación |
| D5 | 2026-11-17 | **Marcar y no eliminar** los valores inusuales (Q3 + 3·IQR) y las superficies de 0 ha | Eliminar atípicos | La guía pide no eliminar valores inusuales sin evidencia. La superficie de 0 ha se excluye de las sumas, pero se conserva |
| D6 | 2026-11-17 | Estandarizar la taxonomía con el **GBIF Backbone** y guardar la consulta como caché | World Flora Online; POWO | GBIF tiene una API pública y gratuita que se puede automatizar. La caché asegura la reproducibilidad. Los 58 sinónimos se contrastaron con WFO (`contraste_wfo_sinonimos.csv`) |
| D7 | 2026-11-17 | Usar `periodo` como año de **inscripción**, no de plantación | Usarlo como edad de la plantación | La ficha del SERFOR lo define como año de inscripción. La base no permite conocer la edad real |
| D8 | 2026-11-17 | Resolver a mano los 40 nombres que GBIF no resolvió (regla R12), con una tabla de decisiones | Dejarlos sin resolver; eliminarlos | Son 1111 filas. Una tabla con justificación por nombre mantiene la trazabilidad y no borra el nombre original |
| D9 | 2026-11-17 | Exportar la base curada en Darwin Core | Publicar solo el CSV propio | Es el estándar de datos de biodiversidad (GBIF) y mejora la interoperabilidad (FAIR I3 y R1.3) |
