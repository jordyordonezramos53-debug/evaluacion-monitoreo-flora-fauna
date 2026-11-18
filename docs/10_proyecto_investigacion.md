# Entregable 10. Proyecto de investigación

## 1. Título

**Remociones potenciales de CO₂ de las plantaciones forestales inscritas en el Registro Nacional de Plantaciones Forestales del Perú (2014-2025): estimación de nivel 1 por grupo de especies, departamento y finalidad**

**Delimitación:**
- **Espacial:** 24 departamentos del Perú, con resolución distrital (UBIGEO).
- **Temporal:** inscripciones de 2014 a 2025, con corte al 11/06/2025.
- **Unidad de análisis:** la plantación inscrita (16 195 plantaciones con superficie válida, 110 852 ha).
- **Temática:** remociones **potenciales** anuales de CO₂ en biomasa viva (aérea y subterránea). No se estiman reservas, secuestro medido, emisiones por cosecha ni carbono del suelo.

## 2. Planteamiento y formulación del problema

### 2.1 Planteamiento

El Perú promueve las plantaciones forestales como actividad productiva y como medida de mitigación del cambio climático. El SERFOR administra el Registro Nacional de Plantaciones Forestales, creado por el Reglamento para la Gestión de las Plantaciones Forestales y los Sistemas Agroforestales (D. S. N.º 020-2015-MINAGRI), y publica sus datos en la Plataforma Nacional de Datos Abiertos.

Sin embargo, el registro se creó con fines **administrativos** y no para estimar carbono. La curaduría de esta práctica mostró cuatro problemas:
1. La superficie se repite en cada especie de una plantación. Sumarla directamente **la sobreestima 2,64 veces** (292 348 ha frente a 110 852 ha reales).
2. No hay coordenadas, edad ni supervivencia de las plantaciones.
3. El 97,9 % de la superficie es de **producción**, por lo que el carbono almacenado es temporal.
4. El 20 % de la superficie corresponde a plantaciones que mezclan especies de distintos grupos del IPCC, sin proporción conocida entre ellas.

En estas condiciones, cualquier cifra de "carbono capturado por las plantaciones inscritas" que no considere estos sesgos puede estar muy inflada. No se conoce cuánto CO₂ **podrían** remover anualmente las plantaciones inscritas, cómo se distribuye ese potencial ni qué parte tiene permanencia de largo plazo.

### 2.2 Formulación

**Problema general:** ¿Cuál es la magnitud de las remociones potenciales anuales de CO₂ en la biomasa viva de las plantaciones forestales inscritas en el Registro Nacional de Plantaciones Forestales del Perú entre 2014 y 2025, y cómo se distribuye por grupo de especies, departamento y finalidad?

**Problemas específicos:**
1. ¿Cuánta superficie inscrita corresponde a cada grupo de especies compatible con las categorías del IPCC, y cuánta no puede asignarse a un solo grupo?
2. ¿Cuál es la remoción potencial anual de CO₂, con su intervalo de incertidumbre, por grupo de especies y por departamento?
3. ¿Qué proporción de las remociones potenciales corresponde a plantaciones de protección o restauración, con mayor potencial de permanencia, frente a las de producción?
4. ¿Cuánto cambia la estimación cuando se consideran distintos supuestos de supervivencia de las plantaciones?

## 3. Justificación

- **Científica:** el estudio cuantifica la magnitud de un sesgo real del registro (el conteo repetido de superficie) y propone un procedimiento reproducible y auditable en GitHub para convertir un registro administrativo en evidencia de nivel 1. El procedimiento también sirve para otros registros forestales.
- **Ambiental:** ofrece un **orden de magnitud con su incertidumbre** del aporte potencial de las plantaciones inscritas a las remociones de CO₂. Evita sobreestimaciones y separa el potencial temporal (producción) del de largo plazo (protección y restauración).
- **Práctica:** identifica qué información debería agregar el SERFOR al registro (coordenadas, año de plantación, supervivencia, proporción de especies) para que pueda usarse en el monitoreo de carbono. Esto se relaciona con requisitos del GHG Protocol, Gold Standard y Verra (ver [entregable 8](08_matriz_metodologias_carbono.md)).
- **Ética y legal:** la base trabajada protege los datos personales de los titulares, conforme a la Ley N.º 29733, Ley de Protección de Datos Personales.

## 4. Objetivos

**Objetivo general:** estimar las remociones potenciales anuales de CO₂ en la biomasa viva de las plantaciones forestales inscritas en el Registro Nacional de Plantaciones Forestales del Perú (2014-2025), por grupo de especies, departamento y finalidad, con el método de ganancias de nivel 1 del IPCC y su incertidumbre asociada.

**Objetivos específicos:**
1. Cuantificar la superficie inscrita por grupo de especies, departamento y finalidad a partir de la base curada, sin conteos repetidos.
2. Asignar a cada plantación una zona ecológica del IPCC y los factores por defecto de crecimiento de biomasa (G_W), relación raíz/tallo (R) y fracción de carbono (CF).
3. Estimar las remociones potenciales anuales de CO₂ y su intervalo de confianza del 95 % mediante simulación de Monte Carlo.
4. Comparar las remociones potenciales de las plantaciones de producción con las de protección y restauración.
5. Evaluar la sensibilidad de la estimación a escenarios de supervivencia del 50 %, 75 % y 100 %.

## 5. Hipótesis

Es un estudio **descriptivo-estimativo**, por lo que las hipótesis son de trabajo y se pueden contrastar con los datos:

- **H1 (concentración):** más del 50 % de las remociones potenciales proviene de menos del 10 % de las plantaciones. *El análisis exploratorio muestra que el 10 % de plantaciones más grandes reúne el 73,8 % de la superficie.*
- **H2 (permanencia):** menos del 5 % de las remociones potenciales corresponde a plantaciones con finalidad exclusiva de protección o restauración.
- **H3 (composición):** la remoción potencial por hectárea difiere entre departamentos amazónicos y andinos por la diferente composición de grupos de especies y zonas ecológicas.

## 6. Antecedentes y marco teórico

### 6.1 Antecedentes

> Antecedentes verificados el 17/11/2026: se abrió cada registro en su repositorio o revista y se confirmaron autores, año, cifras y DOI o *handle*. Las cifras provienen de los resúmenes publicados.

**Nacionales: carbono en plantaciones de bolaina blanca (*Guazuma crinita*), la especie más frecuente del registro (4598 plantaciones)**
- **Neira Valerio (2009)** cuantificó la biomasa y el carbono de plantaciones de *G. crinita* y de su asociación con cacao en Río Negro (Satipo, Junín), con 41 parcelas de 100 m². Las plantaciones puras almacenaron **23,2 t C/ha**, sumando árboles, arbustos, herbáceas, hojarasca y raicillas, y la asociación con cacao **11,5 t C/ha**.
- **Baltazar Peña (2011)** estimó **9,49 t C/ha** de carbono aéreo en una plantación de bolaina blanca de un año en Nuevo Edén (Manu, Madre de Dios), a partir de una biomasa aérea de 21,09 t/ha.
- **Revilla-Chávez et al. (2021)** ajustaron un modelo alométrico de biomasa aérea con 38 árboles de *G. crinita* de 31 meses en plantaciones de la cuenca del Aguaytía (Ucayali): B = 0,04253 × dab^2,5027 (R² = 0,94).
- **Rengifo Trigozo et al. (2021)** midieron tres plantaciones mixtas de 1,5 años en Mariano Dámaso Beraún (Huánuco), con *Schizolobium amazonicum*, *Swietenia macrophylla*, *Inga edulis*, *Juglans neotropica* y *Licaria triandra*. El carbono aéreo fue de solo **0,82 a 1,17 t C/ha**, frente a **67 a 90 t C/ha** de carbono orgánico en el suelo.

Estos estudios miden **reservas** en sitios puntuales y a edades distintas. Muestran además que el carbono aéreo de las plantaciones jóvenes es bajo (de 1 a 23 t C/ha), lo que respalda presentar nuestro resultado como un **potencial** y no como una reserva actual. Ninguno estima el potencial **a escala del registro nacional**, que es el vacío que aborda esta investigación. Huánuco, donde se hizo el último estudio, es además el departamento con más superficie inscrita (17,7 %).

**Metodológicos internacionales**
- IPCC (2006, 2019): método de ganancias y pérdidas y factores por defecto para tierras forestales.
- Requena Suarez et al. (2019): refinan las tasas por defecto del IPCC de crecimiento de biomasa en bosques tropicales y subtropicales con datos de parcelas.
- Wilkinson et al. (2016): principios FAIR para la gestión de datos científicos.

### 6.2 Marco teórico

1. **Remoción y reserva.** Una remoción es un flujo de CO₂ desde la atmósfera hacia un depósito (t CO₂/año). Una reserva es la cantidad almacenada en un momento dado (t C). Este estudio estima **remociones potenciales**, no reservas ni secuestro medido.
2. **Método de ganancias del IPCC (nivel 1).** La ganancia anual de carbono en biomasa es ΔC_G = Σ Aᵢ × G_Wᵢ × (1 + Rᵢ) × CF. Para pasar a CO₂ se multiplica por 44/12.
3. **Niveles (*tiers*) del IPCC.** El nivel 1 usa factores por defecto; el nivel 2, factores nacionales; el nivel 3, mediciones y modelos. La información disponible solo permite el nivel 1.
4. **Permanencia.** El carbono de plantaciones que se cosechan vuelve a la atmósfera, en todo o en parte, en el corto o mediano plazo. Los estándares de certificación exigen gestionar ese riesgo (*buffer*).
5. **Curaduría y FAIR.** Convertir datos administrativos en evidencia científica requiere preservar el original, documentar las transformaciones y hacer el proceso reproducible.

## 7. Variables e indicadores

| Variable | Tipo | Indicador | Unidad | Fuente |
|---|---|---|---|---|
| Superficie de plantación | Independiente | Superficie inscrita por plantación (contada una vez) | ha | Base curada (`superficie_ha`) |
| Grupo de especies | Independiente (categórica) | *Eucalyptus*, *Pinus*, *Tectona*, otras latifoliadas, otras coníferas, bambúes, mixta | — | Base curada + GBIF |
| Zona ecológica | Independiente (categórica) | Zona ecológica global de la FAO en el centroide del distrito | — | FAO GEZ + límites distritales INEI |
| Finalidad | Independiente (categórica) | Producción, protección, restauración o combinaciones | — | Base curada |
| Departamento | Independiente (categórica) | Departamento según UBIGEO | — | Base curada |
| Supervivencia | Interviniente (escenario) | Fracción de superficie en pie | 0,50 / 0,75 / 1,00 | Supuesto |
| Crecimiento de biomasa aérea | Parámetro | G_W por grupo y zona ecológica | t ms/ha/año | IPCC 2019, Tabla 4.10 |
| Relación raíz/tallo | Parámetro | R | adimensional | IPCC 2019, Tabla 4.4 |
| Fracción de carbono | Parámetro | CF | t C/t ms | IPCC 2006, Tabla 4.3 (0,47) |
| **Remoción potencial** | **Dependiente** | ΔCO₂ total, por hectárea y por grupo | t CO₂/año; t CO₂/ha/año | Calculada |

## 8. Matriz de operacionalización

| Variable | Definición conceptual | Definición operacional | Dimensiones | Indicadores | Escala |
|---|---|---|---|---|---|
| Remoción potencial de CO₂ | Flujo anual de CO₂ que la biomasa viva de una plantación podría incorporar según factores por defecto | ΔCO₂ = A × S × G_W × (1 + R) × CF × 44/12 | Total; por hectárea; por grupo; por departamento; por finalidad | t CO₂/año; t CO₂/ha/año; % del total | Razón |
| Superficie efectiva | Superficie inscrita que se supone plantada y en pie | A × S (S = supervivencia) | Inscrita; efectiva por escenario | ha | Razón |
| Composición de especies | Grupo de especies de la plantación según la clasificación del IPCC | Grupo del nombre aceptado (GBIF); "mixta" si hay más de un grupo | 7 grupos | n.º de plantaciones; ha; % | Nominal |
| Permanencia potencial | Probabilidad relativa de que el carbono se mantenga a largo plazo | Finalidad inscrita: protección o restauración (mayor) frente a producción (menor) | Mayor; menor; mixta | % de remociones | Ordinal |
| Contexto ecológico | Condiciones de crecimiento asociadas a la ubicación | Zona ecológica de la FAO en el centroide del distrito | Bosque tropical lluvioso, húmedo, seco, sistemas montañosos… | Categoría | Nominal |

## 9. Diseño metodológico

- **Enfoque:** cuantitativo.
- **Tipo:** aplicado, descriptivo-estimativo.
- **Diseño:** no experimental, transversal (un corte del registro) y basado en datos secundarios.
- **Población:** las 16 204 plantaciones inscritas en el Registro Nacional de Plantaciones Forestales al 11/06/2025.
- **Muestra:** censal. Se excluyen las 9 plantaciones con superficie de 0 ha.
- **Unidad de análisis:** la plantación.
- **Fuentes:**
  1. Base curada del SERFOR (este repositorio).
  2. Límites distritales del INEI.
  3. Mapa de Zonas Ecológicas Globales de la FAO (actualización 2010).
  4. IPCC 2006 y 2019, Vol. 4.

## 10. Procedimientos de procesamiento y análisis

1. **Datos de partida:** `plantaciones_curada.csv`, ya curado (scripts 01 a 03).
2. **Grupo de especies:** clasificación por género y familia (script 04, ya implementado).
3. **Zona ecológica:** unir el UBIGEO con los límites distritales del INEI, calcular el centroide de cada distrito y superponerlo al mapa de zonas ecológicas de la FAO (`geopandas`). Los distritos que cruzan más de una zona se asignan a la de mayor área y se marcan.
4. **Factores:** extraer de la Tabla 4.10 del IPCC 2019 los valores de G_W, con su rango, para Sudamérica por grupo y zona. Extraer R (Tabla 4.4) y CF (Tabla 4.3). Guardarlos en `data/factores_ipcc.csv` con página y tabla de origen.
5. **Plantaciones mixtas:** se usa el promedio de los factores de los grupos presentes. Como análisis de sensibilidad, se aplica el mínimo y el máximo.
6. **Cálculo:** ΔCO₂ por plantación y agregación por grupo, departamento y finalidad.
7. **Incertidumbre:** simulación de Monte Carlo con 10 000 iteraciones. Los factores se muestrean dentro de sus rangos del IPCC y se reportan la mediana y el intervalo del 2,5 % al 97,5 %.
8. **Escenarios de supervivencia** del 50 %, 75 % y 100 %.
9. **Contraste de hipótesis:**
   - H1 con la curva de concentración (Lorenz) y el índice de Gini;
   - H2 con la proporción de ΔCO₂ por finalidad;
   - H3 con la prueba de Kruskal-Wallis sobre ΔCO₂/ha entre regiones (amazónica y andina), con tamaño del efecto.
10. **Herramientas:** Python 3.13 (pandas, geopandas, numpy, scipy, matplotlib). Cada paso se versiona en GitHub.

## 11. Calidad, incertidumbre y reproducibilidad

- **Calidad:** se aplican la curaduría documentada (12 reglas), las banderas de calidad y la exclusión justificada de las superficies de 0 ha. Se hace un análisis de sensibilidad excluyendo las 22 plantaciones de más de 500 ha y las 83 de menos de 0,01 ha.
- **Conservadurismo:** el resultado se presenta como **límite superior del potencial**, nunca como secuestro real. Para la cifra central se usa el valor bajo de los rangos del IPCC.
- **Incertidumbre:** se propagan los rangos de los factores (Monte Carlo) y la de la superficie efectiva (escenarios de supervivencia). Se documentan las fuentes de incertidumbre que no se pueden cuantificar: edad, asignación de zona ecológica y especies mixtas.
- **Reproducibilidad:** el repositorio público tiene los scripts numerados, `requirements.txt`, la huella SHA-256 del original, la caché taxonómica, el registro de cambios y el registro de decisiones. Cualquier persona puede reproducir los resultados siguiendo el README.

## 12. Resultados esperados y limitaciones

### Resultados esperados
1. Una tabla de superficie y de remoción potencial de CO₂, con su intervalo de confianza del 95 %, por grupo de especies, departamento y finalidad.
2. La cuantificación de la sobreestimación que produce usar el registro sin curar (factor de 2,64 en la superficie).
3. La proporción del potencial con permanencia de largo plazo, que se espera menor al 5 %.
4. Un conjunto de recomendaciones al SERFOR para que el registro sirva al monitoreo de carbono.
5. Un repositorio GitHub reproducible y una base curada que cumple los principios FAIR (30/30 en la evaluación de este trabajo), exportada también en Darwin Core y archivada en Zenodo con DOI 10.5281/zenodo.24328237.

### Limitaciones
- Solo se estima el **potencial**: la base no permite medir secuestro real ni tasas de secuestro.
- La inscripción no garantiza que la plantación exista ni que siga en pie, porque no hay datos de supervivencia.
- El año de inscripción no es el año de plantación, así que no se conoce la edad.
- La zona ecológica es aproximada, porque se asigna por distrito y no por coordenadas.
- Las plantaciones mixtas no tienen proporción de especies.
- Los factores del IPCC de nivel 1 son genéricos; los factores nacionales (nivel 2) mejorarían la estimación.
- No se consideran las emisiones por cosecha, la línea base ni las fugas. Por eso **no** es una estimación de créditos de carbono.

## 13. Referencias

- Baltazar Peña, A. L. (2011). *Carbono aéreo almacenado en una plantación de bolaina blanca (Guazuma crinita Martius) de un año de edad, en el centro poblado Nuevo Edén, Alto Madre de Dios* [Tesis de pregrado, Universidad Nacional Agraria de la Selva]. https://hdl.handle.net/20.500.14292/563
- Food and Agriculture Organization of the United Nations. (2012). *Global ecological zones for FAO forest reporting: 2010 update* (Forest Resources Assessment Working Paper 179). FAO.
- Gold Standard Foundation. (2024). *Afforestation/Reforestation GHG Emissions Reduction & Sequestration Methodology* (versión 2.1).
- Greenhouse Gas Protocol. (2004). *A Corporate Accounting and Reporting Standard* (ed. revisada). WRI y WBCSD.
- Greenhouse Gas Protocol. (2026). *Land Sector and Removals Standard* (versión 1.1). WRI y WBCSD. https://ghgprotocol.org/land-sector-and-removals-standard
- IPCC. (2006). *2006 IPCC Guidelines for National Greenhouse Gas Inventories. Volume 4: Agriculture, Forestry and Other Land Use*. IGES.
- IPCC. (2019). *2019 Refinement to the 2006 IPCC Guidelines for National Greenhouse Gas Inventories. Volume 4, Chapter 4: Forest Land*. IPCC.
- Ley N.º 29733, Ley de Protección de Datos Personales. (2011). Congreso de la República del Perú.
- Ley N.º 29763, Ley Forestal y de Fauna Silvestre. (2011). Congreso de la República del Perú.
- Ministerio de Agricultura y Riego. (2015). *Decreto Supremo N.º 020-2015-MINAGRI, Reglamento para la Gestión de las Plantaciones Forestales y los Sistemas Agroforestales* (publicado el 30 de septiembre de 2015). https://sinia.minam.gob.pe/normas/decreto-supremo-que-aprueba-reglamento-gestion-las-plantaciones
- Neira Valerio, Y. (2009). *Cuantificación de biomasa y carbono en plantaciones de Guazuma crinita Mart. y asociación de Guazuma crinita Mart. con Theobroma cacao L. – Satipo* [Tesis de pregrado, Universidad Nacional del Centro del Perú]. http://hdl.handle.net/20.500.12894/3973
- Rengifo Trigozo, J. P., Oré Cierto, L. E., Loarte Aliaga, W. C., & Oré Cierto, J. D. (2021). Carbono almacenado en plantaciones forestales en el distrito de Mariano Dámaso Beraún, Huánuco - Perú. *Yotantsipanko, 1*(2), 32-43. https://doi.org/10.54288/yotantsipanko.v1i2.6
- Requena Suarez, D., Rozendaal, D. M. A., De Sy, V., Phillips, O. L., Alvarez-Dávila, E., Anderson-Teixeira, K., … Herold, M. (2019). Estimating aboveground net biomass change for tropical and subtropical forests: Refinement of IPCC default rates using forest plot data. *Global Change Biology, 25*(11), 3609-3624. https://doi.org/10.1111/gcb.14767
- Revilla-Chávez, J. M., López-Galán, E. E., Guerra-Arévalo, W. F., García-Soria, D. G., Rojas-Mego, K. C., Domínguez-Torrejón, G., & Abanto-Rodríguez, C. (2021). Modelos alométricos de biomasa de árboles de *Guazuma crinita* Mart en plantaciones forestales de Ucayali, Perú. *Scientia Agropecuaria, 12*(4), 579-587. https://doi.org/10.17268/sci.agropecu.2021.062
- Servicio Nacional Forestal y de Fauna Silvestre. (2025). *Plantaciones forestales inscritas en el Registro Nacional de Plantaciones Forestales, por especie* [Conjunto de datos, corte 11/06/2025]. Plataforma Nacional de Datos Abiertos. https://www.datosabiertos.gob.pe/dataset/plantaciones-forestales-inscritas-en-el-registro-nacional-de-plantaciones-forestales-por
- Verra. (2025). *VCS Standard* (versión 5.0).
- Verra. (2025). *VM0047 Afforestation, Reforestation, and Revegetation* (versión 1.1).
- Wilkinson, M. D., Dumontier, M., Aalbersberg, I. J., … Mons, B. (2016). The FAIR Guiding Principles for scientific data management and stewardship. *Scientific Data, 3*, 160018. https://doi.org/10.1038/sdata.2016.18
