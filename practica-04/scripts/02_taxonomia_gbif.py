"""Paso 3b. Estandarización taxonómica con el GBIF Backbone Taxonomy.

Para cada nombre de especie distinto se consulta el servicio público
https://api.gbif.org/v1/species/match y se guarda la respuesta en
data/processed/tabla_taxonomica.csv.

La tabla funciona como caché: si un nombre ya fue consultado, no se vuelve
a consultar. Así el resultado es reproducible aunque GBIF actualice su
taxonomía. Para rehacer la consulta, borrar la tabla.

Regla de decisión (columna `decision`):
  ACEPTAR  -> coincidencia EXACT; FUZZY con confianza >= 90; o HIGHERRANK
              cuando GBIF igual resolvió a nivel de especie (autor mal escrito)
  REVISAR  -> resuelto solo a género o superior (p. ej. 'Pinus sp.'),
              FUZZY < 90 o sin coincidencia
"""
import json
import time
import urllib.parse
import urllib.request
from datetime import date

import pandas as pd

from comun import PROCESSED, leer_original, salida_utf8

salida_utf8()
TABLA = PROCESSED / "tabla_taxonomica.csv"
URL = "https://api.gbif.org/v1/species/match?kingdom=Plantae&name="


def limpiar(nombre: str) -> str:
    """Quita espacios sobrantes (no cambia mayúsculas: eso se hace en `para_consulta`)."""
    return " ".join(str(nombre).split())


def para_consulta(nombre: str) -> str:
    """Corrige el epíteto escrito con mayúscula ('Capparis Flexuosa' -> 'Capparis flexuosa').

    Sin esta corrección GBIF no reconoce el nombre. Solo se aplica a nombres
    de dos palabras, para no alterar los autores (que sí llevan mayúscula).
    """
    partes = nombre.split()
    if len(partes) == 2 and partes[1][:1].isupper():
        partes[1] = partes[1].lower()
    return " ".join(partes)


def consultar(nombre: str) -> dict:
    with urllib.request.urlopen(URL + urllib.parse.quote(nombre), timeout=30) as r:
        return json.load(r)


def fila(nombre: str, j: dict) -> dict:
    tipo = j.get("matchType", "NONE")
    conf = j.get("confidence", 0)
    rango = j.get("rank", "")
    if rango in ("SPECIES", "VARIETY", "SUBSPECIES", "FORM"):
        aceptado = j.get("species", "")
    else:
        aceptado = j.get("canonicalName", "")
    especie_o_menor = rango in ("SPECIES", "VARIETY", "SUBSPECIES", "FORM")
    ok = (tipo == "EXACT" or (tipo == "FUZZY" and conf >= 90)
          or (tipo == "HIGHERRANK" and especie_o_menor))  # p. ej. autor mal escrito
    return {
        "nombre_registrado": nombre,
        "nombre_consultado": para_consulta(nombre),
        "gbif_nombre_canonico": j.get("canonicalName", ""),
        "gbif_nombre_cientifico": j.get("scientificName", ""),
        "gbif_estado": j.get("status", ""),
        "gbif_rango": rango,
        "nombre_aceptado": aceptado,
        "genero": j.get("genus", ""),
        "familia": j.get("family", ""),
        "gbif_tipo_coincidencia": tipo,
        "gbif_confianza": conf,
        "gbif_usage_key": j.get("usageKey", ""),
        "decision": "ACEPTAR" if ok else "REVISAR",
        "fecha_consulta": date.today().isoformat(),
    }


df = leer_original()
nombres = sorted({limpiar(n) for n in df["ESPECIE"].dropna()})
previa = pd.read_csv(TABLA, dtype=str) if TABLA.exists() else pd.DataFrame(columns=["nombre_registrado"])
hechos = set(previa["nombre_registrado"])
pendientes = [n for n in nombres if n not in hechos]
print(f"Nombres distintos: {len(nombres)} | ya en caché: {len(hechos)} | por consultar: {len(pendientes)}")

nuevas = []
for i, n in enumerate(pendientes, 1):
    try:
        nuevas.append(fila(n, consultar(para_consulta(n))))
    except Exception as e:  # noqa: BLE001 - se registra y se sigue
        nuevas.append({"nombre_registrado": n, "decision": "REVISAR", "gbif_tipo_coincidencia": f"ERROR: {e}"})
    if i % 50 == 0:
        print(f"  {i}/{len(pendientes)}")
    time.sleep(0.1)  # consulta pausada para no sobrecargar el servicio

tabla = pd.concat([previa, pd.DataFrame(nuevas)], ignore_index=True)
tabla.to_csv(TABLA, index=False, encoding="utf-8")
print(tabla["decision"].value_counts().to_string())
print(tabla["gbif_estado"].value_counts().to_string())
print(f"Guardado en {TABLA}")
