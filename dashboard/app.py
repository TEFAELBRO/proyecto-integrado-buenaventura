"""Dashboard del proyecto integrado de Buenaventura.

Seis vistas: ejecutiva, aduanera, portuaria, marítima, predictiva y de calidad.
No calcula nada: lee exclusivamente de data/surface y data/trusted. Si un archivo
falta, la vista lo dice en lugar de mostrar una cifra sin respaldo.

    streamlit run dashboard/app.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pandas as pd
import streamlit as st

RAIZ = Path(__file__).resolve().parents[1]
if str(RAIZ) not in sys.path:
    sys.path.insert(0, str(RAIZ))
S, T, F = RAIZ / "data" / "surface", RAIZ / "data" / "trusted", RAIZ / "reports" / "figures"

st.set_page_config(page_title="Buenaventura — producto integrado", layout="wide")


@st.cache_data(show_spinner=False)
def csv(n):
    p = S / n
    return pd.read_csv(p) if p.exists() else None


@st.cache_data(show_spinner=False)
def parq(n):
    p = T / n
    return pd.read_parquet(p) if p.exists() else None


@st.cache_data(show_spinner=False)
def js(n):
    p = S / n
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else None


def falta(nombre: str, pregunta: str = "") -> None:
    """Avisa de un archivo ausente. La pregunta es opcional y solo enriquece el mensaje."""
    ref = f" (pregunta {pregunta})" if pregunta else ""
    st.info(f"Falta `{nombre}`{ref}. Ejecute `python -m src.correr_integrado`. "
            "El dashboard no estima valores ausentes.")


ficha = js("ficha_calidad.json") or {}
st.title("Buenaventura · producto de datos integrado")
st.caption("Dominios aduanero y portuario. El dominio marítimo está documentado como "
           "no viable con fuentes públicas. El modelo predictivo principal es el aduanero; "
           "el portuario aporta valor descriptivo y explicativo, no predictivo.")

c = st.columns(4)
c[0].metric("Aduanas", (ficha.get("dominios", {}) or {}).get("aduanero", "—").split(",")[0])
c[1].metric("Puerto", (ficha.get("dominios", {}) or {}).get("portuario", "—").split(",")[0])
c[2].metric("Meses integrados", ficha.get("meses_integrados", "—"))
c[3].metric("Preguntas ejecutadas", (ficha.get("preguntas", {}) or {}).get("ejecutada", "—"))

vista = st.sidebar.radio("Vista", ["Ejecutiva", "Aduanera", "Portuaria", "Marítima",
                                   "Predictiva", "Calidad y trazabilidad"])
st.sidebar.divider()
st.sidebar.caption("Las alertas son señales de revisión analítica, no órdenes operativas.")

sa, sp = parq("serie_aduanera_mensual.parquet"), parq("serie_portuaria_mensual.parquet")

if vista == "Ejecutiva":
    st.header("Vista ejecutiva")
    if sa is None or sp is None:
        falta("series de trusted")
    else:
        a, b = st.columns(2)
        with a:
            st.subheader("Aduana 35 · valor CIF")
            st.line_chart(sa.set_index("mes")["cif_usd"])
        with b:
            st.subheader("Zona portuaria · toneladas")
            st.line_chart(sp.set_index("mes")[["toneladas_totales",
                                               "toneladas_comercio_exterior"]])
    for adv in ficha.get("advertencias", []):
        st.warning(adv)

elif vista == "Aduanera":
    st.header("Vista aduanera y comercial")
    if sa is None:
        falta("serie_aduanera_mensual.parquet")
    else:
        ind = st.selectbox("Indicador", ["cif_usd", "peso_neto_kg", "cif_kg"])
        if ind == "cif_kg":
            st.caption("Valor unitario implícito agregado. **No es un precio.**")
        st.line_chart(sa.set_index("mes")[ind])
        e = csv("estacionalidad_aduanera.csv")
        if e is not None:
            st.subheader("Estacionalidad (P21)")
            st.bar_chart(e.set_index("mes_num")["indice_estacional"])

elif vista == "Portuaria":
    st.header("Vista de carga portuaria y sociedades portuarias")
    if sp is None:
        falta("serie_portuaria_mensual.parquet")
    else:
        st.line_chart(sp.set_index("mes")[["ton_importacion", "ton_exportacion",
                                           "ton_transbordo"]])
        st.caption("El transbordo no es comercio exterior: es carga que cambia de buque "
                   "sin entrar ni salir del país.")
        p = csv("participacion_tipo_carga.csv")
        if p is not None:
            st.subheader("Composición por tipo de carga (P24)")
            st.dataframe(p, hide_index=True, use_container_width=True)
        st.subheader("Meses extremos (P29)")
        x = csv("extremos_portuarios.csv")
        if x is None:
            falta("extremos_portuarios.csv", "P29")
        else:
            st.dataframe(x, hide_index=True, use_container_width=True)

    st.divider()
    st.header("Sociedades portuarias")
    st.caption("La fuente identifica la **sociedad portuaria**, no la terminal física ni "
               "el muelle. No se presenta como terminal lo que la fuente no define así.")

    a, b = st.columns([3, 2])
    with a:
        st.subheader("Participación en las toneladas movilizadas (P26)")
        pa = csv("participacion_sociedad_portuaria.csv")
        if pa is None:
            falta("participacion_sociedad_portuaria.csv", "P26")
        else:
            col = pa.columns[1]
            st.bar_chart(pa.set_index("sociedad_portuaria")[col])
            st.dataframe(pa, hide_index=True, use_container_width=True)
    with b:
        st.subheader("Concentración (HHI)")
        hh = csv("hhi_anual_sociedades.csv")
        if hh is None:
            falta("hhi_anual_sociedades.csv", "P26")
        else:
            cc_ = csv("comparacion_concentracion.csv")
            if cc_ is None:
                falta("comparacion_concentracion.csv", "P26")
            else:
                fila = cc_.loc[cc_["dimension"] == "Sociedad portuaria"].iloc[0]
                st.metric("HHI global 2018–2026",
                          f"{int(fila['hhi']):,}".replace(",", "."), fila["clase"],
                          delta_color="inverse")
            st.caption("Umbral de concentración: 2.500")
            st.line_chart(hh.set_index("anio")["hhi"])
            if not bool(hh["periodo_completo"].iloc[-1]):
                st.caption("El último punto corresponde a un año parcial "
                           "(seis meses observados) y no es comparable con los completos.")

    st.subheader("Evolución anual por sociedad portuaria (P28)")
    act = csv("actividad_anual_terminales.csv")
    if act is None:
        falta("actividad_anual_terminales.csv", "P28")
    else:
        largo = act.melt(id_vars="sociedad_portuaria", var_name="anio", value_name="toneladas")
        largo["anio"] = pd.to_numeric(largo["anio"], errors="coerce")
        st.line_chart(largo.dropna().pivot(index="anio", columns="sociedad_portuaria",
                                           values="toneladas"))

    sr = csv("sociedades_sin_reporte_2026.csv")
    if sr is not None and len(sr):
        nombres = ", ".join(sr["sociedad_portuaria"])
        st.warning(
            f"**{len(sr)} sociedades no aparecen reportando en los seis meses observados "
            f"de 2026:** {nombres}.\n\n"
            "La fuente registra **reporte**, no operación. Con estos datos solo puede "
            "afirmarse que no figuran en los reportes de 2026; **no puede afirmarse que "
            "hayan dejado de operar**. Un modelo entrenado sobre el total de la zona "
            "leería esta ausencia como una caída del comercio.")
        st.dataframe(sr[["sociedad_portuaria", "ultimo_anio_con_reporte"]],
                     hide_index=True, use_container_width=True)

    st.subheader("Especialización por tipo de carga (P27)")
    esp = csv("especializacion_terminales.csv")
    if esp is None:
        falta("especializacion_terminales.csv", "P27")
    else:
        tabla_esp = esp.set_index("sociedad_portuaria")
        try:
            # El degradado usa el motor de estilos de pandas, que requiere jinja2. Sin esa
            # dependencia pandas lanza AttributeError, no ImportError: se capturan ambas.
            # Si no está disponible se muestra la tabla sin color en lugar de fallar.
            st.dataframe(tabla_esp.style.format("{:.1f}")
                         .background_gradient(cmap="YlOrBr", axis=None),
                         use_container_width=True)
        except (ImportError, AttributeError):
            st.dataframe(tabla_esp.round(1), use_container_width=True)
        st.caption("Porcentaje de la carga de cada sociedad por tipo. La especialización "
                   "casi total implica que una sociedad no puede absorber sin más la carga "
                   "de otra: la capacidad de respaldo es menor de lo que sugiere el "
                   "reparto agregado.")

    st.subheader("Concentración comparada entre dominios")
    cc = csv("comparacion_concentracion.csv")
    if cc is None:
        falta("comparacion_concentracion.csv")
    else:
        c1, c2, c3 = st.columns(3)
        for col, (_, r) in zip((c1, c2, c3), cc.iterrows(), strict=False):
            col.metric(r["dimension"], f"{int(r['hhi']):,}".replace(",", "."), r["clase"],
                       delta_color="inverse" if r["clase"] == "concentrado" else "normal")
        st.info("Buenaventura importa mercancía variada desde orígenes variados, **pero la "
                "mueve por muy pocas sociedades portuarias**. El riesgo no está en qué se "
                "importa ni de dónde viene, sino en el punto físico por el que pasa. "
                "Ninguna de las dos fuentes por separado permite ver este contraste.")

elif vista == "Marítima":
    st.header("Vista de tráfico marítimo")
    nv = csv("reporte_no_viabilidad.csv")
    if nv is None:
        falta("reporte_no_viabilidad.csv")
    else:
        st.error("Este dominio **no pudo construirse** con fuentes públicas. "
                 "Las ocho preguntas del bloque están cerradas como no viables, con "
                 "evidencia documentada. Es una respuesta válida de la especificación, "
                 "no una omisión.")
        st.dataframe(nv[["pregunta", "tema", "estado"]], hide_index=True,
                     use_container_width=True)
        with st.expander("Razón y qué haría falta"):
            st.write(nv["razon"].iloc[0])
            st.write("**Qué haría falta:** " + nv["que_haria_falta"].iloc[0])

elif vista == "Predictiva":
    st.header("Vista predictiva")
    el = csv("elegibilidad_indicadores.csv")
    if el is not None:
        st.subheader("Qué se puede pronosticar y qué no (P46)")
        st.dataframe(el, hide_index=True, use_container_width=True)
    m = csv("metricas_modelos_portuarios.csv")
    if m is None:
        falta("metricas_modelos_portuarios.csv")
    else:
        st.subheader("Desempeño de modelos y líneas base (P47, P48)")
        st.dataframe(m, hide_index=True, use_container_width=True)
        st.caption("Una diferencia menor al 5 % relativo entre modelos es empate técnico.")
    cb = csv("cobertura_intervalos_portuarios.csv")
    if cb is not None:
        st.subheader("Cobertura de intervalos (P51)")
        st.dataframe(cb, hide_index=True, use_container_width=True)

    st.divider()
    st.header("¿Integrar dominios mejora el pronóstico?")
    ab = csv("ablacion_multidominio.csv")
    if ab is None:
        falta("ablacion_multidominio.csv", "P49")
    else:
        st.error(
            "**No. Añadir variables portuarias empeora el pronóstico del valor CIF.**\n\n"
            "La hipótesis con la que arrancó la versión 5 era que cruzar dominios mejoraría "
            "la predicción. Se midió con una ablación por grupos de variables y el "
            "resultado la refuta.")
        def _w(conjunto):
            """WAPE leído del CSV de ablación; nunca escrito a mano."""
            return float(ab.loc[ab["conjunto"] == conjunto, "wape_pct"].iloc[0])

        base_a = _w("A · historia propia")
        m1, m2, m3 = st.columns(3)
        m1.metric("Historia propia + calendario",
                  f"{_w('B · A + calendario'):.3f} %".replace(".", ","),
                  "mejor", delta_color="normal")
        m2.metric("Integrado completo",
                  f"{_w('E · integrado completo'):.3f} %".replace(".", ","),
                  f"{_w('E · integrado completo') - base_a:+.2f} pp".replace(".", ","),
                  delta_color="inverse")
        m3.metric("Historia propia + PUERTO",
                  f"{_w('C · A + PUERTO'):.3f} %".replace(".", ","),
                  f"{_w('C · A + PUERTO') - base_a:+.2f} pp".replace(".", ","),
                  delta_color="inverse")
        st.caption("WAPE sobre 24 cortes de backtest walk-forward. Menor es mejor.")
        st.bar_chart(ab.set_index("conjunto")["wape_pct"])
        st.dataframe(ab, hide_index=True, use_container_width=True)

        st.success(
            "**Qué significa esto para el producto**\n\n"
            "Ambas fuentes miden el mismo comercio subyacente y comparten el mismo rezago "
            "de publicación, así que el puerto no aporta información que la historia del "
            "propio CIF no contenga ya, y sí consume grados de libertad sobre una muestra "
            "corta.\n\n"
            "**El modelo predictivo principal es el aduanero.** El dominio portuario se "
            "conserva por su valor **descriptivo y explicativo**: responde si un mes cambió "
            "por valor o por volumen físico, y por qué sociedad portuaria pasó la carga. "
            "Presentarlo como una mejora del pronóstico sería afirmar lo contrario de lo "
            "que se midió.")

else:
    st.header("Calidad y trazabilidad")
    tz = csv("matriz_trazabilidad_eda.csv")
    if tz is None:
        falta("matriz_trazabilidad_eda.csv")
    else:
        v = int((tz["estado"] == "ejecutada").sum())
        st.progress(v / 52, text=f"{v} de 52 preguntas ejecutadas · "
                                 f"{int((tz['estado']=='no viable').sum())} no viables · "
                                 f"{int((tz['estado']=='parcial').sum())} parciales")
        f = st.multiselect("Estado", sorted(tz["estado"].unique()),
                           default=sorted(tz["estado"].unique()))
        st.dataframe(tz.loc[tz["estado"].isin(f)], hide_index=True, use_container_width=True)
    a, b = st.columns(2)
    with a:
        st.subheader("Fuentes (P01, P07)")
        cf = csv("catalogo_fuentes.csv")
        if cf is None:
            falta("catalogo_fuentes.csv", "P01")
        else:
            st.dataframe(cf, hide_index=True, use_container_width=True)
    with b:
        st.subheader("Integración (P42, P43)")
        mi = csv("matriz_integracion.csv")
        if mi is None:
            falta("matriz_integracion.csv", "P42")
        else:
            st.dataframe(mi, hide_index=True, use_container_width=True)
    figs = sorted(F.glob("*.png"))
    if figs:
        st.subheader("Figuras")
        cols = st.columns(3)
        for i, x in enumerate(figs):
            cols[i % 3].image(str(x), caption=x.stem, use_container_width=True)
