"""Paso 3c. Curaduría: genera la base curada a partir del original sin tocarlo.

Entradas : data/raw/Plantaciones_208.xls (original)
           data/processed/tabla_taxonomica.csv (de 02_taxonomia_gbif.py)
Salidas  : data/processed/plantaciones_especies_curada.csv  (plantación × especie)
           data/processed/plantaciones_curada.csv           (una fila por plantación)
           data/processed/registro_cambios.csv              (qué se hizo, a cuántas filas y por qué)

Principio: los errores verificables se corrigen o se marcan; los valores
inusuales NO se eliminan, solo se marcan con una bandera (columnas flag_*).
"""
import pandas as pd

from comun import ARCHIVO_ORIGINAL, PROCESSED, RENOMBRAR, leer_original, salida_utf8, sha256

salida_utf8()
cambios = []


def registrar(regla, columna, n, tipo, descripcion, unidad="filas"):
    cambios.append({"regla": regla, "columna": columna, "n_afectados": int(n), "unidad": unidad,
                    "tipo": tipo, "descripcion": descripcion})


df = leer_original()
n0 = len(df)

# R01. Nombres de columnas normalizados
df = df.rename(columns=RENOMBRAR)
registrar("R01", "todas", n0, "transformación",
          "Renombrar columnas a snake_case sin tildes ni espacios (interoperabilidad).")

# R02. Espacios sobrantes en textos
cambiada = pd.Series(False, index=df.index)
for c in df.columns:  # todas las columnas se leyeron como texto
    limpio = df[c].str.split().str.join(" ")
    cambiada |= limpio.fillna("") != df[c].fillna("")
    df[c] = limpio
n_esp = cambiada.sum()
registrar("R02", "texto", n_esp, "corrección",
          "Quitar espacios al inicio, al final y dobles. No cambia el contenido.")

# R03. Seudonimización de titulares (datos personales)
clave = df["tipo_documento"].fillna("") + "|" + df["numero_documento"].fillna("")
orden = {k: f"TIT_{i:05d}" for i, k in enumerate(pd.unique(clave), 1)}
df["id_titular"] = clave.map(orden)
df = df.drop(columns=["titular", "numero_documento"])
registrar("R03", "titular, numero_documento", n0, "protección de datos",
          f"Se reemplazan nombre y número de documento por un código ({len(orden)} titulares). "
          "La correspondencia NO se guarda ni se publica.")

# R04. Tipos de dato
df["periodo"] = df["periodo"].astype(int)
df["fecha_corte"] = pd.to_datetime(df["fecha_corte"], format="%Y%m%d").dt.date.astype(str)
df["superficie_plantacion_ha"] = pd.to_numeric(df["superficie_plantacion_ha"])
registrar("R04", "periodo, fecha_corte, superficie_plantacion_ha", n0, "transformación",
          "Periodo a entero, fecha de corte a formato ISO 8601 (AAAA-MM-DD), superficie a número.")

# R05. Superficie igual a cero: error verificable, se marca (no se inventa un valor)
df["flag_superficie_cero"] = df["superficie_plantacion_ha"] == 0
registrar("R05", "superficie_plantacion_ha", df["flag_superficie_cero"].sum(), "marca",
          "Superficie = 0 ha. Se conserva el valor original, se marca y se excluye de las sumas.")

# R06. Superficies atípicas por plantación (Q3 + 3·IQR); se marcan, no se eliminan
por_id = df.drop_duplicates("id_plantacion").set_index("id_plantacion")["superficie_plantacion_ha"]
q1, q3 = por_id.quantile([0.25, 0.75])
limite = q3 + 3 * (q3 - q1)
df["flag_superficie_atipica"] = df["superficie_plantacion_ha"] > limite
df["flag_superficie_mayor_500ha"] = df["superficie_plantacion_ha"] > 500
registrar("R06", "superficie_plantacion_ha",
          df.drop_duplicates("id_plantacion")["flag_superficie_atipica"].sum(), "marca",
          f"Plantación con superficie > {limite:.2f} ha (Q3 + 3·IQR). Valor inusual, no error: se conserva.",
          unidad="plantaciones")

# R07. Estandarización taxonómica (GBIF Backbone)
tax = pd.read_csv(PROCESSED / "tabla_taxonomica.csv", dtype=str)
tax = tax[["nombre_registrado", "nombre_aceptado", "familia", "gbif_estado",
           "gbif_rango", "gbif_tipo_coincidencia", "decision"]].rename(columns={
               "decision": "decision_taxonomica", "gbif_estado": "estado_taxonomico_gbif",
               "gbif_rango": "rango_taxonomico", "gbif_tipo_coincidencia": "coincidencia_gbif"})
df = df.merge(tax, how="left", left_on="especie_original", right_on="nombre_registrado").drop(columns="nombre_registrado")
df["nivel_identificacion"] = "especie"
df.loc[df["rango_taxonomico"].isin(["GENUS", "FAMILY"]), "nivel_identificacion"] = "género o superior"
df.loc[df["especie_original"].isna(), "nivel_identificacion"] = "sin dato"
registrar("R07", "especie_original -> nombre_aceptado, familia", df["nombre_aceptado"].notna().sum(),
          "transformación",
          "Se agrega el nombre aceptado según GBIF sin borrar el nombre registrado. "
          f"Sinónimos actualizados: {(df['estado_taxonomico_gbif'] == 'SYNONYM').sum()} filas; "
          f"por revisar a mano: {(df['decision_taxonomica'] == 'REVISAR').sum()} filas.")

# R12. Revisión manual de los nombres que GBIF no resolvió (tabla documentada, una fila por nombre)
manual = pd.read_csv(PROCESSED / "revision_taxonomica_manual.csv", dtype=str).set_index("nombre_registrado")
en_manual = df["especie_original"].isin(manual.index) & (df["decision_taxonomica"] == "REVISAR")
m = manual.reindex(df.loc[en_manual, "especie_original"])
df.loc[en_manual, "nombre_aceptado"] = m["nombre_aceptado"].values
df.loc[en_manual, "familia"] = m["familia"].values
df.loc[en_manual, "rango_taxonomico"] = m["rango_revisado"].values
df.loc[en_manual, "decision_taxonomica"] = "REVISADO_MANUAL"
df.loc[en_manual & (df["rango_taxonomico"] == "SPECIES"), "nivel_identificacion"] = "especie"
df.loc[en_manual & (df["rango_taxonomico"] == "GENUS"), "nivel_identificacion"] = "género o superior"
df.loc[en_manual & (df["rango_taxonomico"] == "HYBRID"), "nivel_identificacion"] = "híbrido"
registrar("R12", "nombre_aceptado, familia, rango_taxonomico", en_manual.sum(), "corrección",
          f"Revisión manual de {len(manual)} nombres que GBIF no resolvió (identificados a género, "
          "homónimos resueltos por autor, errores de escritura y un híbrido). "
          "Decisiones y justificación en revision_taxonomica_manual.csv.")

# R08. Filas sin especie
df["flag_sin_especie"] = df["especie_original"].isna()
registrar("R08", "especie_original", df["flag_sin_especie"].sum(), "marca",
          "Fila sin especie. Se conserva porque su superficie sigue contando para la plantación.")

# R09. Mismo ID y especie en más de una fila (difieren en finalidad o tipo de plantación)
df["flag_id_especie_repetido"] = df.duplicated(["id_plantacion", "especie_original"], keep=False) & df["especie_original"].notna()
registrar("R09", "id_plantacion, especie_original", df["flag_id_especie_repetido"].sum(), "marca",
          "No son duplicados exactos: cambian la finalidad o el tipo de plantación. No se eliminan.")

# R10. Número de especies y advertencia de superficie repetida
n_especies = df.dropna(subset=["nombre_aceptado"]).groupby("id_plantacion")["nombre_aceptado"].nunique()
df["n_especies_plantacion"] = df["id_plantacion"].map(n_especies).fillna(0).astype(int)
registrar("R10", "superficie_plantacion_ha", (df["n_especies_plantacion"] > 1).sum(), "documentación",
          "La superficie es de la plantación completa y se repite en cada especie: NO sumar por filas.")

orden_cols = ["id_plantacion", "periodo", "fecha_corte", "departamento", "provincia", "distrito",
              "ubigeo", "arffs", "sede", "numero_certificado", "id_titular", "tipo_persona",
              "tipo_documento", "regimen_tenencia", "finalidad", "tipo_plantacion",
              "especie_original", "nombre_aceptado", "familia", "estado_taxonomico_gbif",
              "rango_taxonomico", "coincidencia_gbif", "decision_taxonomica", "nivel_identificacion",
              "superficie_plantacion_ha", "n_especies_plantacion",
              "flag_superficie_cero", "flag_superficie_atipica", "flag_superficie_mayor_500ha",
              "flag_sin_especie", "flag_id_especie_repetido"]
df = df[orden_cols].copy()
df["id_plantacion"] = df["id_plantacion"].astype(int)
df = df.sort_values(["id_plantacion", "especie_original"], na_position="last")

# Tabla por plantación (unidad correcta para sumar superficie)
unir = lambda s: "|".join(sorted(set(s.dropna())))  # noqa: E731
plant = df.groupby("id_plantacion").agg(
    periodo=("periodo", "first"), fecha_corte=("fecha_corte", "first"),
    departamento=("departamento", "first"), provincia=("provincia", "first"),
    distrito=("distrito", "first"), ubigeo=("ubigeo", "first"), arffs=("arffs", "first"),
    numero_certificado=("numero_certificado", "first"), id_titular=("id_titular", "first"),
    tipo_persona=("tipo_persona", "first"), regimen_tenencia=("regimen_tenencia", "first"),
    finalidades=("finalidad", unir), tipos_plantacion=("tipo_plantacion", unir),
    especies_aceptadas=("nombre_aceptado", unir), n_especies=("n_especies_plantacion", "first"),
    superficie_ha=("superficie_plantacion_ha", "first"),
    flag_superficie_cero=("flag_superficie_cero", "first"),
    flag_superficie_atipica=("flag_superficie_atipica", "first"),
    flag_superficie_mayor_500ha=("flag_superficie_mayor_500ha", "first"),
).reset_index()
plant["flag_varias_finalidades"] = plant["finalidades"].str.contains(r"\|")
registrar("R11", "finalidad", plant["flag_varias_finalidades"].sum(), "marca",
          "Plantaciones con más de una finalidad inscrita (se listan todas, separadas por '|').",
          unidad="plantaciones")

df.to_csv(PROCESSED / "plantaciones_especies_curada.csv", index=False, encoding="utf-8")
plant.to_csv(PROCESSED / "plantaciones_curada.csv", index=False, encoding="utf-8")
reg = pd.DataFrame(cambios)
reg.insert(0, "archivo_origen", f"{ARCHIVO_ORIGINAL.name} (SHA-256 {sha256(ARCHIVO_ORIGINAL)[:12]}…)")
reg.to_csv(PROCESSED / "registro_cambios.csv", index=False, encoding="utf-8")

print(f"Filas originales: {n0} | filas curadas: {len(df)} (no se eliminó ninguna fila)")
print(f"Plantaciones: {len(plant)} | superficie válida total: "
      f"{plant.loc[~plant.flag_superficie_cero, 'superficie_ha'].sum():,.2f} ha")
print(reg[["regla", "n_afectados", "unidad", "descripcion"]].to_string(index=False))
