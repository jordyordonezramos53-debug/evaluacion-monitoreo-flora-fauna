"""Funciones y rutas compartidas por los scripts de la práctica."""
import hashlib
import sys
from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parents[1]
RAW = RAIZ / "data" / "raw"
PROCESSED = RAIZ / "data" / "processed"
FIGURES = RAIZ / "figures"

ARCHIVO_ORIGINAL = RAW / "Plantaciones_208.xls"
SHA256_ESPERADO = "dc98fc142b13ac2191a370d1cc2320fad4b0ecc3aace00cdf506411f51e7b2c9"

# Nombres originales -> nombres normalizados (snake_case, sin tildes)
RENOMBRAR = {
    "ID PLANTACION": "id_plantacion",
    "PERIODO": "periodo",
    "DEPARTAMENTO": "departamento",
    "PROVINCIA": "provincia",
    "DISTRITO": "distrito",
    "ARFFS": "arffs",
    "SEDE": "sede",
    "UBIGEO": "ubigeo",
    "FINALIDAD": "finalidad",
    "NUMERO CERTIFICADO": "numero_certificado",
    "TITULAR": "titular",
    "TIPO PERSONA": "tipo_persona",
    "TIPO DOCUMENTO": "tipo_documento",
    "NUMERO DOCUMENTO": "numero_documento",
    "REGIMEN TENENCIA": "regimen_tenencia",
    "TIPO PLANTACION": "tipo_plantacion",
    "ESPECIE": "especie_original",
    "SUPERFICIE PLANTACION": "superficie_plantacion_ha",
    "FECHA CORTE": "fecha_corte",
}


def salida_utf8():
    """Evita errores de consola de Windows al imprimir tildes."""
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:
        pass


def sha256(ruta: Path) -> str:
    h = hashlib.sha256()
    with open(ruta, "rb") as f:
        for bloque in iter(lambda: f.read(1 << 20), b""):
            h.update(bloque)
    return h.hexdigest()


def leer_original() -> pd.DataFrame:
    """Lee el archivo original SIN modificarlo, todo como texto.

    Se lee como texto para no perder ceros a la izquierda (UBIGEO, DNI).
    El archivo tiene extensión .xls pero en realidad es un libro XLSX,
    por eso se fuerza el motor openpyxl.
    """
    if not ARCHIVO_ORIGINAL.exists():
        sys.exit(f"Falta {ARCHIVO_ORIGINAL}. Ver data/raw/FUENTE.md para descargarlo.")
    huella = sha256(ARCHIVO_ORIGINAL)
    if huella != SHA256_ESPERADO:
        print(f"ADVERTENCIA: el SHA-256 no coincide ({huella}). "
              "El archivo no es la versión documentada.")
    return pd.read_excel(ARCHIVO_ORIGINAL, engine="openpyxl", dtype=str)
