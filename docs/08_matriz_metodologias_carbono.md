# Entregable 8. Matriz comparativa de metodologías de carbono y diagnóstico de factibilidad

> **Aviso de verificación.** Las versiones y fechas de los documentos se comprobaron en las páginas oficiales de cada organización el 17/11/2026. El contenido técnico detallado (fórmulas, plazos, porcentajes) debe confirmarse en los PDF oficiales antes de citarlo en el proyecto. Los enlaces están en la sección 5.
>
> **Correcciones tras la segunda verificación (17/11/2026):** (1) el LSR Standard del GHG Protocol tiene ahora una **v1.1**, que es la versión de referencia; (2) Verra **aplazó al 1/7/2027** la entrada en vigor de la VCS v5.0. Se confirmaron sin cambios: Gold Standard P&R v2.1 (31/01/2025), la metodología A/R 403 v2.1, VCS Standard v5.0 (16/12/2025) y VM0047 v1.1 (vigente desde el 14/05/2025). Gold Standard indica en la página de la metodología 403 que actualizará sus metodologías para alinearlas con el mecanismo de créditos del Acuerdo de París (PACM).

## 1. Conceptos que no deben confundirse

| Concepto | Definición operativa | Unidad típica | ¿Se puede obtener con nuestra base? |
|---|---|---|---|
| **Biomasa aérea** | Materia seca de fuste, ramas y hojas por encima del suelo | t ms/ha | ❌ No hay diámetros ni alturas |
| **Biomasa subterránea** | Materia seca de las raíces. Suele estimarse como biomasa aérea × relación raíz/tallo (R) | t ms/ha | ❌ Solo con factores por defecto |
| **Reserva (existencia) de carbono** | Carbono almacenado **en un momento dado** en un depósito: biomasa, madera muerta, hojarasca o suelo | t C/ha o t C | ❌ No hay mediciones |
| **Carbono orgánico del suelo (COS)** | Carbono en la materia orgánica del suelo hasta una profundidad definida (por ejemplo, 30 cm) | t C/ha | ❌ |
| **Cambio de existencias** | Diferencia entre dos inventarios: ΔC = (C₂ − C₁) / (t₂ − t₁) | t C/año | ❌ Hay un solo corte |
| **Emisión** | Flujo de GEI hacia la atmósfera, por ejemplo por cosecha, quema o deforestación | t CO₂e/año | ❌ No hay datos de cosecha ni de pérdida |
| **Remoción** | Flujo de CO₂ desde la atmósfera hacia un depósito, por ejemplo por el crecimiento de árboles | t CO₂e/año | ⚠️ **Solo potencial**, con superficie × factores por defecto |
| **Tasa de secuestro** | Remoción neta por unidad de superficie y tiempo, **medida** | t CO₂e/ha/año | ❌ Requiere mediciones repetidas |

**Conversión de carbono a CO₂:** t CO₂ = t C × 44/12.

## 2. Matriz comparativa

| Criterio | GHG Protocol | Gold Standard (GS4GG) | Verra (VCS) |
|---|---|---|---|
| **Tipo de referente** | Normas de **contabilidad** de GEI para empresas y organizaciones. No emite créditos | Programa de **certificación** de proyectos y emisión de créditos con co-beneficios para los ODS | Programa de **certificación** de proyectos y emisión de créditos (VCU) |
| **Documentos aplicables** | *Corporate Accounting and Reporting Standard* (ed. revisada, 2004); *GHG Protocol for Project Accounting* (2005); *LULUCF Guidance for GHG Project Accounting* (2006); **Land Sector and Removals (LSR) Standard**: v1.0 publicada el 30/01/2026 y reemplazada por la **v1.1** (junio de 2026, cambios menores, junto con la *LSR Guidance*); vigente desde el 1/1/2027 | *Principles & Requirements* v2.1 (31/01/2025; la v2.0 rige desde el 5/12/2024); *Land Use & Forests Activity Requirements*; metodología **403 A/R GHG Emissions Reduction & Sequestration** v2.1 (16/05/2024) | *VCS Standard* v4.5 y **v5.0** (16/12/2025; el 27/10/2026 Verra aplazó la entrada en vigor de la mayoría de cambios del 1/1/2027 al **1/7/2027**); *VCS Program Guide* v5.0; metodología **VM0047 ARR** v1.1 (14/05/2025); *AFOLU Non-Permanence Risk Tool* |
| **Unidad de análisis** | Inventario de la organización o de su cadena de valor (alcances 1, 2 y 3) | Proyecto con área delimitada | Proyecto con área delimitada |
| **Actividad pertinente a plantaciones** | Remociones en tierras propias o de la cadena de valor (LSR Standard) | Forestación y reforestación (A/R) | Forestación, reforestación y revegetación (ARR) |
| **Límites del sistema** | Límites organizacionales y operativos; depósitos de carbono del sector tierra | Área del proyecto georreferenciada y depósitos seleccionados (el COS se excluye de los créditos planificados en la v2.1) | Área del proyecto georreferenciada, depósitos y fuentes de GEI definidos en VM0047 |
| **Línea base** | No exige línea base en el inventario; sí en la contabilidad de proyectos (2005) | Obligatoria: qué pasaría sin el proyecto | Obligatoria: VM0047 usa un enfoque de desempeño con áreas de control o un enfoque censal |
| **Adicionalidad** | No aplica al inventario | Obligatoria | Obligatoria |
| **Permanencia** | El LSR Standard exige monitoreo continuo para declarar remociones | Gestión del riesgo de reversión con reserva (*buffer*) | Evaluación del riesgo de no permanencia y aporte al *buffer pool* |
| **Fugas** | No aplica al inventario | Deben estimarse | Deben estimarse |
| **Monitoreo, reporte y verificación** | Reporte anual del inventario; la verificación es opcional según el programa | Monitoreo periódico y verificación por un organismo acreditado (VVB) | Monitoreo periódico y verificación por un VVB |
| **Incertidumbre** | Debe evaluarse y reportarse | Debe cuantificarse; se aplican descuentos por incertidumbre | Debe cuantificarse según la metodología |
| **Requisitos adicionales** | Trazabilidad física en la cadena de valor (LSR Standard) | Contribución demostrada a ODS además del ODS 13; salvaguardas y consulta a actores | Salvaguardas sociales y ambientales; consulta a actores |
| **Datos mínimos que exige** | Superficie, factores de crecimiento o mediciones, trazabilidad | Polígonos del proyecto, parcelas de inventario, línea base y monitoreo | Polígonos del proyecto, datos satelitales o parcelas, línea base dinámica y monitoreo |

## 3. Aplicabilidad a nuestra base (SERFOR, plantaciones inscritas)

| Requisito | GHG Protocol | Gold Standard | Verra | ¿Lo cumple nuestra base? |
|---|---|---|---|---|
| Superficie de plantación | Sí | Sí | Sí | ✅ Sí, en ha y por plantación |
| Especie | Sí | Sí | Sí | ✅ Sí, estandarizada con GBIF |
| Ubicación precisa (polígonos o coordenadas) | Recomendado | **Obligatorio** | **Obligatorio** | ❌ Solo distrito |
| Fecha de plantación o edad | Necesario | Necesario | Necesario | ❌ Solo año de inscripción |
| Supervivencia o estado actual | Necesario | Necesario | Necesario | ❌ |
| Mediciones dasométricas (DAP, altura) | Opcional (nivel 1 con factores) | Necesario | Necesario | ❌ |
| Línea base | — | **Obligatorio** | **Obligatorio** | ❌ |
| Adicionalidad | — | **Obligatorio** | **Obligatorio** | ❌ No evaluable |
| Permanencia y riesgo | Monitoreo | **Obligatorio** | **Obligatorio** | ❌ La finalidad "producción" implica cosecha |
| Monitoreo y verificación | Reporte | **Obligatorio** | **Obligatorio** | ❌ |

## 4. Diagnóstico de factibilidad

**Conclusión:** con esta base **no es posible** cuantificar créditos de carbono ni aplicar íntegramente ningún estándar de certificación. Tampoco se puede medir una tasa de secuestro real. **Sí es posible** hacer una **estimación de nivel 1 (Tier 1) de las remociones potenciales** de la superficie inscrita, con el método de ganancias del IPCC.

**Método aplicable** (IPCC 2006, Vol. 4, Cap. 2 y 4; Refinamiento 2019, Cap. 4):

ΔC_G = Σᵢ [ Aᵢ × G_Wᵢ × (1 + Rᵢ) × CF ] × 44/12

| Símbolo | Significado | Origen |
|---|---|---|
| Aᵢ | Superficie de las plantaciones del grupo de especies *i* (ha) | **Nuestra base**: `plantaciones_curada.csv` |
| G_Wᵢ | Crecimiento neto de biomasa aérea (t ms/ha/año) | IPCC 2019, **Tabla 4.10** (plantaciones tropicales y subtropicales, por grupo de especies, continente y zona ecológica) |
| Rᵢ | Relación biomasa subterránea / aérea | IPCC 2019, Tabla 4.4 |
| CF | Fracción de carbono de la biomasa seca (por defecto 0,47) | IPCC 2006, Tabla 4.3 |

**Qué conceptos de los estándares sí podemos usar en la investigación:**
1. **Límites del sistema** (los tres): declarar que solo se considera la biomasa viva (aérea y subterránea) y se excluyen la madera muerta, la hojarasca y el COS.
2. **Conservadurismo** (Gold Standard y Verra): elegir el valor bajo del rango cuando el factor es incierto.
3. **Incertidumbre** (los tres): propagar el rango de los factores por defecto del IPCC.
4. **Permanencia** (los tres, como concepto): separar las plantaciones de **producción**, que serán cosechadas, de las de **protección y restauración**. Solo estas últimas se aproximan a un almacenamiento de largo plazo.

**Qué no podemos implementar y por qué:**
- Línea base y adicionalidad: no se sabe qué uso tenía el suelo antes de la plantación.
- Monitoreo y verificación: hay un solo corte y no hay mediciones de campo.
- Asignar la superficie a cada especie en plantaciones mixtas: la fuente no da la proporción.
- Elegir la zona ecológica exacta del IPCC: solo tenemos el distrito, no coordenadas.

## 5. Referencias

- Greenhouse Gas Protocol. (2004). *A Corporate Accounting and Reporting Standard* (ed. revisada). World Resources Institute y World Business Council for Sustainable Development. https://ghgprotocol.org/corporate-standard
- Greenhouse Gas Protocol. (2026). *Land Sector and Removals Standard* (versión 1.1). World Resources Institute y World Business Council for Sustainable Development. https://ghgprotocol.org/land-sector-and-removals-standard
- Gold Standard Foundation. (2025). *Gold Standard for the Global Goals: Principles & Requirements*, versión 2.1. https://globalgoals.goldstandard.org/101-par-principles-requirements/
- Gold Standard Foundation. (2024). *Afforestation/Reforestation GHG Emissions Reduction & Sequestration Methodology*, versión 2.1. https://globalgoals.goldstandard.org/standards/403_V2.1_LUF_AR-Methodology-GHGs-emission-reduction-and-Sequestration-Methodology.pdf
- Verra. (2025). *VCS Standard*, versión 5.0. https://verra.org/documents/vcs-standard-v5-0/
- Verra. (2025). *VCS Program Guide*, versión 5.0. https://verra.org/documents/vcs-program-guide-v5-0/
- Verra. (2025). *VM0047 Afforestation, Reforestation, and Revegetation*, versión 1.1. https://verra.org/methodologies/vm0047-afforestation-reforestation-and-revegetation-v1-1/
- Verra. (2026). *VCS governance and development* [Página web; cambio de la fecha de entrada en vigor de la versión 5, 27/10/2026]. https://verra.org/programs/verified-carbon-standard/governance-development/
- IPCC. (2006). *2006 IPCC Guidelines for National Greenhouse Gas Inventories*, Volumen 4: Agricultura, silvicultura y otros usos de la tierra. IGES.
- IPCC. (2019). *2019 Refinement to the 2006 IPCC Guidelines for National Greenhouse Gas Inventories*, Volumen 4, Capítulo 4: Tierras forestales. https://www.ipcc-nggip.iges.or.jp/public/2019rf/pdf/4_Volume4/19R_V4_Ch04_Forest%20Land.pdf
