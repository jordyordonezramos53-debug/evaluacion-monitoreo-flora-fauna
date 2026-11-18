"""Paso 8. Análisis exploratorio de la base curada.

Entradas : data/processed/plantaciones_curada.csv (una fila por plantación)
           data/processed/plantaciones_especies_curada.csv (plantación × especie)
Salidas  : data/processed/eda/*.csv (tablas)  y  figures/*.png (gráficos)

Regla clave: la superficie se suma SIEMPRE desde la tabla por plantación,
excluyendo las plantaciones con superficie = 0 (flag_superficie_cero).
"""
import matplotlib
import matplotlib.ticker

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

from comun import FIGURES, PROCESSED, salida_utf8  # noqa: E402

salida_utf8()
EDA = PROCESSED / "eda"
EDA.mkdir(parents=True, exist_ok=True)
FIGURES.mkdir(parents=True, exist_ok=True)

# Estilo: una sola serie por gráfico, color de serie 1 de la paleta de referencia,
# texto en tinta neutra, cuadrícula tenue.
AZUL, TINTA, TINTA2, FONDO, REJILLA = "#2a78d6", "#0b0b0b", "#52514e", "#fcfcfb", "#e4e3df"
plt.rcParams.update({
    "figure.facecolor": FONDO, "axes.facecolor": FONDO, "savefig.facecolor": FONDO,
    "axes.edgecolor": REJILLA, "axes.labelcolor": TINTA2, "xtick.color": TINTA2,
    "ytick.color": TINTA2, "text.color": TINTA, "font.size": 10,
    "axes.spines.top": False, "axes.spines.right": False,
    "axes.grid": True, "grid.color": REJILLA, "grid.linewidth": 0.6, "axes.axisbelow": True,
})
miles = matplotlib.ticker.FuncFormatter(lambda v, _: f"{v:,.0f}".replace(",", " "))

p = pd.read_csv(PROCESSED / "plantaciones_curada.csv", dtype={"ubigeo": str})
e = pd.read_csv(PROCESSED / "plantaciones_especies_curada.csv", dtype={"ubigeo": str})
pv = p[~p["flag_superficie_cero"]].copy()  # plantaciones con superficie válida


def guardar(fig, nombre):
    fig.tight_layout()
    fig.savefig(FIGURES / nombre, dpi=150)
    plt.close(fig)


def barras_h(serie, titulo, xlabel, nombre):
    serie = serie.sort_values()
    fig, ax = plt.subplots(figsize=(8, 0.38 * len(serie) + 1.2))
    ax.barh(serie.index, serie.values, color=AZUL, height=0.7)
    ax.grid(axis="y", visible=False)
    for y, v in enumerate(serie.values):
        ax.text(v, y, " " + f"{v:,.0f}".replace(",", " "), va="center", fontsize=8.5, color=TINTA2)
    ax.xaxis.set_major_formatter(miles)
    ax.set_title(titulo, loc="left", fontsize=12, color=TINTA)
    ax.set_xlabel(xlabel)
    ax.margins(x=0.12)
    guardar(fig, nombre)


# 1. Resumen general -----------------------------------------------------------
resumen = pd.DataFrame([
    ("Plantaciones", len(p)),
    ("Plantaciones con superficie válida", len(pv)),
    ("Superficie total (ha)", round(pv["superficie_ha"].sum(), 2)),
    ("Superficie media (ha)", round(pv["superficie_ha"].mean(), 2)),
    ("Superficie mediana (ha)", round(pv["superficie_ha"].median(), 2)),
    ("Superficie P90 (ha)", round(pv["superficie_ha"].quantile(0.9), 2)),
    ("Superficie máxima (ha)", round(pv["superficie_ha"].max(), 2)),
    ("% de la superficie en el 10 % de plantaciones más grandes",
     round(100 * pv.nlargest(int(len(pv) * 0.1), "superficie_ha")["superficie_ha"].sum() / pv["superficie_ha"].sum(), 1)),
    ("Titulares distintos", p["id_titular"].nunique()),
    ("Especies distintas (nombre aceptado)", e["nombre_aceptado"].nunique()),
    ("Familias distintas", e["familia"].nunique()),
    ("Plantaciones de una sola especie", int((p["n_especies"] == 1).sum())),
    ("Plantaciones mixtas (2 o más especies)", int((p["n_especies"] >= 2).sum())),
    ("Plantaciones sin especie identificada", int((p["n_especies"] == 0).sum())),
    ("Plantaciones de menos de 0,01 ha (100 m²)", int((pv["superficie_ha"] < 0.01).sum())),
], columns=["indicador", "valor"])
resumen.to_csv(EDA / "resumen_general.csv", index=False, encoding="utf-8")

# 2. Por año de inscripción -------------------------------------------------------
anio = pv.groupby("periodo").agg(plantaciones=("id_plantacion", "size"),
                                 superficie_ha=("superficie_ha", "sum"),
                                 mediana_ha=("superficie_ha", "median")).round(2)
anio.to_csv(EDA / "por_anio.csv", encoding="utf-8")
fig, ax = plt.subplots(figsize=(8, 4))
ax.bar(anio.index.astype(str), anio["superficie_ha"] / 1000, color=AZUL, width=0.7)
ax.grid(axis="x", visible=False)
ax.set_title("Superficie inscrita por año de inscripción (2025: hasta el 11 de junio)", loc="left", fontsize=12)
ax.set_ylabel("miles de ha")
for x, v in zip(anio.index.astype(str), anio["superficie_ha"] / 1000):
    ax.text(x, v, f"{v:.1f}".replace(".", ","), ha="center", va="bottom", fontsize=8.5, color=TINTA2)
guardar(fig, "fig01_superficie_por_anio.png")

# 3. Por departamento -----------------------------------------------------------
dep = pv.groupby("departamento").agg(plantaciones=("id_plantacion", "size"),
                                     superficie_ha=("superficie_ha", "sum")).round(2)
dep["pct_superficie"] = (100 * dep["superficie_ha"] / dep["superficie_ha"].sum()).round(1)
dep = dep.sort_values("superficie_ha", ascending=False)
dep.to_csv(EDA / "por_departamento.csv", encoding="utf-8")
barras_h(dep["superficie_ha"].head(15).rename(index=str.title),
         "Superficie inscrita por departamento (15 primeros)", "hectáreas",
         "fig02_superficie_por_departamento.png")

# 4. Por finalidad y tenencia ------------------------------------------------------
fin = pv.groupby("finalidades").agg(plantaciones=("id_plantacion", "size"),
                                    superficie_ha=("superficie_ha", "sum")).round(2)
fin["pct_superficie"] = (100 * fin["superficie_ha"] / fin["superficie_ha"].sum()).round(2)
fin.sort_values("superficie_ha", ascending=False).to_csv(EDA / "por_finalidad.csv", encoding="utf-8")
ten = pv.groupby("regimen_tenencia").agg(plantaciones=("id_plantacion", "size"),
                                         superficie_ha=("superficie_ha", "sum")).round(2)
ten.sort_values("superficie_ha", ascending=False).to_csv(EDA / "por_tenencia.csv", encoding="utf-8")
barras_h(fin["superficie_ha"].rename(index=lambda s: s.replace("|", " + ").capitalize()),
         "Superficie inscrita por finalidad", "hectáreas", "fig03_superficie_por_finalidad.png")

# 5. Especies más frecuentes (n.º de plantaciones en que aparecen) ----------------
esp = (e.dropna(subset=["nombre_aceptado"])
        .drop_duplicates(["id_plantacion", "nombre_aceptado"])
        .groupby(["nombre_aceptado", "familia"]).size().rename("plantaciones")
        .reset_index().sort_values("plantaciones", ascending=False))
esp.to_csv(EDA / "especies_frecuencia.csv", index=False, encoding="utf-8")
top = esp.head(15).set_index("nombre_aceptado")["plantaciones"]
barras_h(top, "Especies en más plantaciones (15 primeras)", "n.º de plantaciones",
         "fig04_especies_frecuentes.png")

# 6. Distribución del tamaño de plantación (escala logarítmica) -------------------
fig, ax = plt.subplots(figsize=(8, 4))
bins = np.logspace(np.log10(pv["superficie_ha"].min()), np.log10(pv["superficie_ha"].max()), 40)
ax.hist(pv["superficie_ha"], bins=bins, color=AZUL, edgecolor=FONDO, linewidth=1)
ax.set_xscale("log")
ax.grid(axis="x", visible=False)
med = pv["superficie_ha"].median()
ax.axvline(med, color=TINTA2, linewidth=1.2, linestyle="--")
ax.text(med, ax.get_ylim()[1] * 0.95, f"  mediana = {med:.2f} ha".replace(".", ","), color=TINTA2, fontsize=9, va="top")
ax.set_title("Distribución del tamaño de las plantaciones", loc="left", fontsize=12)
ax.set_xlabel("superficie por plantación (ha, escala logarítmica)")
ax.set_ylabel("n.º de plantaciones")
guardar(fig, "fig05_distribucion_superficie.png")
cortes = [0, 1, 5, 10, 50, 100, 500, np.inf]
etiquetas = ["<1", "1-5", "5-10", "10-50", "50-100", "100-500", ">500"]
tam = pv.assign(rango_ha=pd.cut(pv["superficie_ha"], cortes, labels=etiquetas, right=False))
tam = tam.groupby("rango_ha", observed=False).agg(plantaciones=("id_plantacion", "size"),
                                                  superficie_ha=("superficie_ha", "sum")).round(2)
tam["pct_plantaciones"] = (100 * tam["plantaciones"] / tam["plantaciones"].sum()).round(1)
tam["pct_superficie"] = (100 * tam["superficie_ha"] / tam["superficie_ha"].sum()).round(1)
tam.to_csv(EDA / "por_rango_superficie.csv", encoding="utf-8")

# 7. Grupos de especies compatibles con IPCC (Tabla 4.10) -------------------------
CONIFERAS = {"Pinaceae", "Cupressaceae", "Podocarpaceae", "Araucariaceae"}


def grupo(fila):
    n, f, g = str(fila["nombre_aceptado"]), str(fila["familia"]), str(fila["nombre_aceptado"]).split(" ")[0]
    if g in ("Eucalyptus", "Corymbia"):  # Corymbia se separó de Eucalyptus; se registró como E. torelliana
        return "Eucalyptus spp."
    if g == "Pinus":
        return "Pinus spp."
    if n.startswith("Tectona grandis"):
        return "Tectona grandis"
    if f == "Poaceae":
        return "Bambúes (Poaceae)"
    if f in CONIFERAS:
        return "Otras coníferas"
    if fila["nombre_aceptado"] is np.nan or n == "nan":
        return "Sin especie"
    return "Otras latifoliadas"


e["grupo_ipcc"] = e.apply(grupo, axis=1)
grupos_por_plant = e.groupby("id_plantacion")["grupo_ipcc"].agg(lambda s: sorted(set(s) - {"Sin especie"}))
pv["grupo_ipcc"] = pv["id_plantacion"].map(
    lambda i: (grupos_por_plant.get(i) or ["Sin especie"])[0] if len(grupos_por_plant.get(i) or []) <= 1
    else "Mixta (varios grupos)")
gr = pv.groupby("grupo_ipcc").agg(plantaciones=("id_plantacion", "size"),
                                  superficie_ha=("superficie_ha", "sum")).round(2)
gr["pct_superficie"] = (100 * gr["superficie_ha"] / gr["superficie_ha"].sum()).round(1)
gr = gr.sort_values("superficie_ha", ascending=False)
gr.to_csv(EDA / "por_grupo_ipcc.csv", encoding="utf-8")
barras_h(gr["superficie_ha"], "Superficie por grupo de especies (categorías del IPCC)",
         "hectáreas", "fig06_superficie_por_grupo_ipcc.png")

# 8. Vacíos de información --------------------------------------------------------
vacios = pd.DataFrame([
    ("Coordenadas o polígonos", "No existe", "Impide ubicar la zona ecológica y verificar con imágenes"),
    ("Año de plantación o edad", "No existe (solo año de inscripción)", "Impide estimar crecimiento acumulado"),
    ("Supervivencia o estado actual", "No existe", "No se sabe cuánta superficie inscrita sigue en pie"),
    ("Proporción de cada especie en plantaciones mixtas", "No existe",
     f"{int((p['n_especies'] >= 2).sum())} plantaciones mixtas no se pueden asignar a una sola especie"),
    ("Densidad, DAP, altura", "No existe", "Impide estimar biomasa con ecuaciones alométricas"),
    ("Especie", f"{int(e['flag_sin_especie'].sum())} filas sin dato", "Menor; se marca"),
    ("Identificación a especie", f"{int((e['nivel_identificacion'] == 'género o superior').sum())} filas solo a género",
     "Se agrupan por género"),
], columns=["variable", "situacion", "consecuencia"])
vacios.to_csv(EDA / "vacios_informacion.csv", index=False, encoding="utf-8")

print(resumen.to_string(index=False))
print("\nPor grupo IPCC:\n", gr.to_string())
print("\nPor finalidad:\n", fin.to_string())
print("\nPor rango de superficie:\n", tam.to_string())
print("\nPor año:\n", anio.to_string())
print("\nTop 10 departamentos:\n", dep.head(10).to_string())
print("\nTop 10 especies:\n", esp.head(10).to_string(index=False))
print("\nTenencia:\n", ten.to_string())
