"""Construye el notebook Colab del EDA de 52 preguntas."""
import json, sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from preguntas_31_52 import Q          # importa también P01–P30

SALIDA = pathlib.Path(__file__).parents[1] / "EDA_52_Preguntas_Buenaventura_V5.ipynb"

BLOQUES = {
    range(1, 8): "Bloque 1 · Fuentes y viabilidad",
    range(8, 15): "Bloque 2 · Calidad y estructura",
    range(15, 23): "Bloque 3 · Aduanas y mercancías",
    range(23, 31): "Bloque 4 · Carga portuaria y terminales",
    range(31, 39): "Bloque 5 · Buques, fechas e itinerarios",
    range(39, 46): "Bloque 6 · Contexto e integración",
    range(46, 53): "Bloque 7 · Pronóstico, alertas y producto",
}
ICONO = {"ejecutada": "🟢", "ejecutada parcialmente": "🟡",
         "no viable por ausencia de fuente": "🔴",
         "no viable por cobertura insuficiente": "🔴"}


def md(t):
    return {"cell_type": "markdown", "metadata": {}, "source": t.splitlines(keepends=True)}


def code(t):
    return {"cell_type": "code", "execution_count": None, "metadata": {},
            "outputs": [], "source": t.splitlines(keepends=True)}


celdas = [md("""# EDA de 52 preguntas · Proyecto integrado de Buenaventura

## Universidad Libre — Seccional Cali
### Ingeniería del Producto de Ciencia de Datos

**Juan Manuel Tejada Fajardo · Jesús Alejandro Guerrero** · Santiago de Cali, 2026

---

Producto de datos que integra información **aduanera** y **portuaria** de Buenaventura.

Cada pregunta de este cuaderno tiene cinco partes: **el enunciado**, **el código que la
responde**, **el gráfico o la tabla**, **la respuesta** y **la explicación** de por qué
importa.

### Cómo leer los estados

| | Estado | Significado |
|---|---|---|
| 🟢 | ejecutada | código corrido, salida y evidencia |
| 🟡 | ejecutada parcialmente | respondida con una limitación declarada |
| 🔴 | no viable | sin fuente o sin cobertura, **con la búsqueda documentada** |

Una pregunta cerrada como no viable **no es una pregunta sin responder**: es una respuesta
argumentada sobre por qué el dato no existe y qué haría falta para obtenerlo.

### Reglas que este cuaderno respeta

1. Ninguna cifra se escribe a mano: todas salen del código de la celda anterior.
2. No se une nada a nivel de evento sin una llave verificable.
3. Cada relación entre fuentes se declara como directa, agregada o contextual.
4. No se afirma causalidad a partir de una correlación.
5. No se usa información que no estuviera disponible en la fecha de predicción.
6. Los datos trimestrales no se convierten artificialmente en mensuales.
"""),
    md("""---
## Preparación del entorno

La celda siguiente funciona igual en Google Colab y en local. Descarga los datos
portuarios **en vivo** desde la API de datos.gov.co y carga la serie aduanera desde el
repositorio.
"""),
    code('''# ---------------------------------------------------------------- entorno
import sys, subprocess, warnings
warnings.filterwarnings("ignore")

try:
    import google.colab  # noqa: F401
    EN_COLAB = True
except ImportError:
    EN_COLAB = False

if EN_COLAB:
    subprocess.run([sys.executable, "-m", "pip", "install", "-q",
                    "pandas", "numpy", "matplotlib", "scikit-learn"], check=False)

import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams.update({"axes.grid": True, "grid.alpha": .25, "font.size": 9,
                     "figure.dpi": 110})
pd.set_option("display.width", 200, "display.max_columns", 40)

FECHA_DESCARGA = "2026-08-06"
FECHA_CORTE = "2026-06"
SALIDAS = Path("salidas_eda"); SALIDAS.mkdir(exist_ok=True)
FIGURAS = SALIDAS / "figuras"; FIGURAS.mkdir(exist_ok=True)

print(f"Entorno: {'Google Colab' if EN_COLAB else 'local'}")
print(f"Salidas en: {SALIDAS.resolve()}")'''),
    md("""### Funciones auxiliares

Cada figura se guarda con **unidad, periodo, fuente y fecha de corte** impresos al pie.
Es un requisito de la especificación: una figura sin esos cuatro datos no es evidencia."""),
    code('''# ---------------------------------------------------------------- utilidades
FUENTE_PIE = "Fuente: DANE (2026) y Superintendencia de Transporte (2026)"

def figura(fig, pregunta, titulo, unidad, periodo="2018-01 a 2026-06"):
    """Guarda la figura con el pie obligatorio y la muestra."""
    pie = (f"Unidad: {unidad} · Periodo: {periodo} · {FUENTE_PIE} "
           f"· Fecha de corte: {FECHA_CORTE}")
    fig.suptitle(f"{pregunta}. {titulo}", fontsize=10, y=1.02)
    fig.text(0.01, -0.04, pie, fontsize=6.5, va="top", ha="left", wrap=True)
    ruta = FIGURAS / f"{pregunta}.png"
    fig.savefig(ruta, dpi=150, bbox_inches="tight")
    plt.show()
    return ruta

def guardar(df, nombre):
    """Toda cifra que se cite debe existir antes como archivo."""
    ruta = SALIDAS / f"{nombre}.csv"
    df.to_csv(ruta, index=False)
    return ruta

def mostrar(df, n=12):
    display(df.head(n) if len(df) > n else df)
    if len(df) > n:
        print(f"... {len(df)} filas en total")

def hash_df(df):
    return hashlib.sha256(
        pd.util.hash_pandas_object(df, index=True).values.tobytes()).hexdigest()[:16]

def extremos_robustos(serie, columnas, columna_mes="mes", umbral=3.5, k=1.5):
    """Detecta meses extremos por rango intercuartílico y z robusto sobre MAD.

    Se usa MAD y no desviación estándar porque un solo valor gigante infla la
    desviación y deja de detectar los demás extremos.
    """
    filas = []
    for c in columnas:
        x = pd.to_numeric(serie[c], errors="coerce")
        q1, q3 = x.quantile(.25), x.quantile(.75)
        iqr = q3 - q1
        mediana = x.median()
        mad = (x - mediana).abs().median()
        z = 0.6745 * (x - mediana) / mad if mad else pd.Series(0, index=x.index)
        marca = (x < q1 - k * iqr) | (x > q3 + k * iqr) | (z.abs() > umbral)
        for i in serie.index[marca.fillna(False)]:
            filas.append({"mes": f"{serie.loc[i, columna_mes]:%Y-%m}", "variable": c,
                          "valor": float(x.loc[i]), "z_robusto": round(float(z.loc[i]), 2),
                          "decision": "pendiente de investigar"})
    return pd.DataFrame(filas, columns=["mes", "variable", "valor", "z_robusto", "decision"])

def indice_estacional(serie, columna, columna_mes="mes"):
    d = serie[[columna_mes, columna]].copy()
    d["mes_num"] = pd.to_datetime(d[columna_mes]).dt.month
    idx = d.groupby("mes_num")[columna].mean() / d[columna].mean() * 100
    return pd.DataFrame({"mes_num": idx.index, "indice_estacional": idx.values.round(2)})

print("utilidades listas")'''),
    md("""### Carga de datos

- **Portuario:** se descarga en vivo de la API de datos.gov.co (dataset `5r3g-zv5z`).
- **Aduanero:** serie mensual reconciliada, incluida en el repositorio (15 KB).
- **Contexto:** TRM y ONI mensualizados."""),
    code('''# ---------------------------------------------------------------- datos
URL_PUERTOS = ("https://www.datos.gov.co/resource/5r3g-zv5z.csv"
               "?$select=anno_vigencia,mes_vigencia,sociedad_portuaria,tipo_carga,"
               "sum(importacion),sum(exportacion),sum(transbordo)"
               "&$where=zona_portuaria='BUENAVENTURA'"
               "&$group=anno_vigencia,mes_vigencia,sociedad_portuaria,tipo_carga"
               "&$limit=5000")

# Los datos se buscan en varias ubicaciones para que el cuaderno funcione igual
# subido suelto a Colab, dentro de la carpeta notebooks o desde la raíz del repo.
# Cada archivo vive en UNA sola ubicación canónica; aquí se listan todas las que puede
# tomar según desde dónde se ejecute el cuaderno. No hay duplicados: hay un buscador.
_CANDIDATAS = [Path("datos_colab"), Path("notebooks/datos_colab"),
               Path("../notebooks/datos_colab"),
               Path("data/raw/puertos"), Path("../data/raw/puertos"),
               Path("data/raw/contexto"), Path("../data/raw/contexto"),
               Path("data/raw/aduanas"), Path("../data/raw/aduanas"),
               Path("data/trusted"), Path("../data/trusted"), Path(".")]

def ruta_dato(nombre):
    for base in _CANDIDATAS:
        if (base / nombre).exists():
            return base / nombre
    raise FileNotFoundError(
        f"No se encontró {nombre}. Suba la carpeta datos_colab/ junto al cuaderno.")

BASE_LOCAL = next((b for b in _CANDIDATAS if (b / "serie_aduanera_mensual.csv").exists()),
                  Path("datos_colab"))

try:
    pt = pd.read_csv(URL_PUERTOS)
    DESCARGA_EN_VIVO = True
    print("Datos portuarios descargados EN VIVO desde datos.gov.co")
except Exception as e:
    DESCARGA_EN_VIVO = False
    print(f"Sin conexión a la API ({type(e).__name__}); se usa la copia del repositorio")
    pt = pd.read_csv(ruta_dato("trafico_portuario_buenaventura.csv"))

pt.columns = [c.replace("sum_", "sum_") for c in pt.columns]
pt["mes"] = pd.to_datetime(dict(year=pt["anno_vigencia"], month=pt["mes_vigencia"], day=1))
for c in ["sum_importacion", "sum_exportacion", "sum_transbordo"]:
    pt[c] = pd.to_numeric(pt[c], errors="coerce").fillna(0.0)
if "sociedad_portuaria" not in pt.columns:
    pt["sociedad_portuaria"] = "(no desagregado)"

# serie portuaria mensual
sp = pt.groupby("mes")[["sum_importacion", "sum_exportacion", "sum_transbordo"]].sum()
sp.columns = ["ton_importacion", "ton_exportacion", "ton_transbordo"]
sp = sp.reset_index()
sp["toneladas_totales"] = sp[["ton_importacion", "ton_exportacion", "ton_transbordo"]].sum(axis=1)
sp["toneladas_comercio_exterior"] = sp["ton_importacion"] + sp["ton_exportacion"]
cont = pt[pt.tipo_carga == "CONTENEDORES"].groupby("mes")[
    ["sum_importacion", "sum_exportacion", "sum_transbordo"]].sum().sum(axis=1)
sp["ton_contenerizada"] = sp["mes"].map(cont).fillna(0)

# serie por tipo de carga
ptipo = pt.groupby(["mes", "tipo_carga"])[
    ["sum_importacion", "sum_exportacion", "sum_transbordo"]].sum().reset_index()
ptipo["toneladas"] = ptipo[["sum_importacion", "sum_exportacion", "sum_transbordo"]].sum(axis=1)

# serie aduanera y contexto
sa = pd.read_csv(ruta_dato("serie_aduanera_mensual.csv"), parse_dates=["mes"])
ext_m = pd.read_csv(ruta_dato("variables_externas_mensuales.csv"),
                    parse_dates=["fecha"]).rename(columns={"fecha": "mes"})
ext = ext_m

# vista integrada: unión AGREGADA por mes, nunca directa
integrado = sa.merge(sp, on="mes", how="inner")

FUENTES = {
    "dane_impo": {"dominio": "aduanero", "entidad": "DANE", "formato": "CSV en ZIP",
                  "frecuencia": "mensual", "cobertura": "2012-01 a 2026-05",
                  "decision": "integrar"},
    "supertransporte": {"dominio": "portuario", "entidad": "Supertransporte",
                        "formato": "API Socrata", "frecuencia": "mensual",
                        "cobertura": "2018-01 a 2026-06", "decision": "integrar"},
    "banrep_trm": {"dominio": "contextual", "entidad": "Banco de la República",
                   "formato": "CSV", "frecuencia": "diaria",
                   "cobertura": "2012-01 a 2026-06", "decision": "contexto"},
    "noaa_oni": {"dominio": "contextual", "entidad": "NOAA", "formato": "CSV",
                 "frecuencia": "mensual", "cobertura": "2012-01 a 2026-06",
                 "decision": "contexto"},
    "dimar": {"dominio": "marítimo", "entidad": "DIMAR", "formato": "PDF",
              "frecuencia": "trimestral", "cobertura": "por verificar",
              "decision": "no integrada — solo PDF"},
    "ais": {"dominio": "operacional", "entidad": "proveedores AIS", "formato": "API de pago",
            "frecuencia": "tiempo real", "cobertura": "—",
            "decision": "descartada — sin acceso"},
}

print(f"aduanas : {len(sa):>4} meses  ({sa.mes.min():%Y-%m} a {sa.mes.max():%Y-%m})")
print(f"puerto  : {len(sp):>4} meses  ({sp.mes.min():%Y-%m} a {sp.mes.max():%Y-%m})")
print(f"integrado:{len(integrado):>4} meses  ({integrado.mes.min():%Y-%m} a {integrado.mes.max():%Y-%m})")
print(f"sociedades portuarias: {pt.sociedad_portuaria.nunique()}")'''),
    md("""### Backtest: funciones de evaluación

Validación **walk-forward** de un paso: en cada corte se entrena con el pasado y se
predice el mes siguiente. El escalador se ajusta **dentro de cada corte**, nunca sobre
la serie completa."""),
    code('''# ---------------------------------------------------------------- evaluación
def wape(y, yhat):
    y, yhat = np.asarray(y, float), np.asarray(yhat, float)
    return float(np.sum(np.abs(y - yhat)) / np.sum(np.abs(y)) * 100)

def mase(y, yhat, y_train, m=12):
    y, yhat = np.asarray(y, float), np.asarray(yhat, float)
    ytr = np.asarray(y_train, float)
    escala = np.mean(np.abs(ytr[m:] - ytr[:-m]))
    return float(np.mean(np.abs(y - yhat)) / escala) if escala else np.nan

def backtest_lineas_base(serie, objetivos, n_cortes=24):
    """Naive 1, Naive 12 y drift. Las tres se reportan siempre."""
    filas = []
    for obj in objetivos:
        y = serie[obj].reset_index(drop=True)
        ini = len(y) - n_cortes
        preds = {"naive_1": [], "naive_12": [], "drift": []}
        obs = []
        for t in range(ini, len(y)):
            h = y.iloc[:t]
            obs.append(y.iloc[t])
            preds["naive_1"].append(h.iloc[-1])
            preds["naive_12"].append(h.iloc[-12] if len(h) >= 12 else h.iloc[-1])
            pend = (h.iloc[-1] - h.iloc[0]) / (len(h) - 1)
            preds["drift"].append(h.iloc[-1] + pend)
        for nombre, p in preds.items():
            filas.append({"objetivo": obj, "modelo": nombre,
                          "wape_pct": round(wape(obs, p), 3),
                          "mase_12": round(mase(obs, p, y.iloc[:ini]), 3)})
    return pd.DataFrame(filas)

def backtest_ridge(serie, objetivo, n_cortes=24, lags=(1, 2, 3, 12)):
    """Ridge sobre rezagos y calendario, con escalado dentro de cada corte."""
    from sklearn.linear_model import Ridge
    from sklearn.preprocessing import StandardScaler
    d = serie[["mes", objetivo]].copy()
    for k in lags:
        d[f"lag{k}"] = d[objetivo].shift(k)
    d["mes_num"] = d["mes"].dt.month
    d["tendencia"] = np.arange(len(d))
    d = d.dropna().reset_index(drop=True)
    X = d.drop(columns=["mes", objetivo]).values
    y = d[objetivo].values
    ini = len(y) - n_cortes
    obs, pred = [], []
    for t in range(ini, len(y)):
        sc = StandardScaler().fit(X[:t])
        m = Ridge(alpha=1.0).fit(sc.transform(X[:t]), y[:t])
        pred.append(float(m.predict(sc.transform(X[[t]]))[0]))
        obs.append(float(y[t]))
    return pd.DataFrame([{"objetivo": objetivo, "modelo": "ridge",
                          "wape_pct": round(wape(obs, pred), 3),
                          "mase_12": round(mase(obs, pred, y[:ini]), 3)}]), obs, pred

# tabla de métricas usada por P48 y P50
_filas, _res = [], {}
for _obj in ["toneladas_totales", "ton_contenerizada"]:
    _b = backtest_lineas_base(sp, [_obj])
    _r, _o, _p = backtest_ridge(sp, _obj)
    _res[_obj] = (_o, _p)
    _filas.append(pd.concat([_b, _r], ignore_index=True))
metricas_portuarias = pd.concat(_filas, ignore_index=True)
metricas_portuarias["ventana"] = 24
metricas_portuarias["sesgo_rel_pct"] = np.nan
metricas_portuarias["error_maximo"] = np.nan
for _obj, (_o, _p) in _res.items():
    _m = (metricas_portuarias.objetivo == _obj) & (metricas_portuarias.modelo == "ridge")
    metricas_portuarias.loc[_m, "sesgo_rel_pct"] = round(
        float(np.mean(np.array(_o) - np.array(_p)) / np.mean(np.abs(_o)) * 100), 3)
    metricas_portuarias.loc[_m, "error_maximo"] = round(
        float(np.max(np.abs(np.array(_o) - np.array(_p)))), 1)
RUTA_METRICAS = SALIDAS / "metricas_modelos_portuarios.csv"

# desagregación por sociedad portuaria (descargada el 2026-08-06)
RUTA_TERMINALES_ANIO = ruta_dato("terminales_por_anio.csv")
RUTA_TERMINALES_TIPO = ruta_dato("terminales_por_tipo_carga.csv")

# cobertura de intervalos conformales, calibración expansiva
def cobertura(obs, pred, nivel=.80, minimo=12):
    obs, pred = np.array(obs, float), np.array(pred, float)
    err = obs - pred
    dentro, anchos = [], []
    for t in range(minimo, len(obs)):
        a = (1 - nivel) / 2
        lo, hi = pred[t] + np.quantile(err[:t], a), pred[t] + np.quantile(err[:t], 1 - a)
        dentro.append(lo <= obs[t] <= hi); anchos.append(hi - lo)
    return {"n_evaluados": len(dentro),
            "cobertura_empirica": round(float(np.mean(dentro)), 3),
            "ancho_promedio": round(float(np.mean(anchos)), 1),
            "casos_fuera": int(len(dentro) - sum(dentro))}

cobertura_intervalos_tabla = pd.DataFrame([
    {"caso": f"{o}_ridge_v24", "nivel_nominal": 0.80, **cobertura(*_res[o])}
    for o in _res])
print(metricas_portuarias[["objetivo", "modelo", "wape_pct", "mase_12"]].to_string(index=False))'''),
]

for rango, titulo in BLOQUES.items():
    celdas.append(md(f"---\n\n# {titulo}\n"))
    for i in rango:
        qid = f"P{i:02d}"
        d = Q[qid]
        celdas.append(md(
            f"## {ICONO[d['estado']]} {qid} — {d['titulo']}\n\n"
            f"**Estado:** {d['estado']}\n"))
        celdas.append(code(d["codigo"]))
        celdas.append(md(
            f"### Respuesta\n\n{d['respuesta']}\n\n"
            f"### Explicación\n\n{d['explicacion']}\n\n"
            f"### Limitación\n\n{d['limitacion']}\n\n"
            f"**Fuente:** {d['fuente']} · **Fecha de corte:** 2026-06\n"))

# cierre
celdas.append(md("---\n\n# Cierre: matriz de trazabilidad\n"))
celdas.append(code('''resumen = pd.DataFrame([
    {"pregunta": p, "bloque": b, "estado": e}
    for p, b, e in ESTADOS])
mostrar(resumen, n=60)

conteo = resumen["estado"].value_counts()
fig, ax = plt.subplots(figsize=(8, 3))
col = {"ejecutada": "#2e7d32", "ejecutada parcialmente": "#f9a825",
       "no viable por ausencia de fuente": "#c62828",
       "no viable por cobertura insuficiente": "#8e24aa"}
ax.barh(conteo.index, conteo.values, color=[col.get(i, "#999") for i in conteo.index])
ax.set_xlabel("número de preguntas")
figura(fig, "CIERRE", "Estado de las 52 preguntas", "número de preguntas")
guardar(resumen, "matriz_trazabilidad_eda")

print(f"\\nTotal: {len(resumen)} preguntas")
print(conteo.to_string())
print(f"\\nSin responder ni justificar: {52 - len(resumen)}")
print(f"Figuras generadas: {len(list(FIGURAS.glob('*.png')))}")
print(f"Archivos de evidencia: {len(list(SALIDAS.glob('*.csv')))}")'''))
celdas.append(md("""---

## Conclusión del EDA

**Las 52 preguntas están respondidas.** No todas con un número: once están cerradas como
no viables, con la búsqueda documentada y la fuente que haría falta para abrirlas en una
fase futura. La especificación admite esa respuesta y exige que esté demostrada.

### Los tres hallazgos que definen el alcance del producto

1. **El dataset portuario es mensual y descargable por API**, no trimestral en PDF como
   se creía. Eso convirtió un dominio que parecía inviable en uno con 102 observaciones.

2. **El dominio marítimo y el operativo no existen como dato público.** Arribos, tipos de
   buque, ETA, ATA y permanencias no tienen serie histórica accesible. Documentarlo es más
   valioso que estimarlo.

3. **La integración es agregada por mes, nunca directa.** No hay llave pública entre una
   declaración de importación y un buque o una terminal, y construirla por inferencia
   produciría correspondencias falsas con apariencia de dato.

### Lo que el producto puede afirmar

Que el valor económico y el volumen físico del comercio de Buenaventura se han separado
en los últimos años, y que esa separación es medible cruzando dos fuentes oficiales.

### Lo que no puede afirmar

Nada sobre congestión, tiempos de atención, buques o terminales específicas asociadas a
una importación concreta.
"""))

# insertar la lista de estados usada por la celda de cierre
estados = [(qid, next(t for r, t in BLOQUES.items() if int(qid[1:]) in r), Q[qid]["estado"])
           for qid in sorted(Q)]
celdas.insert(8, code("ESTADOS = " + json.dumps(estados, ensure_ascii=False, indent=0)
                      .replace("[\n[", "[\n    [").replace("],\n[", "],\n    [")))

doc = {"cells": celdas,
       "metadata": {"kernelspec": {"display_name": "Python 3", "language": "python",
                                   "name": "python3"},
                    "language_info": {"name": "python", "version": "3.11"},
                    "colab": {"provenance": [], "toc_visible": True}},
       "nbformat": 4, "nbformat_minor": 5}
SALIDA.write_text(json.dumps(doc, ensure_ascii=False, indent=1), encoding="utf-8")
print(f"notebook escrito: {SALIDA.name}")
print(f"celdas: {len(celdas)} · preguntas: {len(Q)}")
