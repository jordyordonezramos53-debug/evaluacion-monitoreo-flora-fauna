"""Paso 5. Exporta la base curada con términos de Darwin Core (estándar de datos de biodiversidad).

Entradas : data/processed/plantaciones_especies_curada.csv
           data/processed/tabla_taxonomica.csv
Salida   : data/processed/darwin_core_ocurrencias.csv  (una fila por plantación × especie identificada)

Darwin Core: https://dwc.tdwg.org/terms/  · Cada fila es el registro de una especie cultivada en
una plantación inscrita. Las filas sin especie (flag_sin_especie) no se exportan porque Darwin Core
exige un nombre científico. No se exporta ningún dato de titulares.
"""
import json

import pandas as pd

from comun import PROCESSED, salida_utf8

salida_utf8()

e = pd.read_csv(PROCESSED / "plantaciones_especies_curada.csv", dtype=str)
tax = pd.read_csv(PROCESSED / "tabla_taxonomica.csv", dtype=str)[["nombre_registrado", "gbif_usage_key"]]
e = e.merge(tax, how="left", left_on="especie_original", right_on="nombre_registrado")
e = e[e["flag_sin_especie"] != "True"].copy()
e = e.sort_values(["id_plantacion", "especie_original", "finalidad", "tipo_plantacion"]).reset_index(drop=True)
e["n"] = e.groupby("id_plantacion").cumcount() + 1

rango = {"SPECIES": "species", "SUBSPECIES": "subspecies", "VARIETY": "variety", "FORM": "form",
         "GENUS": "genus", "FAMILY": "family", "HYBRID": "nothospecies"}


def taxon_id(fila):
    if fila["decision_taxonomica"] == "ACEPTAR" and isinstance(fila["gbif_usage_key"], str):
        return f"https://www.gbif.org/species/{int(float(fila['gbif_usage_key']))}"
    return ""


def observaciones(fila):
    marcas = {"flag_superficie_cero": "superficie de 0 ha", "flag_superficie_atipica": "superficie atípica",
              "flag_superficie_mayor_500ha": "superficie mayor de 500 ha",
              "flag_id_especie_repetido": "misma especie inscrita con otra finalidad o tipo"}
    return "; ".join(t for c, t in marcas.items() if fila[c] == "True")


dwc = pd.DataFrame({
    "occurrenceID": "SERFOR-RNPF-" + e["id_plantacion"] + "-" + e["n"].astype(str),
    "basisOfRecord": "HumanObservation",
    "degreeOfEstablishment": "cultivated",
    "institutionCode": "SERFOR",
    "collectionCode": "RNPF",
    "year": e["periodo"],  # año de inscripción, no de plantación (ver docs/05_diccionario_datos.md)
    "country": "Peru",
    "countryCode": "PE",
    "stateProvince": e["departamento"],
    "county": e["provincia"],
    "municipality": e["distrito"],
    "locationID": "UBIGEO:" + e["ubigeo"],
    "scientificName": e["nombre_aceptado"],
    "verbatimIdentification": e["especie_original"],
    "taxonRank": e["rango_taxonomico"].map(rango).fillna(""),
    "family": e["familia"],
    "kingdom": "Plantae",
    "taxonID": e.apply(taxon_id, axis=1),
    "identificationRemarks": e["decision_taxonomica"].map(
        {"ACEPTAR": "Nombre resuelto con GBIF Backbone", "REVISADO_MANUAL": "Revisión manual (regla R12)"}),
    "occurrenceRemarks": e.apply(observaciones, axis=1),
    "dynamicProperties": [json.dumps({"id_plantacion": int(i), "superficie_plantacion_ha": float(s),
                                      "finalidad": f, "tipo_plantacion": t}, ensure_ascii=False)
                          for i, s, f, t in zip(e["id_plantacion"], e["superficie_plantacion_ha"],
                                                e["finalidad"], e["tipo_plantacion"])],
})

assert dwc["occurrenceID"].is_unique
dwc.to_csv(PROCESSED / "darwin_core_ocurrencias.csv", index=False, encoding="utf-8")
print(f"Registros Darwin Core: {len(dwc)} (se omiten {int((pd.read_csv(PROCESSED / 'plantaciones_especies_curada.csv', dtype=str)['flag_sin_especie'] == 'True').sum())} filas sin especie)")
print(f"Con taxonID de GBIF: {(dwc['taxonID'] != '').sum()} | rangos: {dwc['taxonRank'].value_counts().to_dict()}")
