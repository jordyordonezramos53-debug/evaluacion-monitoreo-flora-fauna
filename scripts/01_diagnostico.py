"""Paso 3a. Diagnóstico inicial de calidad del archivo original (sin modificarlo).

Salida: data/processed/diagnostico_inicial.csv (indicador, valor, comentario)
No imprime ni guarda datos personales (nombres ni números de documento).
"""
import csv
from collections import Counter

import pandas as pd

from comun import PROCESSED, RAW, leer_original, salida_utf8

salida_utf8()
df = leer_original()
area = pd.to_numeric(df["SUPERFICIE PLANTACION"], errors="coerce")
por_id = df.assign(_a=area).drop_duplicates("ID PLANTACION")
q1, q3 = por_id["_a"].quantile([0.25, 0.75])
limite_atipico = q3 + 3 * (q3 - q1)

especies = df["ESPECIE"].dropna()
unicas = pd.Series(especies.unique())
n_esp = df.groupby("ID PLANTACION")["ESPECIE"].count()
ub_inconsistente = (df.groupby("UBIGEO")[["DEPARTAMENTO", "PROVINCIA", "DISTRITO"]]
                    .nunique() > 1).any(axis=1).sum()
dep_vs_ubigeo = (df.groupby(df["UBIGEO"].str[:2])["DEPARTAMENTO"].nunique() > 1).sum()
dup_id_esp = df.duplicated(["ID PLANTACION", "ESPECIE"]).sum()
dni = df.loc[df["TIPO DOCUMENTO"] == "DNI", "NUMERO DOCUMENTO"].str.len()
ruc = df.loc[df["TIPO DOCUMENTO"] == "RUC", "NUMERO DOCUMENTO"].str.len()

# Versión anterior en CSV: ¿cuántas filas se desalinean por comas sin comillas?
csv_2022 = RAW / "DataSetPlantaciones_0.csv"
conteo_campos = Counter()
if csv_2022.exists():
    with open(csv_2022, encoding="utf-8", errors="replace", newline="") as f:
        filas = list(csv.reader(f))
    esperado = len(filas[0])
    conteo_campos = Counter(len(r) for r in filas[1:])
    filas_rotas = sum(v for k, v in conteo_campos.items() if k != esperado)
else:
    filas_rotas = None

ind = [
    ("filas (plantación × especie)", len(df), "Cada fila es una inscripción por especie"),
    ("columnas", df.shape[1], ""),
    ("plantaciones únicas (ID)", df["ID PLANTACION"].nunique(), ""),
    ("plantaciones con más de una especie", int((n_esp > 1).sum()), ""),
    ("plantaciones con superficie distinta entre sus filas", int((df.assign(_a=area).groupby("ID PLANTACION")["_a"].nunique() > 1).sum()),
     "0 = la superficie se repite idéntica en cada fila de especie"),
    ("superficie sumando todas las filas (ha)", round(area.sum(), 2), "INCORRECTO: cuenta varias veces la misma plantación"),
    ("superficie contando cada plantación una vez (ha)", round(por_id["_a"].sum(), 2), "Valor correcto"),
    ("factor de sobreestimación", round(area.sum() / por_id["_a"].sum(), 2), ""),
    ("periodo mínimo", df["PERIODO"].min(), ""),
    ("periodo máximo", df["PERIODO"].max(), ""),
    ("fecha de corte", ", ".join(df["FECHA CORTE"].unique()), ""),
    ("filas sin especie", int(df["ESPECIE"].isna().sum()), ""),
    ("filas sin titular", int(df["TITULAR"].isna().sum()), ""),
    ("filas repetidas exactas", int(df.duplicated().sum()), ""),
    ("filas con mismo ID y especie", int(dup_id_esp), "Difieren en finalidad o tipo de plantación: no son duplicados"),
    ("plantaciones con más de una finalidad", int((df.groupby("ID PLANTACION")["FINALIDAD"].nunique() > 1).sum()), ""),
    ("superficie = 0 ha", int((area == 0).sum()), "Error verificable: una plantación inscrita no puede medir 0 ha"),
    ("superficie no numérica", int(area.isna().sum()), ""),
    ("límite de atípico por plantación (Q3 + 3·IQR, ha)", round(limite_atipico, 2), ""),
    ("plantaciones atípicas (> límite)", int((por_id["_a"] > limite_atipico).sum()), "Se marcan, no se eliminan"),
    ("plantaciones > 500 ha", int((por_id["_a"] > 500).sum()), ""),
    ("superficie máxima (ha)", por_id["_a"].max(), ""),
    ("UBIGEO con longitud distinta de 6", int((df["UBIGEO"].str.len() != 6).sum()), ""),
    ("UBIGEO con más de un nombre de lugar", int(ub_inconsistente), ""),
    ("prefijo de UBIGEO con más de un departamento", int(dep_vs_ubigeo), ""),
    ("DNI con longitud distinta de 8", int((dni != 8).sum()), ""),
    ("RUC con longitud distinta de 11", int((ruc != 11).sum()), ""),
    ("nombres de especie distintos (texto)", len(unicas), ""),
    ("nombres con más de dos palabras (autor o categoría infraespecífica)",
     int(((unicas.str.split().str.len() > 2) & ~unicas.str.contains(r"\bspp?\.?$", regex=True)).sum()),
     "El mismo taxón aparece con y sin autor, p. ej. 'Guadua angustifolia' y 'Guadua angustifolia Kunth'"),
    ("nombres identificados solo a género (sp./spp.)", int(unicas.str.contains(r"\bspp?\.?$", regex=True).sum()), ""),
    ("nombres con espacios sobrantes", int(unicas.str.contains(r"^\s|\s$|\s\s", regex=True).sum()), ""),
    ("CSV 2022: filas desalineadas", filas_rotas, f"Distribución de campos por fila: {dict(sorted(conteo_campos.items()))}"),
]

PROCESSED.mkdir(parents=True, exist_ok=True)
salida = PROCESSED / "diagnostico_inicial.csv"
pd.DataFrame(ind, columns=["indicador", "valor", "comentario"]).to_csv(salida, index=False, encoding="utf-8")
for k, v, c in ind:
    print(f"- {k}: {v}" + (f"  ({c})" if c else ""))
print(f"\nGuardado en {salida.relative_to(PROCESSED.parents[1])}")
