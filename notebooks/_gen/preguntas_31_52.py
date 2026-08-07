"""Definición de P31 a P52 del EDA V5."""
from preguntas_1_30 import Q, q

# ============================ BLOQUE 5 · BUQUES, FECHAS E ITINERARIOS ============================
_BUSQUEDA = '''ev = pd.DataFrame([
    {"fuente": "DIMAR — estadísticas de tráfico marítimo",
     "url": "dimar.mil.co/operaciones-estadisticas",
     "formato": "PDF trimestral", "serie_tabular": False, "granularidad": "trimestral agregada",
     "resultado": "sin desagregación por evento ni descarga estructurada"},
    {"fuente": "datos.gov.co — catálogo",
     "url": "datos.gov.co/api/catalog/v1?q=arribos+zarpes",
     "formato": "API", "serie_tabular": False, "granularidad": "—",
     "resultado": "0 resultados para arribos y zarpes"},
    {"fuente": "Portal Logístico de Colombia",
     "url": "plc.mintransporte.gov.co", "formato": "tablero web", "serie_tabular": False,
     "granularidad": "agregada", "resultado": "sin exportación histórica por evento"},
    {"fuente": "AIS comercial", "url": "proveedores privados", "formato": "API de pago",
     "serie_tabular": True, "granularidad": "evento",
     "resultado": "sin acceso ni presupuesto; restringe redistribución"},
])
mostrar(ev)

fig, ax = plt.subplots(figsize=(9, 2.6))
ax.axis("off")
ax.text(.5, .55, "NO VIABLE CON FUENTES PÚBLICAS", ha="center", va="center",
        fontsize=15, color="#c62828", weight="bold")
ax.text(.5, .2, "{tema}", ha="center", va="center", fontsize=9, color="#555")
figura(fig, "{id}", "No viabilidad de {slug}", "sin dato")
guardar(ev, "busqueda_{id}")'''

_MOTIVO = ("Se consultaron cuatro vías: DIMAR, el catálogo de datos.gov.co, el Portal "
           "Logístico de Colombia y proveedores comerciales de AIS. Ninguna entrega una "
           "serie histórica tabular con desagregación por evento. DIMAR publica únicamente "
           "boletines trimestrales en PDF.")

_NO_VIABLES = [
    ("P31", "¿Cuántos arribos y zarpes se registran por periodo en Buenaventura?",
     "conteo de arribos y zarpes por periodo", "arribos y zarpes",
     "Sin conteo mensual de recaladas no se puede medir intensidad de tráfico ni cruzarla "
     "con la carga movilizada. Es la pregunta que habría permitido decir si más toneladas "
     "significan más buques o buques más grandes.",
     "Los boletines trimestrales de DIMAR sí traen conteos agregados. Tabularlos daría unas "
     "34 observaciones trimestrales, insuficientes para pronóstico pero útiles como contexto."),
    ("P32", "¿Qué tipos de buque participan y cómo cambia su composición?",
     "composición por tipo de buque", "tipos de buque",
     "El tipo de buque es lo que conectaría el tráfico marítimo con la naturaleza de la "
     "carga: portacontenedores con carga contenerizada, graneleros con granel. Sin ese "
     "dato, la relación entre ambos dominios queda solo en el nivel de toneladas.",
     "Requiere la serie de DIMAR tabulada o acceso AIS."),
    ("P33", "¿Qué banderas, puertos de procedencia, destinos o rutas aparecen con mayor frecuencia?",
     "banderas, procedencias, destinos y rutas", "conectividad maritima",
     "La conectividad marítima habría permitido contrastar los países de origen de la "
     "aduana con las rutas efectivas de los buques, que no tienen por qué coincidir: la "
     "mercancía puede transbordar en un puerto intermedio.",
     "Requiere acceso AIS o registros de capitanía de puerto."),
    ("P34", "¿Qué horarios y días concentran arribos, atraques o zarpes?",
     "patrones horarios y semanales de operación", "patrones horarios",
     "Los patrones horarios son información puramente operativa que ninguna fuente pública "
     "colombiana publica de forma histórica. Era una de las promesas más ambiciosas del "
     "planteamiento y también la menos sustentable.",
     "Requiere datos de sistema de terminal o AIS con marca de tiempo."),
    ("P35", "¿Cuál es la diferencia entre tiempos estimados y reales de llegada o salida?",
     "diferencia entre ETA/ATA y ETD/ATD", "puntualidad ETA ATA",
     "La puntualidad exige tener las dos marcas de tiempo, la estimada y la real, para el "
     "mismo evento. Ninguna fuente pública las publica juntas. Estimar una de ellas "
     "convertiría el indicador en una suposición presentada como medición.",
     "Requiere AIS combinado con itinerarios declarados por las navieras."),
    ("P36", "¿Cuánto tiempo permanecen los buques en fondeo, terminal o puerto?",
     "permanencia en fondeo, terminal y puerto", "permanencia en puerto",
     "La permanencia es el indicador que la gente asocia con congestión portuaria. "
     "Precisamente por eso conviene no estimarlo: presentar una permanencia inventada como "
     "medida de congestión sería el error más grave que este proyecto podría cometer.",
     "Requiere pares de eventos de entrada y salida por buque, disponibles solo en AIS o "
     "en sistemas de terminal."),
    ("P37", "¿Qué buques, rutas o terminales presentan mayores frecuencias o permanencias?",
     "ranking por frecuencia y permanencia", "ranking de buques y rutas",
     "Depende por completo de P31 y P36. Sin identificador estable de buque no hay ranking "
     "posible.",
     "Requiere identificador IMO o MMSI con historia."),
    ("P38", "¿Qué calidad y cobertura tienen los identificadores, fechas e itinerarios?",
     "calidad de identificadores y campos temporales", "calidad de identificadores",
     "Esta pregunta existe para decidir si el análisis operativo es defendible. La respuesta "
     "es que no lo es, porque no hay identificadores que auditar. Responderla honestamente "
     "es lo que impide construir el resto del bloque sobre datos que no existen.",
     "Requiere que exista primero alguna de las fuentes de P31 a P37."),
]

for _id, _tit, _tema, _slug, _expl, _futuro in _NO_VIABLES:
    q(_id, _tit, "no viable por ausencia de fuente",
      _BUSQUEDA.replace("{id}", _id).replace("{tema}", _tema).replace("{slug}", _slug),
      f"NO VIABLE. No existe fuente pública con serie histórica para {_tema}. " + _MOTIVO,
      _expl,
      f"Fuente necesaria para una fase futura: {_futuro}",
      "Búsqueda propia del 6 de agosto de 2026 en DIMAR, datos.gov.co, Portal Logístico y "
      "proveedores AIS")

# ============================ BLOQUE 6 · CONTEXTO E INTEGRACIÓN ============================
q("P39", "¿Qué relación temporal existe entre TRM, CIF, peso, toneladas, TEU y arribos?",
  "ejecutada parcialmente",
'''j = integrado.merge(ext_m, on="mes", how="left")
pares = [("cif_usd", "trm_cop_usd"), ("toneladas_totales", "trm_cop_usd"),
         ("toneladas_totales", "oni_anomalia")]
filas = []
for a, b in pares:
    da, db = j[a].diff(), j[b].diff()
    for k in range(7):
        m = da.notna() & db.shift(k).notna()
        n = int(m.sum())
        r = float(np.corrcoef(da[m], db.shift(k)[m])[0, 1]) if n > 2 else np.nan
        banda = 1.96 / np.sqrt(n) if n > 2 else np.nan
        filas.append({"par": f"{a}~{b}", "lag": k, "correlacion": round(r, 4), "n": n,
                      "significativa": bool(abs(r) > banda) if n > 2 else None,
                      "usable_sin_fuga": k >= 1})
cc = pd.DataFrame(filas)
mostrar(cc.head(21))

fig, ax = plt.subplots(figsize=(10, 3.4))
for par, s in cc.groupby("par"):
    ax.plot(s["lag"], s["correlacion"], marker="o", ms=4, label=par)
ax.axhline(0, color="grey", lw=.8)
ax.axvspan(-.4, .4, color="crimson", alpha=.12)
ax.set_xlabel("rezago (meses)"); ax.set_ylabel("correlación en diferencias")
ax.legend(fontsize=7)
figura(fig, "P39", "Correlacion cruzada entre dominios y variables externas", "coeficiente")
guardar(cc, "correlaciones_integradas")''',
  "Las correlaciones entre la TRM y los indicadores de ambos dominios son débiles en todos "
  "los rezagos usables. La franja roja marca el rezago 0, que no puede usarse sin fuga.",
  "El resultado negativo es útil: descarta la TRM como señal predictiva fuerte y evita "
  "cargar el modelo con una variable que no aporta. En la versión anterior del proyecto la "
  "ablación llegó a la misma conclusión por otra vía, lo cual refuerza el hallazgo.",
  "TEU y arribos no entran en el análisis porque no existen como dato. La pregunta se "
  "responde solo en la parte que las fuentes permiten.",
  "Banco de la República, NOAA y las dos fuentes integradas; cálculo propio sobre series "
  "diferenciadas")

q("P40", "¿Qué condiciones meteorológicas o meteomarinas coinciden con cambios en arribos, tiempos o carga?",
  "no viable por ausencia de fuente",
'''met = pd.DataFrame([
    {"fuente": "IDEAM", "variable": "precipitación y viento",
     "evaluada": True, "integrada": False,
     "motivo": "requiere selección de estación y validación de cobertura no realizada"},
    {"fuente": "DIMAR — meteomarina", "variable": "oleaje y marea",
     "evaluada": True, "integrada": False, "motivo": "sin serie histórica descargable"},
    {"fuente": "NOAA ONI", "variable": "anomalía oceánica",
     "evaluada": True, "integrada": True, "motivo": "integrada como contexto en P39"},
])
mostrar(met)
guardar(met, "fuentes_meteomarinas")''',
  "PARCIAL. Solo el ONI quedó integrado, como variable de contexto. Las fuentes de oleaje, "
  "viento y marea no se integraron.",
  "La variable meteomarina tendría sentido si existiera el dominio operativo: la lógica "
  "sería que el oleaje afecta los tiempos de atraque. Sin arribos ni permanencias, no hay "
  "contra qué cruzarla, y cruzarla contra toneladas mensuales agregadas sería un ejercicio "
  "sin interpretación clara.",
  "IDEAM publica datos por estación; seleccionar la estación representativa de la bahía y "
  "validar su cobertura es trabajo de una fase futura.",
  "IDEAM, DIMAR y NOAA; evaluación propia")

q("P41", "¿Qué eventos externos verificables coinciden con cambios estructurales o extremos?",
  "ejecutada",
'''eventos = pd.DataFrame([
    {"evento": "Pandemia de COVID-19", "inicio": "2020-03", "fin": "2020-06",
     "dominio": "ambos", "fuente": "PENDIENTE DE VERIFICAR Y FECHAR"},
    {"evento": "Paro nacional y bloqueos viales", "inicio": "2021-04", "fin": "2021-06",
     "dominio": "ambos", "fuente": "PENDIENTE DE VERIFICAR Y FECHAR"},
    {"evento": "Crisis global de fletes marítimos", "inicio": "2021-01", "fin": "2022-12",
     "dominio": "aduanero", "fuente": "PENDIENTE DE VERIFICAR Y FECHAR"},
])
mostrar(eventos)

fig, ax = plt.subplots(2, 1, figsize=(11, 6), sharex=True)
ax[0].plot(sa["mes"], sa["cif_usd"] / 1e9, lw=1, color="#31708e")
ax[0].set_ylabel("CIF (mil M USD)")
ax[1].plot(sp["mes"], sp["toneladas_totales"] / 1e6, lw=1, color="#6a8f3d")
ax[1].set_ylabel("toneladas (M)")
for _, e in eventos.iterrows():
    for a in ax:
        a.axvspan(pd.Timestamp(e["inicio"]), pd.Timestamp(e["fin"]), alpha=.15, color="orange")
figura(fig, "P41", "Series anotadas con eventos externos", "mil M USD y M toneladas")
guardar(eventos, "catalogo_eventos")''',
  "Tres eventos catalogados con su rango de fechas y anotados sobre ambas series. Las "
  "fuentes están marcadas como pendientes de verificar.",
  "El catálogo documenta coincidencia temporal, no causalidad. Anotar la pandemia sobre la "
  "serie no demuestra que la pandemia causó la caída: demuestra que ocurrieron a la vez, y "
  "deja al lector decidir. Marcar las fuentes como pendientes es preferible a citar de "
  "memoria una referencia que después no se sostiene.",
  "Las tres fuentes deben verificarse y fecharse antes de la entrega final para cumplir APA.",
  "Elaboración propia; fuentes pendientes de verificación")

q("P42", "¿Qué relaciones entre fuentes pueden construirse de forma directa, agregada o solo contextual?",
  "ejecutada",
'''rel = pd.DataFrame([
    {"origen": "DANE IMPO", "destino": "Supertransporte", "llave": "mes calendario",
     "tipo": "AGREGADA", "cardinalidad": "1:1 tras agregar", "riesgo_duplicacion": "nulo"},
    {"origen": "DANE IMPO", "destino": "TRM", "llave": "mes calendario",
     "tipo": "AGREGADA", "cardinalidad": "1:1", "riesgo_duplicacion": "nulo"},
    {"origen": "DANE IMPO", "destino": "ONI", "llave": "mes calendario",
     "tipo": "CONTEXTUAL", "cardinalidad": "1:1", "riesgo_duplicacion": "nulo"},
    {"origen": "DANE IMPO", "destino": "eventos", "llave": "rango de fechas",
     "tipo": "CONTEXTUAL", "cardinalidad": "1:N", "riesgo_duplicacion": "nulo"},
    {"origen": "declaración", "destino": "buque o terminal", "llave": "NO EXISTE",
     "tipo": "NO VIABLE", "cardinalidad": "—", "riesgo_duplicacion": "—"},
])
mostrar(rel)

fig, ax = plt.subplots(figsize=(9, 3.2))
ax.axis("off")
cajas = {"DANE IMPO": (.08, .5), "Supertransporte": (.5, .5), "TRM / ONI": (.5, .85),
         "Eventos": (.5, .15), "Buque / terminal": (.88, .5)}
for t, (x, y) in cajas.items():
    color = "#c62828" if "Buque" in t else "#31708e"
    ax.text(x, y, t, ha="center", va="center", fontsize=8, color="white",
            bbox=dict(boxstyle="round,pad=0.4", fc=color, ec="none"))
ax.annotate("", xy=(.42, .5), xytext=(.17, .5), arrowprops=dict(arrowstyle="->", lw=1.6))
ax.text(.29, .55, "agregada\\npor mes", ha="center", fontsize=7)
ax.annotate("", xy=(.5, .78), xytext=(.5, .58), arrowprops=dict(arrowstyle="->", lw=1.2, ls=":"))
ax.annotate("", xy=(.5, .22), xytext=(.5, .42), arrowprops=dict(arrowstyle="->", lw=1.2, ls=":"))
ax.annotate("", xy=(.79, .5), xytext=(.60, .5),
            arrowprops=dict(arrowstyle="->", lw=1.6, color="#c62828", ls="--"))
ax.text(.70, .56, "SIN LLAVE", ha="center", fontsize=7, color="#c62828", weight="bold")
figura(fig, "P42", "Diagrama de integracion entre dominios", "relaciones")
guardar(rel, "matriz_integracion")''',
  "Ninguna relación es directa. La aduanera-portuaria es agregada por mes; TRM, ONI y "
  "eventos son contextuales; el vínculo entre declaración y buque o terminal es NO VIABLE "
  "por ausencia de llave.",
  "Esta es la pregunta que protege al proyecto de su error más probable. Sería tentador "
  "afirmar que las importaciones de un mes llegaron en tales buques o por tal terminal. No "
  "hay ninguna llave pública que lo permita, y construirla por inferencia produciría "
  "correspondencias falsas presentadas con apariencia de dato.",
  "Una llave a nivel de evento existiría si la DIAN publicara el manifiesto de carga con "
  "identificador de buque, lo que no ocurre.",
  "Elaboración propia a partir del esquema de ambas fuentes")

q("P43", "¿Qué porcentaje de registros o periodos queda vinculado en cada integración?",
  "ejecutada",
'''ma, mp = set(sa["mes"]), set(sp["mes"])
com = ma & mp
emb = pd.DataFrame([
    {"etapa": "meses aduaneros", "n": len(ma)},
    {"etapa": "meses portuarios", "n": len(mp)},
    {"etapa": "meses vinculados", "n": len(com)},
    {"etapa": "solo aduanas", "n": len(ma - mp)},
    {"etapa": "solo puerto", "n": len(mp - ma)},
])
mostrar(emb)

fig, ax = plt.subplots(figsize=(8, 3))
ax.barh(emb["etapa"][::-1], emb["n"][::-1],
        color=["#a5673f", "#a5673f", "#2e7d32", "#31708e", "#6a8f3d"][::-1])
ax.set_xlabel("número de meses")
figura(fig, "P43", "Embudo de integracion entre dominios", "meses")
print(f"periodo común: {min(com):%Y-%m} a {max(com):%Y-%m}")
print(f"cobertura del dominio portuario: {len(com)/len(mp)*100:.1f} %")
guardar(emb, "embudo_integracion")''',
  "101 meses vinculados de 173 aduaneros y 102 portuarios. El periodo común es 2018-01 a "
  "2026-05, es decir el 99 % del dominio portuario y el 58 % del aduanero.",
  "El único mes portuario que no se vincula es junio de 2026, porque la aduana todavía no "
  "lo publicó. Ese detalle es la evidencia empírica de que el puerto va por delante en el "
  "calendario de publicación, y anticipa la respuesta de P44.",
  "La vinculación es de periodos, no de registros: no existe integración a nivel de evento.",
  "Cálculo propio sobre ambas series")

q("P44", "¿Los desfases de publicación y frecuencia introducen sesgos al comparar las fuentes?",
  "ejecutada",
'''disp = pd.DataFrame([
    {"fuente": "DANE IMPO", "ultimo_mes": "2026-05", "rezago_dias": 45,
     "disponible_al_predecir_mes_siguiente": False},
    {"fuente": "Supertransporte", "ultimo_mes": "2026-06", "rezago_dias": 60,
     "disponible_al_predecir_mes_siguiente": False},
    {"fuente": "TRM", "ultimo_mes": "2026-06", "rezago_dias": 0,
     "disponible_al_predecir_mes_siguiente": True},
    {"fuente": "ONI", "ultimo_mes": "2026-06", "rezago_dias": 15,
     "disponible_al_predecir_mes_siguiente": True},
])
mostrar(disp)

fig, ax = plt.subplots(figsize=(9, 2.8))
col = ["#2e7d32" if d else "#c62828" for d in disp["disponible_al_predecir_mes_siguiente"]]
ax.barh(disp["fuente"], disp["rezago_dias"], color=col)
ax.set_xlabel("rezago de publicación (días)")
figura(fig, "P44", "Rezago de publicacion por fuente", "días")
guardar(disp, "calendario_disponibilidad")''',
  "El puerto llega a junio de 2026 y la aduana a mayo. Sin embargo, **ninguna de las dos "
  "está disponible para predecir el mes en curso**: ambas publican con rezago superior a un "
  "mes.",
  "Aquí está el hallazgo que impide un atajo tentador. Como el puerto publica antes, se "
  "podría pensar en usarlo como predictor adelantado del CIF. No funciona: al momento de "
  "pronosticar el CIF de un mes, tampoco existe el dato portuario de ese mes. El desfase "
  "entre ambas es de un mes, pero el rezago de ambas frente al presente es mayor. Ignorar "
  "esto produciría fuga operacional, que es el error que la línea base del proyecto "
  "identificó como el más peligroso.",
  "Los rezagos declarados son los plazos normativos; el rezago observado puede variar.",
  "DANE, Superintendencia de Transporte, Banco de la República y NOAA")

q("P45", "¿Qué indicadores integrados aportan información adicional frente a revisar cada fuente por separado?",
  "ejecutada",
'''val = pd.DataFrame([
    {"pregunta_del_usuario": "¿Subió el comercio o subieron los precios?",
     "con_una_fuente": "no distinguible", "con_la_vista_integrada": "sí: CIF vs toneladas",
     "aporta": True},
    {"pregunta_del_usuario": "¿El aumento de valor vino con más carga física?",
     "con_una_fuente": "no", "con_la_vista_integrada": "sí", "aporta": True},
    {"pregunta_del_usuario": "¿Qué terminal absorbió el cambio?",
     "con_una_fuente": "solo puerto", "con_la_vista_integrada": "sí, por sociedad portuaria",
     "aporta": True},
    {"pregunta_del_usuario": "¿Qué buque trajo esa mercancía?",
     "con_una_fuente": "no", "con_la_vista_integrada": "NO: sin llave verificable",
     "aporta": False},
])
mostrar(val)

j = integrado.copy()
j["cif_base100"] = j["cif_usd"] / j["cif_usd"].iloc[0] * 100
j["ton_base100"] = j["toneladas_totales"] / j["toneladas_totales"].iloc[0] * 100
fig, ax = plt.subplots(figsize=(11, 3.6))
ax.plot(j["mes"], j["cif_base100"], lw=1.3, label="valor CIF (aduana)")
ax.plot(j["mes"], j["ton_base100"], lw=1.3, label="toneladas movilizadas (puerto)")
ax.set_ylabel("índice base 100 = 2018-01"); ax.legend(fontsize=7)
figura(fig, "P45", "Valor economico frente a volumen fisico", "índice base 100")
guardar(val, "valor_incremental")''',
  "Tres de cuatro preguntas del usuario solo se responden con la vista integrada. La cuarta "
  "sigue sin respuesta porque exigiría una llave que no existe.",
  "La figura es el argumento central del proyecto integrado: el valor económico y el "
  "volumen físico se separan visiblemente a partir de cierto punto. Con una sola fuente ese "
  "hecho es invisible. Esa separación es la respuesta operativa a la pregunta de si un mes "
  "cambió por precio o por cantidad, y es lo que justifica el costo de integrar dos "
  "dominios en vez de quedarse con uno.",
  "El valor incremental está argumentado sobre casos de uso, no medido con usuarios reales.",
  "Cálculo propio sobre la vista integrada")

# ============================ BLOQUE 7 · PRONÓSTICO, ALERTAS Y PRODUCTO ============================
q("P46", "¿Qué indicadores tienen calidad, historia, frecuencia y utilidad suficientes para ser pronosticados?",
  "ejecutada",
'''eleg = pd.DataFrame([
    {"indicador": "cif_usd", "dominio": "aduanero", "n_obs": len(sa), "continuidad": "completa",
     "rezago_dias": 45, "elegible": True},
    {"indicador": "peso_neto_kg", "dominio": "aduanero", "n_obs": len(sa),
     "continuidad": "completa", "rezago_dias": 45, "elegible": True},
    {"indicador": "toneladas_totales", "dominio": "portuario", "n_obs": len(sp),
     "continuidad": "completa", "rezago_dias": 60, "elegible": True},
    {"indicador": "ton_contenerizada", "dominio": "portuario", "n_obs": len(sp),
     "continuidad": "completa", "rezago_dias": 60, "elegible": True},
    {"indicador": "TEU", "dominio": "portuario", "n_obs": 0, "continuidad": "—",
     "rezago_dias": None, "elegible": False},
    {"indicador": "arribos", "dominio": "marítimo", "n_obs": 0, "continuidad": "—",
     "rezago_dias": None, "elegible": False},
    {"indicador": "permanencia_media", "dominio": "operacional", "n_obs": 0,
     "continuidad": "—", "rezago_dias": None, "elegible": False},
])
mostrar(eleg)

fig, ax = plt.subplots(figsize=(9, 3.2))
col = ["#2e7d32" if e else "#c62828" for e in eleg["elegible"]]
ax.barh(eleg["indicador"][::-1], eleg["n_obs"][::-1], color=col[::-1])
ax.axvline(36, ls="--", color="grey")
ax.text(37, .2, "mínimo para backtest", fontsize=7, color="grey")
ax.set_xlabel("observaciones mensuales disponibles")
figura(fig, "P46", "Elegibilidad de indicadores para pronostico", "número de observaciones")
guardar(eleg, "elegibilidad_indicadores")''',
  "Cuatro indicadores elegibles de siete evaluados. Los tres descartados no tienen ni una "
  "sola observación porque su fuente no existe.",
  "La regla se aplica antes de modelar, no después de ver los resultados. Un indicador sin "
  "historia suficiente no se pronostica aunque el usuario lo pida: se describe. Fijar el "
  "umbral en 36 observaciones antes de mirar los datos evita el sesgo de acomodar el "
  "criterio al indicador que uno quería incluir.",
  "La utilidad para el usuario se evaluó por razonamiento, no con usuarios reales.",
  "Elaboración propia sobre las series construidas")

q("P47", "¿Qué desempeño obtienen Naive 1, Naive estacional y drift para cada indicador seleccionado?",
  "ejecutada",
'''base = backtest_lineas_base(sp, ["toneladas_totales", "ton_contenerizada"], n_cortes=24)
mostrar(base)

fig, ax = plt.subplots(figsize=(9, 3.2))
piv = base.pivot(index="modelo", columns="objetivo", values="wape_pct")
piv.plot(kind="bar", ax=ax, color=["#31708e", "#a5673f"])
ax.set_ylabel("WAPE (%)"); ax.set_xlabel("")
plt.xticks(rotation=0)
figura(fig, "P47", "Desempeno de las lineas base por indicador", "WAPE en porcentaje")
guardar(base, "lineas_base_portuarias")''',
  "Para toneladas totales, Naive 1 obtiene 9,17 % de WAPE y Naive 12 llega a 12,84 %. Para "
  "carga contenerizada, Naive 1 obtiene 8,55 %.",
  "Las tres líneas base se reportan siempre, no solo la estacional. En la versión anterior "
  "del proyecto se reportaba únicamente Naive 12, y eso hacía parecer que el modelo mejoraba "
  "un 55 % cuando frente a Naive 1 la mejora real era del 8 %. La línea base más exigente "
  "es la que define si el modelo aporta algo.",
  "Con 24 cortes, las diferencias menores a un punto porcentual deben leerse con cautela.",
  "Cálculo propio, backtest walk-forward de un paso")

q("P48", "¿Qué modelos logran mejor estabilidad fuera de muestra sin fuga?",
  "ejecutada",
'''met = pd.read_csv(RUTA_METRICAS) if RUTA_METRICAS.exists() else metricas_portuarias
mostrar(met[met.ventana == 24][["objetivo", "modelo", "wape_pct", "mase_12"]].round(3))

fig, ax = plt.subplots(1, 2, figsize=(12, 3.4))
for i, obj in enumerate(["toneladas_totales", "ton_contenerizada"]):
    s = met[(met.ventana == 24) & (met.objetivo == obj)].sort_values("wape_pct")
    col = ["#2e7d32" if m not in ("naive_1", "naive_12", "drift") else "#9e9e9e"
           for m in s["modelo"]]
    ax[i].barh(s["modelo"][::-1], s["wape_pct"][::-1], color=col[::-1])
    ax[i].set_title(obj, fontsize=9); ax[i].set_xlabel("WAPE (%)")
figura(fig, "P48", "Comparacion de modelos frente a lineas base", "WAPE en porcentaje")
guardar(met, "metricas_modelos_portuarios")''',
  "Para toneladas totales, Ridge obtiene 6,61 % contra 9,17 % de Naive 1: una mejora real "
  "del 28 %. Para carga contenerizada, **Naive 1 gana con 8,55 % y Ridge queda en 9,45 %**: "
  "el modelo es peor que repetir el último valor observado.",
  "Este resultado dividido es el más valioso del bloque. Un indicador se puede pronosticar "
  "y el otro no, y ambos vienen de la misma fuente y el mismo pipeline. Reportar solo el "
  "caso exitoso habría sido más cómodo y menos cierto. Para la carga contenerizada la "
  "recomendación es usar Naive 1 y presentar el indicador de forma descriptiva.",
  "Sin auditoría de fuga en verde ninguna de estas métricas sería publicable; la auditoría "
  "se ejecuta en el pipeline antes de calcularlas.",
  "Cálculo propio, backtest walk-forward con escalado dentro de cada corte")

q("P49", "¿Qué variables aportan valor incremental al pronóstico?",
  "ejecutada parcialmente",
'''abl = pd.DataFrame([
    {"conjunto": "solo rezagos", "dominio": "historia propia", "n_variables": 4},
    {"conjunto": "rezagos + calendario", "dominio": "historia + calendario", "n_variables": 10},
    {"conjunto": "rezagos + medias móviles", "dominio": "historia propia", "n_variables": 8},
    {"conjunto": "completo", "dominio": "todo", "n_variables": 14},
])
mostrar(abl)
print("Resultado heredado del pipeline aduanero de la línea base:")
print("  el modelo completo (6,40 %) resultó PEOR que rezagos + calendario (5,55 %)")
print("  la TRM empeoró el resultado y el ONI no aportó nada")
guardar(abl, "ablacion_conjuntos")''',
  "PARCIAL. La ablación por dominio (aduanero, portuario, marítimo, contexto) no se ejecutó. "
  "Se dispone del resultado del pipeline aduanero: el modelo completo resultó peor que uno "
  "con la mitad de variables, y ni la TRM ni el ONI aportaron.",
  "Que más variables empeoren el resultado es contraintuitivo y por eso hay que medirlo. "
  "Con series cortas, cada variable adicional consume grados de libertad y añade ruido. La "
  "ablación es lo que convierte 'agregamos TRM porque tiene sentido económico' en una "
  "decisión con evidencia a favor o en contra.",
  "La ablación multidominio es la tarea pendiente que más directamente justificaría la "
  "integración: falta medir si las variables portuarias mejoran el pronóstico aduanero.",
  "Cálculo propio; resultado aduanero de la línea base V4")

q("P50", "¿Los modelos presentan sesgo, errores extremos o degradación por régimen?",
  "ejecutada",
'''diag = met[met.ventana == 24][["objetivo", "modelo", "wape_pct", "sesgo_rel_pct",
                                "error_maximo"]].round(3)
mostrar(diag)

fig, ax = plt.subplots(figsize=(9, 3.2))
s = diag[diag.modelo == "ridge"]
ax.barh(s["objetivo"], s["sesgo_rel_pct"], color=["#31708e", "#a5673f"])
ax.axvline(0, color="grey", lw=.8)
ax.set_xlabel("sesgo relativo (%)  ·  positivo = el modelo subestima")
figura(fig, "P50", "Sesgo relativo por indicador", "porcentaje")
guardar(diag, "diagnostico_residuos")''',
  "Se reporta sesgo relativo y error máximo por indicador y modelo. Un sesgo positivo "
  "significa que el modelo subestima de forma sistemática.",
  "El sesgo importa más que el error promedio para un producto operativo. Un modelo que se "
  "equivoca poco pero siempre hacia el mismo lado induce decisiones consistentemente "
  "sesgadas, y eso es peor que un error mayor pero simétrico. El error máximo cumple otra "
  "función: un promedio aceptable puede esconder un mes catastrófico.",
  "La degradación por régimen requiere más historia posterior al cambio de nivel de 2025.",
  "Cálculo propio sobre los residuos del backtest")

q("P51", "¿Los intervalos alcanzan la cobertura nominal y mantienen un ancho útil?",
  "ejecutada",
'''cob = cobertura_intervalos_tabla
mostrar(cob)

fig, ax = plt.subplots(figsize=(9, 3.2))
ax.barh(cob["caso"], cob["cobertura_empirica"] * 100, color="#31708e")
ax.axvline(80, ls="--", color="crimson", lw=1.6)
ax.text(81, -.4, "nominal 80 %", fontsize=7, color="crimson")
ax.set_xlabel("cobertura empírica (%)")
figura(fig, "P51", "Cobertura empirica frente al nivel nominal", "porcentaje")
guardar(cob, "cobertura_intervalos")''',
  "Los intervalos se construyen con cuantiles empíricos de los errores fuera de muestra y "
  "calibración expansiva. La cobertura se mide, no se declara.",
  "La regla que este bloque hace cumplir es que un intervalo nunca se deriva del WAPE ni de "
  "ninguna métrica de error puntual, que es exactamente lo que hacía la versión anterior del "
  "proyecto. Si la cobertura medida no alcanza el nivel declarado, el intervalo se recalibra "
  "o se renombra según lo que realmente cubre. Con pocos cortes evaluables, la incertidumbre "
  "sobre la propia cobertura es alta y eso también se declara.",
  "Con menos de veinte cortes evaluables el intervalo de confianza de la cobertura es "
  "demasiado ancho para concluir.",
  "Cálculo propio, calibración conformal expansiva")

q("P52", "¿Cómo debe transformar el dashboard los indicadores en señales normales, de seguimiento o de alerta?",
  "ejecutada",
'''matriz = pd.DataFrame([
    {"nivel": "normal", "criterio": "dentro del comportamiento histórico esperado",
     "accion": "seguimiento de rutina del informe mensual"},
    {"nivel": "seguimiento", "criterio": "variación relevante dentro del rango histórico",
     "accion": "revisar composición por país, capítulo o tipo de carga"},
    {"nivel": "alerta", "criterio": "desviación fuera del umbral o fuera del intervalo",
     "accion": "revisión dirigida y verificación de la fuente"},
])
mostrar(matriz)

fig, ax = plt.subplots(figsize=(9, 2.6))
ax.axis("off")
for i, (c, n, t) in enumerate([("#2e7d32", "NORMAL", "rutina"),
                               ("#ef6c00", "SEGUIMIENTO", "revisar composición"),
                               ("#c62828", "ALERTA", "revisión dirigida")]):
    ax.add_patch(plt.Rectangle((i * .34, .3), .3, .4, fc=c, alpha=.85))
    ax.text(i * .34 + .15, .55, n, ha="center", color="white", fontsize=10, weight="bold")
    ax.text(i * .34 + .15, .4, t, ha="center", color="white", fontsize=7)
ax.set_xlim(0, 1); ax.set_ylim(0, 1)
figura(fig, "P52", "Matriz de decision de la senal de alerta", "niveles")
guardar(matriz, "matriz_decision")''',
  "Tres niveles con criterio y acción sugerida. Los umbrales se calibran sobre la variación "
  "interanual y únicamente con la ventana de entrenamiento.",
  "Hay una decisión de diseño detrás que vale explicar. La primera versión de estas reglas "
  "comparaba el pronóstico contra la mediana histórica del nivel. En una serie con "
  "tendencia, eso hace que todo mes reciente quede en el percentil 100 y la alerta se "
  "dispare siempre. Una alerta que suena siempre no informa nada. Por eso el estadístico se "
  "calcula sobre la variación interanual, que sí es estacionaria.",
  "Cada alerta explica su razón y no constituye una orden operativa. Los umbrales no han "
  "sido validados con un usuario real.",
  "Elaboración propia, calibrada solo con la ventana de entrenamiento")


# --------------------------------------------------------------------------------------
# Guarda de degradación: P26 y P27 dependen de la columna `sociedad_portuaria`, que solo
# llega si el cuaderno pudo descargar de la API. Sin conexión, el respaldo local no la
# trae y un HHI calculado sobre una única categoría daría 10.000, es decir "concentrado".
# Ese número sería falso: no mide concentración, mide que no hay desagregación. Se
# antepone una comprobación que detiene el cálculo y lo declara.
# --------------------------------------------------------------------------------------
_GUARDA = """
DESAGREGADO = pt["sociedad_portuaria"].nunique() > 1
if not DESAGREGADO:
    print("MODO DEGRADADO: el cuaderno no pudo descargar la desagregación por sociedad")
    print("portuaria y está usando el respaldo local, que solo trae tipo de carga.")
    print("Esta pregunta NO se responde con datos agregados: un HHI sobre una sola")
    print("categoria daria 10.000 por construccion, y eso no mide concentracion.")
    print("\\nEjecute el cuaderno con conexion a internet para responderla.")
else:
"""

def _indentar(codigo: str) -> str:
    return "\n".join(("    " + l) if l.strip() else l for l in codigo.split("\n"))

for _p in ("P26", "P27"):
    Q[_p]["codigo"] = _GUARDA + _indentar(Q[_p]["codigo"])
    Q[_p]["limitacion"] = (
        "Requiere conexión a internet para descargar la desagregación por sociedad "
        "portuaria. Sin ella el cuaderno lo declara y no calcula, en lugar de producir "
        "un indicador falso. " + Q[_p]["limitacion"])


# ======================================================================================
# P26, P27 y P28 reimplementadas con la desagregación real por sociedad portuaria,
# descargada el 2026-08-06 con dos consultas adicionales a la misma API.
# ======================================================================================
q("P26", "¿Qué sociedades portuarias concentran carga, contenedores o tipos de tráfico?",
  "ejecutada",
"""ta = pd.read_csv(RUTA_TERMINALES_ANIO)
ta["ton"] = ta[["sum_importacion", "sum_exportacion", "sum_transbordo"]].sum(axis=1)

tot = ta.groupby("sociedad_portuaria")["ton"].sum().sort_values(ascending=False)
# El HHI se calcula sobre las participaciones SIN redondear: redondear a dos decimales
# antes de elevar al cuadrado desplaza el índice (3.515 en vez de 3.514).
part_exacta = tot / tot.sum() * 100
hhi = float((part_exacta ** 2).sum())
part = part_exacta.round(2)
mostrar(part.rename("participacion_pct").reset_index())

hhi_anio = []
for y, g in ta.groupby("anno_vigencia"):
    p_ = g.groupby("sociedad_portuaria")["ton"].sum()
    p_ = p_ / p_.sum() * 100
    hhi_anio.append({"anio": int(y), "hhi": round(float((p_ ** 2).sum())),
                     "sociedades_que_reportan": int((p_ > 0).sum()),
                     "anio_completo": int(y) < 2026})
hhi_anio = pd.DataFrame(hhi_anio)

fig, ax = plt.subplots(1, 2, figsize=(12, 3.6))
ax[0].barh([s[:34] for s in part.index][::-1], part.values[::-1], color="#31708e")
ax[0].set_xlabel("% de toneladas 2018-2026")
ax[0].set_title(f"Participacion  ·  HHI global {hhi:,.0f}", fontsize=9)
ax[1].plot(hhi_anio["anio"], hhi_anio["hhi"], marker="o", color="#a5673f")
ax[1].axhline(2500, ls="--", color="crimson")
ax[1].text(2018.1, 2560, "umbral de concentracion", fontsize=6.5, color="crimson")
ax[1].set_ylabel("HHI"); ax[1].set_xlabel("año")
ax[1].set_title("Evolucion de la concentracion", fontsize=9)
figura(fig, "P26", "Concentracion por sociedad portuaria", "porcentaje e indice HHI")

print(f"HHI global: {hhi:,.0f} -> CONCENTRADO (umbral 2.500)")
print(hhi_anio.to_string(index=False))
guardar(part.reset_index(), "participacion_sociedad_portuaria")
guardar(hhi_anio, "hhi_anual_terminales")""",
  "El HHI por sociedad portuaria es **3.514** en el periodo 2018–2026. La Sociedad Portuaria "
  "Regional de Buenaventura moviliza el 51,4 % de las toneladas, Aguadulce el 25,3 % y "
  "TCBUEN el 13,7 %. El índice supera el umbral de 2.500 que suele usarse para calificar un "
  "reparto como concentrado. Entre los **años completos** bajó de 4.722 en 2018 a 2.988 en "
  "2023 y subió a 3.740 en 2025. El valor de 2026 (4.217) **no es comparable**: cubre seis "
  "meses y solo tres sociedades reportan. Recalculando 2025 con esas mismas tres, el HHI "
  "sería 4.096, de modo que la mayor parte del salto se explica por el cambio de cobertura "
  "del reporte y no por una redistribución entre las que siguen.",
  "El contraste con el dominio aduanero es lo que aporta la integración. La canasta de "
  "productos tiene un HHI de 434 y la de orígenes 1.351: ambas desconcentradas. La "
  "movilización, con 3.514, está unas ocho veces más concentrada que la de capítulos "
  "arancelarios. Buenaventura importa mercancía variada desde orígenes variados y la "
  "moviliza a través de pocas sociedades portuarias. Ninguna de las dos fuentes por "
  "separado permite observar ese contraste.",
  "El HHI mide reparto de toneladas reportadas, **no capacidad instalada, utilización ni "
  "posibilidad real de sustitución**: un índice alto no permite concluir por sí solo que "
  "exista un riesgo operativo. El dato de 2026 cubre seis meses y tres sociedades, y no es "
  "comparable con los años completos. La fuente identifica la razón social que reporta, que "
  "puede administrar una o varias instalaciones: no se puede descender a la instalación "
  "física ni al muelle.",
  "Superintendencia de Transporte (2026), consulta agregada por año y sociedad portuaria")

q("P27", "¿Qué sociedades portuarias se especializan en determinados tipos de carga?",
  "ejecutada",
"""tc = pd.read_csv(RUTA_TERMINALES_TIPO)
tc["ton"] = tc[["sum_importacion", "sum_exportacion", "sum_transbordo"]].sum(axis=1)
piv = tc.pivot_table(index="sociedad_portuaria", columns="tipo_carga",
                     values="ton", aggfunc="sum", fill_value=0)
perfil = (piv.div(piv.sum(axis=1), axis=0) * 100).round(1)
mostrar(perfil.reset_index())

fig, ax = plt.subplots(figsize=(9.5, 3.4))
im = ax.imshow(perfil.values, aspect="auto", cmap="YlOrBr", vmin=0, vmax=100)
ax.set_xticks(range(len(perfil.columns)))
ax.set_xticklabels([c[:18] for c in perfil.columns], rotation=30, ha="right", fontsize=7)
ax.set_yticks(range(len(perfil.index)))
ax.set_yticklabels([i[:36] for i in perfil.index], fontsize=7)
for i in range(perfil.shape[0]):
    for j in range(perfil.shape[1]):
        v = perfil.values[i, j]
        if v > 3:
            ax.text(j, i, f"{v:.0f}", ha="center", va="center", fontsize=6.5,
                    color="white" if v > 55 else "black")
fig.colorbar(im, ax=ax, label="% de la carga de la sociedad portuaria")
figura(fig, "P27", "Especializacion de cada sociedad portuaria", "porcentaje")
guardar(perfil.reset_index(), "especializacion_terminales")""",
  "La especialización es casi total. TCBUEN moviliza **100 % contenedores**. Grupo Portuario "
  "y Compañía de Puertos Asociados movilizan **solo graneles**. Aguadulce combina "
  "contenedores con granel sólido, y la Sociedad Portuaria Regional es la única con una "
  "canasta repartida entre contenedores, granel sólido, carga general y granel líquido.",
  "La especialización matiza la lectura de P26. El HHI trata a las sociedades como si fueran "
  "intercambiables, y el cruce muestra que no movilizan lo mismo: TCBUEN no registró "
  "toneladas de granel en el periodo, y Compañía de Puertos Asociados no registró "
  "contenedores. Un reparto agregado del 51 % y 25 % describe cuánto movilizó cada una, no "
  "si podrían movilizar lo de la otra.",
  "La fuente registra toneladas movilizadas por tipo de carga: **no contiene capacidad "
  "instalada, utilización, número de muelles ni equipos**. No permite afirmar que una "
  "sociedad no pueda movilizar un tipo de carga, solo que no lo registró en el periodo. El "
  "perfil se calcula sobre 2018-2026 completo y no capta cambios internos.",
  "Superintendencia de Transporte (2026), consulta agregada por sociedad y tipo de carga")

q("P28", "¿Existen cambios de capacidad, concesión, infraestructura o metodología que afecten las series?",
  "ejecutada",
"""ta = pd.read_csv(RUTA_TERMINALES_ANIO)
ta["ton"] = ta[["sum_importacion", "sum_exportacion", "sum_transbordo"]].sum(axis=1)
piv = ta.pivot_table(index="sociedad_portuaria", columns="anno_vigencia",
                     values="ton", fill_value=0)
mostrar((piv / 1e6).round(2).reset_index())

fig, ax = plt.subplots(figsize=(10, 3.4))
for soc in piv.index:
    ax.plot(piv.columns, piv.loc[soc] / 1e6, marker="o", ms=3.5, label=soc[:30])
ax.set_ylabel("millones de toneladas por año"); ax.set_xlabel("año")
ax.legend(fontsize=6, ncol=2)
ax.axvspan(2025.5, 2026.5, color="grey", alpha=.15)
ax.text(2025.6, ax.get_ylim()[1] * .9, "2026 parcial (6 meses)", fontsize=6.5, color="#555")
figura(fig, "P28", "Actividad anual por sociedad portuaria", "millones de toneladas")

print("Sociedades que no aparecen reportando en 2026:")
for soc in piv.index:
    activos = [int(y) for y in piv.columns if piv.loc[soc, y] > 0]
    if max(activos) < 2026:
        print(f"  {soc[:48]:<48} último año con reporte: {max(activos)}")
print("La fuente registra reporte, no operacion: no puede concluirse que hayan dejado de operar.")
guardar(piv.reset_index(), "actividad_anual_terminales")""",
  "**Dos de las cinco sociedades portuarias no aparecen reportando en 2026.** Grupo Portuario cae de cerca de 1,5 "
  "millones de toneladas anuales a 3.630 en 2025 y no figura en los seis meses observados de 2026. Compañía de Puertos "
  "Asociados reporta hasta 2025 y tampoco aparece en 2026. Se verificó mes a mes: en los "
  "seis meses de 2026 solo reportan tres sociedades, de modo que **no se trata de rezago de "
  "publicación**.",
  "Este es el tipo de cambio que rompe una serie sin avisar. Si dos sociedades dejan de "
  "figurar, el total de la zona cae por razones de reporte y no comerciales, y un modelo "
  "entrenado sobre esa serie interpretaría el quiebre como una caída del comercio. Obliga a "
  "revisar si el pronóstico portuario debe hacerse sobre el total de la zona o sobre las "
  "sociedades que siguen reportando.",
  "La fuente registra reporte, no operación: los datos solo permiten afirmar que no figuran "
  "en los reportes del periodo observado. **No puede afirmarse que hayan dejado de operar.** La causa institucional (fin de "
  "concesión, fusión o cambio de obligación de reporte) requiere fuentes de la ANI que no "
  "se integraron.",
  "Superintendencia de Transporte (2026), verificación mensual propia sobre 2026")

# ======================================================================================
# P49 reimplementada con la ablación multidominio real.
# ======================================================================================
q("P49", "¿Qué variables aportan valor incremental al pronóstico?",
  "ejecutada",
"""from sklearn.linear_model import Ridge
from sklearn.preprocessing import StandardScaler

d = integrado.merge(ext_m, on="mes", how="left").sort_values("mes").reset_index(drop=True)
OBJ = "cif_usd"
# TODAS las variables se rezagan: al predecir el mes t no existe ningun dato de t
for k in (1, 2, 3, 12):
    d[f"cif_lag{k}"] = d[OBJ].shift(k)
for k in (1, 2, 3):
    d[f"ton_lag{k}"] = d["toneladas_totales"].shift(k)
    d[f"cont_lag{k}"] = d["ton_contenerizada"].shift(k)
    d[f"trm_lag{k}"] = d["trm_cop_usd"].shift(k)
d["cif_ma3"] = d[OBJ].shift(1).rolling(3).mean()
d["ton_ma3"] = d["toneladas_totales"].shift(1).rolling(3).mean()
d["mes_num"] = d["mes"].dt.month
d["tendencia"] = np.arange(len(d))
d["oni_lag1"] = d["oni_anomalia"].shift(1)

A = ["cif_lag1", "cif_lag2", "cif_lag3", "cif_lag12", "cif_ma3"]
CAL = ["mes_num", "tendencia"]
PUE = ["ton_lag1", "ton_lag2", "ton_lag3", "cont_lag1", "ton_ma3"]
CTX = ["trm_lag1", "trm_lag2", "trm_lag3", "oni_lag1"]
CONJ = {"A · historia propia": A, "B · A + calendario": A + CAL,
        "C · A + PUERTO": A + PUE, "D · A + contexto": A + CTX,
        "E · integrado completo": A + CAL + PUE + CTX}

dd = d.dropna().reset_index(drop=True)
N = 24
filas = []
for nombre, cols in CONJ.items():
    X, y = dd[cols].values, dd[OBJ].values
    ini = len(y) - N
    obs, pred = [], []
    for t in range(ini, len(y)):
        sc = StandardScaler().fit(X[:t])
        m = Ridge(alpha=1.0).fit(sc.transform(X[:t]), y[:t])
        pred.append(float(m.predict(sc.transform(X[[t]]))[0]))
        obs.append(float(y[t]))
    filas.append({"conjunto": nombre, "n_vars": len(cols), "wape_pct": round(wape(obs, pred), 3)})

y = dd[OBJ].values
ini = len(y) - N
for nom, f in [("naive_1", lambda h: h[-1]),
               ("naive_12", lambda h: h[-12] if len(h) >= 12 else h[-1]),
               ("drift", lambda h: h[-1] + (h[-1] - h[0]) / (len(h) - 1))]:
    obs = [y[t] for t in range(ini, len(y))]
    pred = [f(y[:t]) for t in range(ini, len(y))]
    filas.append({"conjunto": f"base · {nom}", "n_vars": 0,
                  "wape_pct": round(wape(obs, pred), 3)})

abl = pd.DataFrame(filas).sort_values("wape_pct").reset_index(drop=True)
base_a = abl.loc[abl.conjunto == "A · historia propia", "wape_pct"].iloc[0]
abl["ganancia_vs_A_pp"] = (base_a - abl["wape_pct"]).round(3)
mostrar(abl)

fig, ax = plt.subplots(figsize=(9.5, 3.4))
col = ["#2e7d32" if g > 0 else "#c62828" if "base" not in c else "#9e9e9e"
       for g, c in zip(abl["ganancia_vs_A_pp"], abl["conjunto"])]
ax.barh(abl["conjunto"][::-1], abl["wape_pct"][::-1], color=col[::-1])
ax.axvline(base_a, ls="--", color="#31708e")
ax.text(base_a + .05, -.4, "solo historia propia", fontsize=6.5, color="#31708e")
ax.set_xlabel("WAPE (%)  ·  menor es mejor")
figura(fig, "P49", "Ablacion multidominio sobre el pronostico del CIF", "WAPE en porcentaje",
       "2018-01 a 2026-05")

c = abl.loc[abl.conjunto == "C · A + PUERTO", "wape_pct"].iloc[0]
print(f"¿El puerto mejora el pronostico aduanero? {'SI' if c < base_a else 'NO'}")
print(f"  historia propia: {base_a:.3f} %   ->   con puerto: {c:.3f} %")
guardar(abl, "ablacion_multidominio")""",
  "**Las variables portuarias NO mejoran el pronóstico del CIF: lo empeoran.** Solo la "
  "historia propia da 6,082 % de WAPE; añadiendo variables portuarias sube a 6,575 %. El "
  "modelo integrado completo (16 variables) tampoco mejora: 6,167 %. El único conjunto que "
  "aporta es historia propia más calendario, con 5,875 %. Las cinco configuraciones superan "
  "a las tres líneas base.",
  "Este es el resultado más importante de la versión 5, y es negativo. La hipótesis "
  "implícita del proyecto integrado era que cruzar dominios mejoraría la predicción. Los "
  "datos dicen que no. La explicación tiene sentido: ambas fuentes miden el mismo comercio "
  "subyacente con el mismo rezago de publicación, así que el puerto no aporta información "
  "que la historia del propio CIF no contenga ya, y sí aporta ruido y grados de libertad "
  "consumidos sobre una muestra de 89 filas. **El valor de la integración no es predictivo: "
  "es explicativo.** Sirve para responder si un mes cambió por valor o por volumen físico, "
  "y para localizar por qué terminal pasa la carga. Presentarla como una mejora del "
  "pronóstico sería afirmar algo que este análisis refuta.",
  "La ablación se hace sobre 89 filas utilizables y 24 cortes, con Ridge. Un conjunto de "
  "variables portuarias distinto o una muestra más larga podrían dar otro resultado, pero "
  "la conclusión debe reportarse tal como se midió.",
  "Cálculo propio sobre la vista integrada, backtest walk-forward de un paso")


# ======================================================================================
# Gráficos para las once preguntas que solo producían tabla. Cada visual es informativo,
# no decorativo: donde un gráfico de datos no tendría sentido, se usa un panel de estado
# que comunica el resultado de la comprobación.
# ======================================================================================
_GRAFICOS = {

"P03": '''
piv = dicc.assign(v=1).pivot_table(index="variable", columns="dominio", values="v", fill_value=0)
fig, ax = plt.subplots(figsize=(7.5, 3.2))
im = ax.imshow(piv.values, aspect="auto", cmap="Blues", vmin=0, vmax=1.4)
ax.set_xticks(range(len(piv.columns)))
ax.set_xticklabels(piv.columns, fontsize=8)
ax.set_yticks(range(len(piv.index)))
ax.set_yticklabels(piv.index, fontsize=8)
for i in range(piv.shape[0]):
    for j in range(piv.shape[1]):
        if piv.values[i, j]:
            ax.text(j, i, "presente", ha="center", va="center", fontsize=7, color="white")
ax.set_title("Qué variable aporta cada dominio", fontsize=9)
figura(fig, "P03", "Matriz fuente-variable", "presencia")''',

"P04": '''
fig, ax = plt.subplots(figsize=(8.5, 3))
y = range(len(acc))
ax.barh([f - .2 for f in y], acc["automatizable"].astype(int), height=.38,
        color="#31708e", label="descarga automatizable")
ax.barh([f + .2 for f in y], acc["reproducible"].astype(int), height=.38,
        color="#a5673f", label="reproducible")
ax.set_yticks(list(y))
ax.set_yticklabels([s[:30] for s in acc["fuente"]], fontsize=8)
ax.set_xticks([0, 1])
ax.set_xticklabels(["no", "sí"])
ax.legend(fontsize=7)
figura(fig, "P04", "Accesibilidad y reproducibilidad por fuente", "sí o no")''',

"P06": '''
cols = ["permite_uso_academico", "exige_atribucion", "permite_redistribuir"]
fig, ax = plt.subplots(figsize=(7.5, 2.8))
im = ax.imshow(leg[cols].astype(int).values, aspect="auto", cmap="RdYlGn", vmin=0, vmax=1)
ax.set_xticks(range(len(cols)))
ax.set_xticklabels(["uso académico", "exige atribución", "redistribución"], fontsize=8)
ax.set_yticks(range(len(leg)))
ax.set_yticklabels(leg["fuente"], fontsize=8)
for i in range(len(leg)):
    for j, c in enumerate(cols):
        ax.text(j, i, "sí" if leg[c].iloc[i] else "no", ha="center", va="center", fontsize=8)
figura(fig, "P06", "Matriz de condiciones legales por fuente", "permitido o no")''',

"P08": '''
fig, ax = plt.subplots(figsize=(8, 2.8))
ax.barh(man["fuente"], man["filas"], color=["#31708e", "#a5673f"])
for i, v in enumerate(man["filas"]):
    ax.text(v, i, f"  {v:,} filas", va="center", fontsize=8)
ax.set_xlabel("filas registradas en el manifiesto")
figura(fig, "P08", "Volumen y trazabilidad de cada fuente aprobada", "número de filas")''',

"P09": '''
esq_a = esq[esq.dominio == "aduanero"]
fig, ax = plt.subplots(figsize=(9.5, 2.8))
colores = {"coma": "#31708e", "punto y coma": "#a5673f", "mixto": "#c62828"}
for i, (_, r) in enumerate(esq_a.iterrows()):
    ax.barh(0, 1, left=i, color=colores.get(r["separador"], "#999"), edgecolor="white")
    ax.text(i + .5, 0, f"{r['columnas']}\\ncol", ha="center", va="center",
            fontsize=7, color="white")
    ax.text(i + .5, .62, r["vigencia"], ha="center", fontsize=6.5, rotation=25)
ax.set_ylim(-.6, 1)
ax.set_yticks([])
ax.set_xticks([])
ax.set_title("Cada color es un formato distinto: cinco cambios en catorce años", fontsize=9)
figura(fig, "P09", "Evolucion del esquema por vigencia", "formato y número de columnas")''',

"P11": '''
fig, ax = plt.subplots(figsize=(8, 2.8))
b = ax.barh(dup["capa"], dup["duplicados"], color="#2e7d32")
ax.set_xlabel("duplicados encontrados")
ax.set_xlim(0, max(1, dup["duplicados"].max() * 1.4))
for i, v in enumerate(dup["duplicados"]):
    ax.text(v + .02, i, f"  {v} sobre {dup['filas'].iloc[i]:,} filas", va="center", fontsize=8)
figura(fig, "P11", "Duplicados detectados por capa", "número de duplicados")''',

"P12": '''
fig, ax = plt.subplots(figsize=(8, 2.8))
disponible = uni["factor_a_base"].notna()
ax.barh(uni["variable"], [1] * len(uni),
        color=["#2e7d32" if d else "#c62828" for d in disponible])
for i, (_, r) in enumerate(uni.iterrows()):
    txt = f"{r['unidad']}" + (f"  ·  factor {int(r['factor_a_base'])}"
                              if pd.notna(r["factor_a_base"]) else "")
    ax.text(.02, i, txt, va="center", fontsize=8, color="white")
ax.set_xticks([])
ax.set_title("En rojo, la unidad que la fuente NO publica", fontsize=9)
figura(fig, "P12", "Unidades por variable y factor de conversion", "unidad")''',

"P13": '''
fig, ax = plt.subplots(figsize=(8, 2.8))
y = range(len(dom))
ax.barh([v - .2 for v in y], dom["n_negativos"], height=.38, color="#c62828",
        label="negativos")
ax.barh([v + .2 for v in y], dom["n_ceros"], height=.38, color="#f9a825", label="ceros")
ax.set_yticks(list(y))
ax.set_yticklabels(dom["variable"], fontsize=8)
ax.set_xlabel("registros")
ax.legend(fontsize=7)
ax.set_title("Cero negativos. Los ceros son legítimos: ese movimiento no ocurrió", fontsize=9)
figura(fig, "P13", "Valores negativos y ceros por variable", "número de registros")''',

"P14": '''
fig, ax = plt.subplots(1, 2, figsize=(11, 2.8))
ax[0].bar(["esperados", "observados"],
          [cont["meses_esperados"], cont["meses_observados"]], color=["#a5673f", "#2e7d32"])
ax[0].set_ylabel("meses")
ax[0].set_title(f"Continuidad portuaria: {'sin huecos' if cont['continua'] else 'CON HUECOS'}",
                fontsize=9)
ax[1].axis("off")
ax[1].text(.5, .6, "173 de 173 meses", ha="center", fontsize=15, weight="bold", color="#2e7d32")
ax[1].text(.5, .35, "dentro de la tolerancia declarada del 0,5 %", ha="center", fontsize=9)
ax[1].text(.5, .15, "diferencia total del CIF: 0,000066 %", ha="center", fontsize=9, color="#555")
ax[1].set_title("Reconciliación del dominio aduanero", fontsize=9)
figura(fig, "P14", "Continuidad y reconciliacion", "meses y porcentaje")''',

"P22": '''
fig, ax = plt.subplots(figsize=(8.5, 2.6))
ax.axis("off")
ax.text(.5, .72, "NO EVALUABLE CON UNA SOLA DESCARGA", ha="center", fontsize=13,
        weight="bold", color="#8e24aa")
ax.text(.5, .44, "Medir el efecto de las revisiones exige al menos dos descargas "
        "en fechas distintas.", ha="center", fontsize=9)
ax.text(.5, .18, "Disponible: 1 descarga (2026-08-01). La versión queda conservada con su "
        "hash para la comparación futura.", ha="center", fontsize=8, color="#555")
figura(fig, "P22", "Estado de la evaluacion de revisiones del DANE", "sin dato")''',

"P40": '''
fig, ax = plt.subplots(figsize=(8.5, 2.8))
ax.barh(met["fuente"], [1] * len(met),
        color=["#2e7d32" if x else "#c62828" for x in met["integrada"]])
for i, (_, r) in enumerate(met.iterrows()):
    ax.text(.02, i, f"{r['variable']} — {'integrada' if r['integrada'] else 'no integrada'}",
            va="center", fontsize=8, color="white")
ax.set_xticks([])
ax.set_title("Solo el ONI quedó integrado, como contexto", fontsize=9)
figura(fig, "P40", "Fuentes meteomarinas evaluadas frente a integradas", "integrada o no")''',
}

for _id, _g in _GRAFICOS.items():
    Q[_id]["codigo"] = Q[_id]["codigo"].rstrip() + "\n" + _g.strip() + "\n"


# ======================================================================================
# P23 y P30 ampliadas: la caída del transbordo y la descomposición del crecimiento del
# CIF en volumen y valor unitario. Ambos resultados salían del pipeline pero no estaban
# redactados en ninguna pregunta, de modo que no eran trazables.
# ======================================================================================
Q["P23"]["codigo"] = Q["P23"]["codigo"].rstrip() + """

# Descomposición del total: el transbordo no es comercio exterior colombiano
a12, u12 = sp.head(12), sp.tail(12)
desc = pd.DataFrame([
    {"componente": c,
     "primeros_12_meses_Mt": round(a12[c].mean() / 1e6, 3),
     "ultimos_12_meses_Mt": round(u12[c].mean() / 1e6, 3),
     "variacion_pct": round((u12[c].mean() / a12[c].mean() - 1) * 100, 1)}
    for c in ["ton_importacion", "ton_exportacion", "ton_transbordo", "toneladas_totales"]])
mostrar(desc)

fig, ax = plt.subplots(figsize=(9, 3.2))
col = ["#2e7d32" if v > 0 else "#c62828" for v in desc["variacion_pct"]]
ax.barh(desc["componente"], desc["variacion_pct"], color=col)
ax.axvline(0, color="grey", lw=.8)
ax.set_xlabel("variación entre los primeros y los últimos 12 meses de la serie (%)")
figura(fig, "P23b", "Variacion por componente del trafico portuario", "porcentaje")
guardar(desc, "descomposicion_trafico_portuario")
"""
Q["P23"]["respuesta"] = (
    "La zona portuaria movilizó en promedio 1,70 millones de toneladas mensuales entre "
    "2018-01 y 2026-06, en 102 meses continuos sin huecos.\n\n"
    "Al descomponer el total, los componentes se mueven en direcciones opuestas: "
    "comparando los primeros doce meses de la serie (2018) con los últimos doce "
    "(2025-07 a 2026-06), las toneladas de importación **suben un 19,6 %**, las de "
    "exportación apenas un 1,3 %, y el **transbordo cae un 85,2 %**. El total resultante "
    "baja un 13,3 %.")
Q["P23"]["explicacion"] = (
    "El transbordo es carga que llega en un buque y sale en otro sin entrar al territorio "
    "aduanero: no forma parte del comercio exterior colombiano. Sumarlo al total mezcla dos "
    "cosas distintas. Con esa suma, la serie sugiere que la zona movilizó un 12,6 % menos "
    "de carga; separando componentes, lo que descendió fue el trasbordo, mientras la carga "
    "de importación creció. Es la diferencia entre leer una caída del comercio y leer un "
    "cambio en el uso del puerto como punto de conexión entre buques.")
Q["P23"]["limitacion"] = (
    "La comparación usa promedios de doce meses en los extremos de la serie, no una "
    "tendencia ajustada. La fuente no informa por qué cambió el transbordo: las causas "
    "posibles —decisiones de las navieras, reasignación de rutas o cambios de reporte— no "
    "son distinguibles con estos datos.")

Q["P30"]["codigo"] = Q["P30"]["codigo"].rstrip() + """

# ¿Cuánto del alza del valor CIF es más mercancía y cuánto mercancía más cara?
# CIF = peso x valor unitario, de modo que la descomposición se hace en logaritmos
# para que las dos partes sumen exactamente el total.
j12a, j12b = integrado.head(12), integrado.tail(12)
g_cif = np.log(j12b["cif_usd"].mean() / j12a["cif_usd"].mean())
g_peso = np.log(j12b["peso_neto_kg"].mean() / j12a["peso_neto_kg"].mean())
g_uni = np.log(j12b["cif_kg"].mean() / j12a["cif_kg"].mean())
dsc = pd.DataFrame([
    {"componente": "valor CIF", "variacion_pct": round((np.exp(g_cif) - 1) * 100, 1),
     "aporte_al_crecimiento_pct": 100.0},
    {"componente": "volumen (peso neto)", "variacion_pct": round((np.exp(g_peso) - 1) * 100, 1),
     "aporte_al_crecimiento_pct": round(g_peso / g_cif * 100, 1)},
    {"componente": "valor unitario (CIF/kg)", "variacion_pct": round((np.exp(g_uni) - 1) * 100, 1),
     "aporte_al_crecimiento_pct": round(g_uni / g_cif * 100, 1)}])
mostrar(dsc)

fig, ax = plt.subplots(figsize=(8, 2.8))
ax.barh(["valor unitario", "volumen"],
        [dsc.aporte_al_crecimiento_pct.iloc[2], dsc.aporte_al_crecimiento_pct.iloc[1]],
        color=["#a5673f", "#31708e"])
ax.set_xlabel("aporte al crecimiento del valor CIF (%)")
ax.set_title("Aportes al crecimiento del CIF", fontsize=9)
print(f"suma de los dos aportes: {dsc.aporte_al_crecimiento_pct.iloc[1] + dsc.aporte_al_crecimiento_pct.iloc[2]:.1f} %")
print("El residuo no nulo viene de promediar meses: la media de un cociente no es el")
print("cociente de las medias, de modo que la identidad CIF = peso x valor unitario se")
print("cumple mes a mes pero no exactamente sobre los promedios de doce meses.")
figura(fig, "P30b", "Descomposicion del crecimiento del CIF", "porcentaje del crecimiento")
guardar(dsc, "descomposicion_cif_volumen_valor")
"""
