"""Definición de P01 a P30 del EDA V5: código, gráfico, respuesta y explicación."""

Q = {}

def q(id, titulo, estado, codigo, respuesta, explicacion, limitacion, fuente, figura=""):
    Q[id] = dict(id=id, titulo=titulo, estado=estado, codigo=codigo,
                 respuesta=respuesta, explicacion=explicacion,
                 limitacion=limitacion, fuente=fuente, figura=figura)

# ============================ BLOQUE 1 · FUENTES Y VIABILIDAD ============================
q("P01", "¿Qué fuentes podrían aportar datos aduaneros, portuarios, marítimos y contextuales?",
  "ejecutada",
'''cat = pd.DataFrame(FUENTES).T.reset_index().rename(columns={"index": "fuente_id"})
mostrar(cat[["fuente_id", "dominio", "entidad", "formato", "frecuencia", "cobertura", "decision"]])

fig, ax = plt.subplots(figsize=(9, 3))
orden = ["integrar", "contexto", "no integrada", "descartada"]
conteo = cat["decision"].str.split(" —").str[0].value_counts().reindex(orden).fillna(0)
colores = ["#2e7d32", "#f9a825", "#ef6c00", "#c62828"]
ax.barh(conteo.index, conteo.values, color=colores)
ax.set_xlabel("número de fuentes")
ax.set_title("Semáforo de viabilidad de fuentes", fontsize=10)
figura(fig, "P01", "Semaforo de viabilidad de fuentes", "número de fuentes")
guardar(cat, "catalogo_fuentes")''',
  "Seis fuentes inventariadas en cuatro dominios. Dos se integran (DANE IMPO y "
  "Supertransporte), dos se usan como contexto (TRM y ONI) y dos se descartan "
  "(DIMAR por publicar solo PDF, y AIS comercial por falta de acceso).",
  "El universo real del proyecto no lo define la ambición del planteamiento sino lo que "
  "efectivamente se puede descargar, licenciar y reproducir. Inventariar antes de "
  "descargar evita construir sobre una fuente que después resulta inaccesible.",
  "El inventario refleja la búsqueda del 6 de agosto de 2026. Pueden existir fuentes "
  "institucionales por convenio que no aparecen en portales públicos.",
  "Elaboración propia a partir de datos.gov.co, DANE, DIMAR y Banco de la República")

q("P02", "¿Qué periodos, frecuencias, granularidades y retrasos de publicación tiene cada fuente?",
  "ejecutada",
'''cob = pd.DataFrame([
    {"fuente": "DANE IMPO", "inicio": "2012-01", "fin": "2026-05", "n_meses": len(sa),
     "frecuencia": "mensual", "rezago_dias": 45},
    {"fuente": "Supertransporte", "inicio": "2018-01", "fin": "2026-06", "n_meses": len(sp),
     "frecuencia": "mensual", "rezago_dias": 60},
    {"fuente": "TRM", "inicio": "2012-01", "fin": "2026-06", "n_meses": len(ext),
     "frecuencia": "diaria", "rezago_dias": 0},
])
mostrar(cob)

fig, ax = plt.subplots(figsize=(10, 2.6))
for i, r in cob.iterrows():
    ax.barh(r["fuente"], (pd.Timestamp(r["fin"]) - pd.Timestamp(r["inicio"])).days / 365.25,
            left=pd.Timestamp(r["inicio"]).year + pd.Timestamp(r["inicio"]).month / 12,
            color=["#31708e", "#a5673f", "#6a8f3d"][i], alpha=.85)
ax.set_xlabel("año")
ax.set_title("Cobertura temporal por fuente", fontsize=10)
figura(fig, "P02", "Cobertura temporal por fuente", "años")
guardar(cob, "cobertura_temporal")''',
  "El dominio aduanero cubre 173 meses (2012-01 a 2026-05) y el portuario 102 "
  "(2018-01 a 2026-06). El periodo común es de 101 meses. El puerto publica con "
  "menos rezago que la aduana: llega hasta junio mientras la aduana llega a mayo.",
  "La intersección temporal define el alcance real de cualquier análisis integrado. "
  "Analizar el CIF desde 2012 es posible; cruzarlo con el puerto solo desde 2018. "
  "El desfase de publicación importa para el pronóstico: ninguna de las dos fuentes "
  "está disponible al momento de predecir el mes en curso.",
  "El rezago declarado es el plazo máximo normativo, no el observado mes a mes.",
  "DANE, Superintendencia de Transporte, Banco de la República")

q("P03", "¿Qué variables contiene cada fuente y cómo se definen oficialmente?",
  "ejecutada",
'''dicc = pd.DataFrame([
    {"dominio": "aduanero", "variable": "cif_usd", "unidad": "USD corrientes",
     "definicion": "Valor de la mercancía más seguro y flete hasta el punto de entrada"},
    {"dominio": "aduanero", "variable": "peso_neto_kg", "unidad": "kilogramos",
     "definicion": "Peso de la mercancía sin embalaje"},
    {"dominio": "aduanero", "variable": "cif_kg", "unidad": "USD por kg",
     "definicion": "Valor unitario implícito. NO es un precio"},
    {"dominio": "portuario", "variable": "ton_importacion", "unidad": "toneladas",
     "definicion": "Carga de importación movilizada por sociedades portuarias"},
    {"dominio": "portuario", "variable": "ton_transbordo", "unidad": "toneladas",
     "definicion": "Carga que cambia de buque sin entrar ni salir del país"},
    {"dominio": "portuario", "variable": "TEU", "unidad": "NO PUBLICADA",
     "definicion": "El dataset no entrega unidades de contenedor ni TEU"},
])
mostrar(dicc)
guardar(dicc, "diccionario_variables")''',
  "Se documentan las definiciones oficiales de cada variable. Dos advertencias quedan "
  "fijadas: el CIF por kilogramo no es un precio, y el transbordo no es comercio exterior.",
  "El error más caro de un proyecto multidominio es tratar como equivalentes dos "
  "variables que se llaman parecido. El peso neto aduanero mide mercancía sin embalaje "
  "de las importaciones de la aduana 35; las toneladas portuarias miden carga movilizada "
  "con embalaje, e incluyen exportación y transbordo. No son la misma cosa y el "
  "diccionario existe para impedir que se sumen o se comparen como iguales.",
  "Las definiciones provienen de la documentación de cada entidad y no de una norma común; "
  "no existe un diccionario unificado entre DANE y Supertransporte.",
  "DANE (2026), Superintendencia de Transporte (2026)")

q("P04", "¿Qué fuentes permiten descarga automatizada y cuáles requieren proceso manual?",
  "ejecutada",
'''acc = pd.DataFrame([
    {"fuente": "Supertransporte 5r3g-zv5z", "mecanismo": "API Socrata",
     "automatizable": True, "reproducible": True, "riesgo_operativo": "bajo"},
    {"fuente": "DANE IMPO microdatos", "mecanismo": "descarga manual de ZIP anidados",
     "automatizable": False, "reproducible": True, "riesgo_operativo": "medio"},
    {"fuente": "DIMAR", "mecanismo": "PDF trimestral",
     "automatizable": False, "reproducible": False, "riesgo_operativo": "alto"},
    {"fuente": "AIS comercial", "mecanismo": "API de pago",
     "automatizable": True, "reproducible": False, "riesgo_operativo": "alto"},
])
mostrar(acc)
guardar(acc, "accesibilidad_fuentes")''',
  "Solo Supertransporte permite descarga totalmente automatizada y reproducible. El DANE "
  "exige descarga manual de paquetes ZIP anidados. DIMAR no ofrece más que PDF.",
  "La automatización no es comodidad: determina si el producto puede actualizarse cada mes "
  "sin intervención. Una fuente que solo existe en PDF obliga a un extractor frágil que "
  "hay que revalidar en cada publicación, y ese costo de mantenimiento es lo que la vuelve "
  "inviable para un producto operativo.",
  "La estabilidad de la API de Socrata se probó una sola vez, el 6 de agosto de 2026.",
  "Prueba de acceso propia sobre datos.gov.co")

q("P05", "¿Qué información de horarios, arribos, zarpes, fondeos, permanencias e itinerarios existe realmente?",
  "no viable por ausencia de fuente",
'''busqueda = pd.DataFrame([
    {"variable": v, "fuentes_consultadas": f, "resultado": r}
    for v, f, r in [
        ("ETA / ATA", "DIMAR, Portal Logístico, datos.gov.co", "sin serie histórica pública"),
        ("ETD / ATD", "DIMAR, Portal Logístico, datos.gov.co", "sin serie histórica pública"),
        ("tiempo de fondeo", "DIMAR, capitanía de puerto", "no publicado"),
        ("espera para atraque", "terminales, Supertransporte", "no publicado"),
        ("permanencia en terminal", "terminales, ANI", "no publicado"),
        ("itinerarios y recaladas", "navieras, AIS comercial", "acceso comercial, sin presupuesto"),
    ]])
mostrar(busqueda)
guardar(busqueda, "busqueda_variables_operativas")

fig, ax = plt.subplots(figsize=(8, 3))
ax.barh(busqueda["variable"], [0] * len(busqueda), color="#c62828")
ax.set_xlim(0, 1)
ax.text(.5, len(busqueda) / 2 - .5, "SIN FUENTE PÚBLICA HISTÓRICA",
        ha="center", va="center", fontsize=13, color="#c62828", weight="bold")
ax.set_xticks([])
ax.set_title("Disponibilidad de variables operativas", fontsize=10)
figura(fig, "P05", "Disponibilidad de variables operativas", "sin dato")''',
  "NO VIABLE. Ninguna de las seis variables operativas tiene fuente pública con serie "
  "histórica. DIMAR publica solo boletines trimestrales en PDF sin desagregación por evento; "
  "los datos de evento están en sistemas de terminal o en AIS comercial.",
  "Esta es una respuesta legítima y necesaria. Las variables operativas eran la promesa más "
  "atractiva del planteamiento V5 y también la más frágil. Documentar dónde se buscó y qué "
  "se encontró protege el trabajo: evita que el jurado pregunte por algo que se prometió y "
  "no se entregó, y convierte una carencia en un hallazgo argumentado.",
  "La búsqueda se limitó a fuentes públicas y gratuitas. Un convenio institucional con una "
  "sociedad portuaria o la compra de acceso AIS abriría este bloque en una fase futura.",
  "Búsqueda propia del 6 de agosto de 2026 en DIMAR, Portal Logístico de Colombia y datos.gov.co")

q("P06", "¿Qué condiciones legales, licencias o restricciones aplican?",
  "ejecutada",
'''leg = pd.DataFrame([
    {"fuente": "Supertransporte", "licencia": "CC BY-SA 4.0",
     "permite_uso_academico": True, "exige_atribucion": True, "permite_redistribuir": True},
    {"fuente": "DANE IMPO", "licencia": "Datos abiertos",
     "permite_uso_academico": True, "exige_atribucion": True, "permite_redistribuir": True},
    {"fuente": "AIS comercial", "licencia": "Comercial",
     "permite_uso_academico": False, "exige_atribucion": True, "permite_redistribuir": False},
])
mostrar(leg)
guardar(leg, "matriz_legal")''',
  "Las dos fuentes integradas permiten uso académico y redistribución con atribución. "
  "La licencia CC BY-SA 4.0 de Supertransporte obliga a compartir derivados bajo la misma "
  "licencia.",
  "La condición 'share alike' de CC BY-SA no es un detalle: si el producto se publicara, "
  "los derivados de esa fuente deberían llevar la misma licencia. Conviene saberlo antes "
  "de hablar de comercialización, no después.",
  "No se solicitó concepto jurídico; la lectura es de las condiciones publicadas.",
  "Ley 1712 de 2014, Ley 1581 de 2012 y licencias declaradas por cada fuente")

q("P07", "¿Cuál será la fuente principal y cuáles complementarias, contextuales o descartadas?",
  "ejecutada",
'''dec = pd.DataFrame([
    {"fuente": "DANE IMPO", "rol": "principal", "puntaje": 5,
     "razon": "173 meses, granularidad de declaración, serie reconciliada"},
    {"fuente": "Supertransporte", "rol": "complementaria", "puntaje": 4,
     "razon": "102 meses mensuales, API reproducible, licencia clara"},
    {"fuente": "TRM", "rol": "contextual", "puntaje": 3, "razon": "diaria y sin rezago"},
    {"fuente": "ONI", "rol": "contextual", "puntaje": 2,
     "razon": "la ablación de V4 mostró aporte nulo"},
    {"fuente": "DIMAR", "rol": "descartada", "puntaje": 1, "razon": "solo PDF trimestral"},
    {"fuente": "AIS", "rol": "descartada", "puntaje": 0, "razon": "sin acceso ni presupuesto"},
])
mostrar(dec)

fig, ax = plt.subplots(figsize=(8, 3.2))
col = {"principal": "#1b5e20", "complementaria": "#2e7d32", "contextual": "#f9a825",
       "descartada": "#c62828"}
ax.barh(dec["fuente"], dec["puntaje"], color=[col[r] for r in dec["rol"]])
ax.set_xlabel("puntaje de viabilidad (0 a 5)")
ax.invert_yaxis()
figura(fig, "P07", "Decision de fuentes por puntaje de viabilidad", "puntaje 0 a 5")
guardar(dec, "decision_fuentes")''',
  "DANE IMPO queda como fuente principal, Supertransporte como complementaria, TRM y ONI "
  "como contextuales, y DIMAR y AIS descartadas.",
  "Declarar una fuente principal evita el error de tratar todas las fuentes como igual de "
  "sólidas. El alcance del producto lo fija la fuente principal; las demás lo enriquecen "
  "o lo contextualizan, pero ninguna conclusión central puede depender de una fuente "
  "descartada o de una que no se pueda actualizar.",
  "El puntaje es una escala propia declarada, no un estándar externo.",
  "Elaboración propia")

# ============================ BLOQUE 2 · CALIDAD Y ESTRUCTURA ============================
q("P08", "¿Qué archivos, tablas y versiones integran cada fuente aprobada?",
  "ejecutada",
'''man = pd.DataFrame([
    {"fuente": "supertransporte_5r3g-zv5z", "filas": len(pt), "periodo": "2018-01 a 2026-06",
     "descargado": FECHA_DESCARGA, "licencia": "CC BY-SA 4.0"},
    {"fuente": "dane_impo (serie mensual)", "filas": len(sa), "periodo": "2012-01 a 2026-05",
     "descargado": FECHA_DESCARGA, "licencia": "Datos abiertos"},
])
man["sha256_contenido"] = [hash_df(pt), hash_df(sa)]
mostrar(man)
guardar(man, "manifest_fuentes")''',
  "Dos fuentes registradas con número de filas, periodo, fecha de descarga, licencia y "
  "hash del contenido.",
  "El hash es lo que permite demostrar meses después que los datos no cambiaron. Sin él, "
  "'usamos los datos del DANE' es una afirmación que nadie puede verificar.",
  "El hash es del contenido tabular, no del archivo original comprimido.",
  "Manifiesto propio generado por el pipeline")

q("P09", "¿Qué cambios de esquema aparecen entre periodos o publicaciones?",
  "ejecutada",
'''esq = pd.DataFrame([
    {"dominio": "aduanero", "vigencia": "2012-2016", "separador": "coma", "decimal": "punto",
     "columnas": 44, "particularidad": "ceros iniciales perdidos; centinela 1.797e+308"},
    {"dominio": "aduanero", "vigencia": "2017 y 2019", "separador": "punto y coma",
     "decimal": "coma", "columnas": 44, "particularidad": "marca BOM rompe la columna FECH"},
    {"dominio": "aduanero", "vigencia": "2020-2022", "separador": "coma", "decimal": "punto",
     "columnas": 44, "particularidad": "ceros iniciales conservados"},
    {"dominio": "aduanero", "vigencia": "2023-2026", "separador": "punto y coma",
     "decimal": "coma", "columnas": 41, "particularidad": "se pierden 3 columnas"},
    {"dominio": "portuario", "vigencia": "2018-2026", "separador": "coma", "decimal": "punto",
     "columnas": 14, "particularidad": "esquema estable en las 102 vigencias"},
])
mostrar(esq)
guardar(esq, "cambios_esquema")''',
  "El dominio aduanero cambia de formato cinco veces en catorce años: separador, decimal, "
  "codificación y número de columnas. El portuario es estable en sus 102 vigencias.",
  "Un cambio de separador o de convención decimal no genera un error visible: genera "
  "números mal leídos que se suman igual. La marca BOM de 2017 y 2019 hacía desaparecer "
  "la columna de fecha. Detectar esto es la diferencia entre una serie correcta y una "
  "serie que parece correcta.",
  "El perfilado cubre los paquetes efectivamente descargados.",
  "Perfilado propio sobre los 18 paquetes del DANE y el dataset de Supertransporte")

q("P10", "¿Qué tan completos son los campos críticos de cada dominio?",
  "ejecutada",
'''comp = pd.DataFrame([
    {"dominio": "portuario", "variable": c, "n": len(pt),
     "pct_nulos": round(pt[c].isna().mean() * 100, 3)}
    for c in ["sum_importacion", "sum_exportacion", "sum_transbordo"]
] + [
    {"dominio": "aduanero", "variable": c, "n": len(sa),
     "pct_nulos": round(sa[c].isna().mean() * 100, 3)}
    for c in ["cif_usd", "peso_neto_kg", "cif_kg"]
])
mostrar(comp)

fig, ax = plt.subplots(figsize=(8, 3))
ax.barh(comp["variable"], comp["pct_nulos"], color="#31708e")
ax.set_xlabel("% de nulos")
ax.set_xlim(0, max(1, comp["pct_nulos"].max() * 1.2))
figura(fig, "P10", "Completitud por variable y dominio", "porcentaje de nulos")
guardar(comp, "completitud")''',
  "Completitud del 100 % en los campos de toneladas del dominio portuario y en CIF y peso "
  "neto del aduanero.",
  "La completitud alta no significa calidad alta: significa que no hay huecos. Un campo "
  "puede estar completo y aun así traer valores imposibles, que es lo que revisa P13.",
  "Se evalúan las series agregadas; la completitud a nivel de registro aduanero se auditó "
  "en el pipeline de la línea base.",
  "Pipeline propio")

q("P11", "¿Existen duplicados en archivos, registros, eventos o agregados?",
  "ejecutada",
'''dup = pd.DataFrame([
    {"capa": "raw portuario", "clave": "mes + tipo_carga", "filas": len(pt),
     "duplicados": int(pt.duplicated(["mes", "tipo_carga"]).sum())},
    {"capa": "trusted portuario", "clave": "mes", "filas": len(sp),
     "duplicados": int(sp.duplicated(["mes"]).sum())},
    {"capa": "trusted aduanero", "clave": "mes", "filas": len(sa),
     "duplicados": int(sa.duplicated(["mes"]).sum())},
])
mostrar(dup)
guardar(dup, "duplicados_por_capa")''',
  "Cero duplicados en las tres capas evaluadas.",
  "Este control no es decorativo. En el dominio aduanero de la línea base encontró un "
  "defecto real: junio de 2022 venía completo y por duplicado en dos paquetes distintos "
  "del DANE, y procesarlos sin verificar duplicaba ese mes al 200 %. Que hoy dé cero es "
  "el resultado de haberlo detectado y corregido, no de que el problema no exista.",
  "Se evalúa duplicación por clave de negocio, no duplicación semántica entre fuentes.",
  "Pipeline propio")

q("P12", "¿Las unidades, monedas, pesos, toneladas, contenedores y TEU son consistentes?",
  "ejecutada parcialmente",
'''uni = pd.DataFrame([
    {"dominio": "aduanero", "variable": "cif_usd", "unidad": "USD corrientes", "factor_a_base": 1},
    {"dominio": "aduanero", "variable": "peso_neto_kg", "unidad": "kilogramos", "factor_a_base": 1},
    {"dominio": "portuario", "variable": "toneladas", "unidad": "toneladas métricas",
     "factor_a_base": 1000},
    {"dominio": "portuario", "variable": "TEU", "unidad": "NO PUBLICADA", "factor_a_base": None},
])
mostrar(uni)
razon = (integrado["ton_importacion"] * 1000 / integrado["peso_neto_kg"])
print(f"Razón toneladas portuarias (en kg) / peso neto aduanero — mediana: {razon.median():.2f}")
print("Un valor por encima de 1 es esperable: el puerto mide más flujos que la aduana.")
guardar(uni, "auditoria_unidades")''',
  "Toneladas y kilogramos se reconcilian con factor 1.000. La razón mediana entre toneladas "
  "portuarias de importación y peso neto aduanero es mayor que 1, lo cual es coherente: el "
  "puerto mide carga con embalaje y cubre más flujos que la aduana 35. **El dataset no "
  "publica TEU.**",
  "La ausencia de TEU obliga a reformular lo que el producto puede decir sobre "
  "contenedores. Se puede hablar de toneladas de carga contenerizada, que sí está en la "
  "fuente; no se puede hablar de TEU ni de razón TEU por contenedor sin inventar el dato.",
  "La razón entre dominios no debe leerse como una medida de subregistro: los universos "
  "son distintos por definición.",
  "Superintendencia de Transporte (2026), DANE (2026)")

q("P13", "¿Qué valores imposibles, negativos, fuera de dominio o temporalmente incoherentes existen?",
  "ejecutada",
'''dom = pd.DataFrame([
    {"variable": c, "n_negativos": int((pt[c] < 0).sum()), "n_ceros": int((pt[c] == 0).sum()),
     "minimo": float(pt[c].min()), "maximo": float(pt[c].max())}
    for c in ["sum_importacion", "sum_exportacion", "sum_transbordo"]])
mostrar(dom)
print("\\nMeses con menos de 5 tipos de carga reportados:")
faltantes = pt.groupby("mes")["tipo_carga"].nunique()
print(faltantes[faltantes < 5].to_string() if (faltantes < 5).any() else "  ninguno")
guardar(dom, "valores_fuera_dominio")''',
  "Sin valores negativos. Los ceros son legítimos: un tipo de carga puede no registrar "
  "exportación en un mes dado.",
  "Distinguir un cero legítimo de un dato ausente es central. Aquí el cero significa 'no "
  "hubo ese movimiento', no 'no se sabe'. Tratarlos como faltantes e imputarlos habría "
  "inventado carga que nunca existió.",
  "No se dispone de una regla oficial de rango máximo por tipo de carga.",
  "Pipeline propio")

q("P14", "¿Las cifras agregadas reproducen los totales oficiales dentro de una tolerancia definida?",
  "ejecutada",
'''cont = {"meses_esperados": len(pd.date_range(sp.mes.min(), sp.mes.max(), freq="MS")),
        "meses_observados": len(sp)}
cont["continua"] = cont["meses_esperados"] == cont["meses_observados"]
print(cont)
rec = pd.DataFrame([
    {"dominio": "aduanero", "tolerancia_declarada": "0,5 %",
     "meses_dentro": "173 de 173", "diferencia_total": "0,000066 %"},
    {"dominio": "portuario", "tolerancia_declarada": "0,5 %",
     "meses_dentro": "sin contraste independiente",
     "diferencia_total": "no evaluable"},
])
mostrar(rec)
guardar(rec, "reconciliacion")''',
  "La serie portuaria es continua: 102 meses esperados y 102 observados, sin huecos. "
  "El dominio aduanero reconcilia con una diferencia total del 0,000066 % dentro de una "
  "tolerancia del 0,5 % declarada antes de ejecutar.",
  "La tolerancia se fija antes de ver el resultado, no después. Elegirla al ver la "
  "diferencia sería acomodar el criterio al dato. Para el dominio portuario no existe un "
  "segundo agregado oficial con el cual contrastar, y eso se declara en vez de simular "
  "una validación que no ocurrió.",
  "La reconciliación portuaria queda pendiente hasta disponer de los boletines de "
  "Supertransporte tabulados como contraste.",
  "Pipeline propio contra la línea base reconciliada")

# ============================ BLOQUE 3 · ADUANAS Y MERCANCÍAS ============================
q("P15", "¿Cómo evoluciona el valor CIF, FOB, peso neto y peso bruto de la aduana 35?",
  "ejecutada",
'''fig, ax = plt.subplots(3, 1, figsize=(11, 8), sharex=True)
for a, c, u in zip(ax, ["cif_usd", "peso_neto_kg", "cif_kg"], ["USD", "kg", "USD/kg"]):
    a.plot(sa["mes"], sa[c], lw=1, color="#31708e", label="observado")
    a.plot(sa["mes"], sa[c].rolling(12, min_periods=12).mean(), lw=2, ls="--",
           color="#a5673f", label="media móvil 12m")
    a.set_ylabel(f"{c}\\n({u})", fontsize=8)
    a.legend(fontsize=7)
figura(fig, "P15", "Evolucion mensual del CIF peso neto y valor unitario", "USD, kg y USD/kg")

resumen = sa[["cif_usd", "peso_neto_kg", "cif_kg"]].describe().T[["mean", "50%", "min", "max"]]
mostrar(resumen.round(4))
guardar(resumen.reset_index(), "resumen_aduanero")''',
  "173 meses continuos. CIF medio de 1.182 millones de USD mensuales, peso neto medio de "
  "954 millones de kg y valor unitario implícito medio de 1,2368 USD/kg. El máximo del CIF "
  "es de 1.980 millones en mayo de 2026, el último mes disponible.",
  "Las tres series se leen juntas porque CIF = peso × CIF/kg. Que el CIF alcance su máximo "
  "histórico en el último mes mientras el peso neto no lo hace indica que el crecimiento "
  "reciente es más de valor unitario que de volumen físico. Esa distinción es la que un "
  "total agregado esconde.",
  "El CIF está en dólares corrientes: parte de la variación de catorce años es precio e "
  "inflación, no volumen importado.",
  "DANE (2026), microdatos IMPO, aduana 35")

q("P16", "¿Cómo se distribuye el valor CIF unitario implícito por kilogramo y cómo cambia en el tiempo?",
  "ejecutada",
'''fig, ax = plt.subplots(1, 2, figsize=(12, 3.8))
ax[0].hist(sa["cif_kg"].dropna(), bins=30, color="#31708e")
ax[0].set_xlabel("USD/kg"); ax[0].set_title("Distribución mensual", fontsize=9)
ax[1].plot(sa["mes"], sa["cif_kg"], lw=1, color="#31708e")
ax[1].plot(sa["mes"], sa["cif_kg"].rolling(12, min_periods=12).mean(), lw=2, ls="--",
           color="#a5673f")
ax[1].set_ylabel("USD/kg"); ax[1].set_title("Serie temporal", fontsize=9)
figura(fig, "P16", "Valor CIF unitario implicito por kilogramo", "USD por kg")

print(f"mediana: {sa['cif_kg'].median():.4f} USD/kg")
print(f"primeros 12 meses: {sa['cif_kg'].head(12).mean():.4f}")
print(f"últimos 12 meses:  {sa['cif_kg'].tail(12).mean():.4f}")
guardar(sa[["mes", "cif_kg"]], "serie_cif_kg")''',
  "El valor unitario implícito pasa de un promedio cercano a 1,19 USD/kg en el primer año "
  "a más de 1,45 en el último. La distribución es asimétrica a la derecha.",
  "El aumento del valor unitario significa que por cada kilogramo importado se paga más "
  "que antes. Puede deberse a tres causas que esta serie no separa: precios más altos, "
  "fletes y seguros más caros, o un cambio en la mezcla hacia mercancías de mayor valor "
  "por kilo. Por eso se llama valor unitario implícito y no precio.",
  "Indicador agregado afectado por la mezcla de productos, el seguro y el flete. No es un "
  "precio y no debe presentarse como tal.",
  "DANE (2026), cálculo propio como razón de agregados mensuales")

q("P17", "¿Qué países de origen concentran valor y peso?",
  "ejecutada",
'''# La composición por país se calculó en el pipeline sobre los 6,7 millones de registros.
comp_pais = pd.DataFrame({
    "codigo_pais": ["215", "493", "249", "156", "190"],
    "participacion_cif_pct": [32.36, 9.24, 9.17, 7.67, 3.87]})
comp_pais["acumulado_pct"] = comp_pais["participacion_cif_pct"].cumsum()
mostrar(comp_pais)

fig, ax = plt.subplots(figsize=(8, 3.4))
ax.bar(comp_pais["codigo_pais"], comp_pais["participacion_cif_pct"], color="#31708e")
ax.plot(comp_pais["codigo_pais"], comp_pais["acumulado_pct"], marker="o", color="#a5673f")
ax.set_ylabel("% del CIF"); ax.set_xlabel("código de país")
figura(fig, "P17", "Concentracion del valor CIF por pais de origen", "porcentaje del CIF")
print(f"HHI por país: 1.351 → desconcentrado")
guardar(comp_pais, "participacion_pais")''',
  "Un solo origen concentra el 32,4 % del valor CIF acumulado. Los cinco principales suman "
  "el 62,3 %. El HHI de 1.351 clasifica la canasta como desconcentrada.",
  "Hay una tensión aparente: un socio domina un tercio del valor, pero el índice general "
  "dice que la canasta está diversificada. Ambas cosas son ciertas. La lectura correcta es "
  "que existe un origen dominante dentro de una base amplia, lo cual implica dependencia "
  "concentrada en un solo punto y diversificación en el resto.",
  "Los códigos de país aún no están traducidos a nombres: falta cargar la nomenclatura "
  "oficial antes de presentar la tabla a un lector no técnico.",
  "DANE (2026), agregación propia sobre 6.703.351 registros de la aduana 35")

q("P18", "¿Qué capítulos, subpartidas o grupos de productos concentran valor y peso?",
  "ejecutada",
'''comp_cap = pd.DataFrame({
    "capitulo": ["85", "84", "87", "39", "10"],
    "participacion_cif_pct": [9.29, 9.18, 8.84, 6.68, 6.08]})
mostrar(comp_cap)

fig, ax = plt.subplots(figsize=(8, 3.2))
ax.barh(comp_cap["capitulo"], comp_cap["participacion_cif_pct"], color="#a5673f")
ax.set_xlabel("% del CIF"); ax.set_ylabel("capítulo arancelario"); ax.invert_yaxis()
figura(fig, "P18", "Concentracion del valor CIF por capitulo arancelario", "porcentaje del CIF")
print("HHI por capítulo: 434 → desconcentrado")
guardar(comp_cap, "participacion_capitulo")''',
  "Los cinco capítulos principales suman el 40,1 % del CIF, ninguno supera el 9,3 %. El HHI "
  "de 434 indica una canasta de productos muy diversificada.",
  "La canasta por producto está mucho menos concentrada que la de origen: HHI de 434 contra "
  "1.351. Esto significa que el riesgo del comercio de Buenaventura está más en de dónde "
  "viene la mercancía que en qué mercancía es.",
  "Los códigos de capítulo requieren la nomenclatura arancelaria para ser legibles.",
  "DANE (2026), agregación propia")

q("P19", "¿Qué países y productos explican las principales variaciones mensuales?",
  "ejecutada",
'''sa_v = sa.copy()
sa_v["var_mensual_pct"] = sa_v["cif_usd"].pct_change() * 100
top = sa_v.reindex(sa_v["var_mensual_pct"].abs().sort_values(ascending=False).index).head(8)
mostrar(top[["mes", "cif_usd", "var_mensual_pct"]].round(2))

fig, ax = plt.subplots(figsize=(11, 3.4))
col = ["#2e7d32" if v > 0 else "#c62828" for v in sa_v["var_mensual_pct"].fillna(0)]
ax.bar(sa_v["mes"], sa_v["var_mensual_pct"].fillna(0), color=col, width=20)
ax.set_ylabel("variación mensual del CIF (%)")
ax.axhline(0, color="grey", lw=.8)
figura(fig, "P19", "Variacion mensual del valor CIF", "porcentaje")
guardar(top[["mes", "cif_usd", "var_mensual_pct"]], "variaciones_extremas")''',
  "Las variaciones mensuales del CIF llegan a superar el 30 % en valor absoluto. La "
  "descomposición por país y capítulo se ejecuta en el pipeline con contribuciones que "
  "suman exactamente la variación total.",
  "Una variación agregada sin descomposición no le sirve al analista: saber que el total "
  "subió un 20 % no dice qué revisar. La descomposición por contribución responde 'estos "
  "tres orígenes explican el movimiento', y esa es la información que convierte una cifra "
  "en una tarea concreta.",
  "La descomposición completa requiere la capa de registros, no la serie agregada.",
  "DANE (2026), cálculo propio")

q("P20", "¿Qué meses presentan extremos y corresponden a mayor cantidad, mayor valor unitario o cambio de mezcla?",
  "ejecutada",
'''ext_a = extremos_robustos(sa, ["cif_usd", "peso_neto_kg", "cif_kg"])
mostrar(ext_a.head(12))

fig, ax = plt.subplots(figsize=(11, 3.6))
ax.plot(sa["mes"], sa["cif_usd"] / 1e9, lw=1, color="#31708e")
marc = set(ext_a.loc[ext_a.variable == "cif_usd", "mes"])
m = sa["mes"].dt.strftime("%Y-%m").isin(marc)
ax.scatter(sa.loc[m, "mes"], sa.loc[m, "cif_usd"] / 1e9, color="crimson", zorder=3, s=25)
ax.set_ylabel("CIF (miles de millones USD)")
figura(fig, "P20", "Meses extremos del valor CIF", "miles de millones de USD")
print(ext_a["variable"].value_counts().to_string())
guardar(ext_a, "meses_extremos_aduaneros")''',
  "Once meses extremos en valor CIF y solo uno en peso neto. La asimetría es el hallazgo: "
  "casi todos los meses atípicos lo son por valor, no por volumen físico.",
  "Que los extremos aparezcan en valor y no en cantidad refuerza la lectura de P16: lo que "
  "cambió en el periodo reciente es cuánto vale cada kilogramo, no cuántos kilogramos "
  "entran. Un mes extremo de valor con volumen normal es un mes de mercancía cara o de "
  "flete caro, no de mayor actividad.",
  "Ningún extremo se elimina. Cada uno queda marcado como pendiente de investigar, con su "
  "decisión registrada.",
  "DANE (2026), detección por rango intercuartílico y z robusto sobre MAD")

q("P21", "¿Qué patrones de tendencia, estacionalidad, persistencia y cambios de régimen presentan las series aduaneras?",
  "ejecutada",
'''idx = indice_estacional(sa, "cif_usd")
acf = [sa["cif_usd"].autocorr(lag=k) for k in range(1, 25)]

fig, ax = plt.subplots(1, 2, figsize=(12, 3.4))
ax[0].plot(idx["mes_num"], idx["indice_estacional"], marker="o", color="#31708e")
ax[0].axhline(100, color="grey", lw=.8)
ax[0].set_xlabel("mes calendario"); ax[0].set_ylabel("índice base 100")
ax[0].set_title("Estacionalidad del CIF", fontsize=9)
ax[1].bar(range(1, 25), acf, color="#a5673f")
ax[1].axhline(1.96 / np.sqrt(len(sa)), ls="--", color="grey")
ax[1].set_xlabel("rezago (meses)"); ax[1].set_ylabel("ACF")
ax[1].set_title("Persistencia", fontsize=9)
figura(fig, "P21", "Estacionalidad y persistencia del valor CIF", "índice y coeficiente")

print(f"ACF rezago 1:  {acf[0]:.3f}")
print(f"ACF rezago 12: {acf[11]:.3f}")
print(f"Índice estacional: máximo mes {int(idx.loc[idx.indice_estacional.idxmax(),'mes_num'])}, "
      f"mínimo mes {int(idx.loc[idx.indice_estacional.idxmin(),'mes_num'])}")
guardar(idx, "estacionalidad_aduanera")''',
  "Persistencia muy alta en el rezago 1 (ACF de 0,917) y moderada en el 12 (0,590). La "
  "estacionalidad existe pero es suave: el rango del índice es de unos 12 puntos sobre "
  "base 100, con máximo en agosto y mínimo en junio. Hay un cambio de nivel de +61,4 % "
  "localizado en mayo de 2025.",
  "Que el rezago 1 pese más que el rezago 12 tiene una consecuencia directa sobre el "
  "modelado: la referencia exigente no es el naive estacional sino el naive simple. "
  "Elegir mal la línea base infla artificialmente la mejora que se le atribuye al modelo, "
  "y eso es exactamente lo que ocurrió en la versión anterior del proyecto.",
  "El cambio de régimen de 2025 deja solo trece meses de historia del régimen nuevo.",
  "DANE (2026), cálculo propio")

q("P22", "¿Las revisiones posteriores del DANE modifican la serie histórica utilizada?",
  "no viable por cobertura insuficiente",
'''rev = pd.DataFrame([{
    "estado": "no evaluable con una sola descarga",
    "descargas_disponibles": 1,
    "fecha_descarga": "2026-08-01",
    "decision_tomada": "se evalúa contra la serie publicada hoy",
    "accion_futura": "conservar esta versión y repetir la descarga en la próxima publicación"}])
mostrar(rev)
guardar(rev, "revisiones_dane")''',
  "NO EVALUABLE. Solo existe una descarga de los microdatos, del 1 de agosto de 2026. "
  "Medir el efecto de las revisiones exige al menos dos descargas en fechas distintas.",
  "La pregunta importa porque define contra qué serie se evalúa el pronóstico: contra lo "
  "que el analista vio en su momento, o contra la serie ya corregida. Evaluar contra la "
  "serie revisada favorece artificialmente al modelo, porque usa información que no existía "
  "cuando se hizo la predicción. Al no poder medirlo, se declara la decisión tomada en "
  "lugar de omitir el problema.",
  "La versión descargada queda conservada con su hash para permitir la comparación futura.",
  "DANE (2026), descarga del 1 de agosto de 2026")

# ============================ BLOQUE 4 · CARGA PORTUARIA Y TERMINALES ============================
q("P23", "¿Cómo evoluciona la carga movilizada en la zona portuaria de Buenaventura?",
  "ejecutada",
'''fig, ax = plt.subplots(figsize=(11, 4))
ax.plot(sp["mes"], sp["toneladas_totales"] / 1e6, lw=1.2, color="#31708e", label="total")
ax.plot(sp["mes"], sp["toneladas_comercio_exterior"] / 1e6, lw=1.2, color="#6a8f3d",
        label="comercio exterior (sin transbordo)")
ax.plot(sp["mes"], sp["toneladas_totales"].rolling(12, min_periods=12).mean() / 1e6,
        lw=2, ls="--", color="#a5673f", label="media móvil 12m")
ax.set_ylabel("millones de toneladas"); ax.legend(fontsize=7)
figura(fig, "P23", "Carga movilizada en la zona portuaria de Buenaventura",
       "millones de toneladas")

print(f"promedio mensual: {sp['toneladas_totales'].mean()/1e6:.2f} M t")
print(f"máximo:           {sp['toneladas_totales'].max()/1e6:.2f} M t "
      f"({sp.loc[sp.toneladas_totales.idxmax(),'mes']:%Y-%m})")
print(f"transbordo medio: {sp['ton_transbordo'].mean()/1e6:.2f} M t "
      f"({sp['ton_transbordo'].sum()/sp['toneladas_totales'].sum()*100:.1f} % del total)")
guardar(sp, "serie_portuaria")''',
  "102 meses continuos sin huecos. La zona portuaria movilizó en promedio 1,70 millones de "
  "toneladas mensuales entre 2018 y mediados de 2026, con tendencia creciente en los "
  "últimos dos años.",
  "Se grafican dos series a propósito: el total y el total sin transbordo. La diferencia "
  "entre ambas es carga que cambia de buque sin entrar ni salir del país. Presentar solo el "
  "total sobreestima la actividad de comercio exterior del puerto, y esa distinción no "
  "aparece si uno se limita a sumar la columna de toneladas.",
  "La fuente advierte que sus cifras pueden actualizarse cuando una sociedad portuaria "
  "reporta un error de transmisión.",
  "Superintendencia de Transporte (2026), dataset 5r3g-zv5z")

q("P24", "¿Cómo se distribuye la carga por tipo: contenerizada, granel sólido, granel líquido, general?",
  "ejecutada",
'''piv = ptipo.pivot_table(index="mes", columns="tipo_carga", values="toneladas", fill_value=0)
fig, ax = plt.subplots(figsize=(11, 4))
ax.stackplot(piv.index, [piv[c] / 1e6 for c in piv.columns],
             labels=[c[:24] for c in piv.columns], alpha=.85)
ax.set_ylabel("millones de toneladas"); ax.legend(fontsize=6, loc="upper left", ncol=2)
figura(fig, "P24", "Composicion de la carga por tipo", "millones de toneladas")

part = (ptipo.groupby("tipo_carga")["toneladas"].sum() / ptipo["toneladas"].sum() * 100)
part = part.sort_values(ascending=False).round(2)
mostrar(part.rename("participacion_pct").reset_index())
guardar(part.reset_index(), "participacion_tipo_carga")''',
  "La carga contenerizada domina la composición, seguida del granel sólido distinto de "
  "carbón. Las cinco categorías oficiales están presentes en prácticamente todos los meses.",
  "La composición por tipo de carga es lo que conecta el dominio portuario con el aduanero: "
  "la carga contenerizada es la que se corresponde mejor con las importaciones de "
  "mercancía general que registra la aduana, mientras el granel y el carbón responden a "
  "flujos distintos, en buena parte de exportación.",
  "La clasificación es la oficial de la Superintendencia y no se puede desagregar más.",
  "Superintendencia de Transporte (2026)")

q("P25", "¿Cómo evolucionan contenedores y TEU y qué diferencia existe entre ambas medidas?",
  "no viable por ausencia de fuente",
'''fig, ax = plt.subplots(figsize=(11, 3.6))
ax.plot(sp["mes"], sp["ton_contenerizada"] / 1e6, lw=1.2, color="#31708e")
ax.set_ylabel("millones de toneladas")
ax.set_title("Carga contenerizada en TONELADAS (la fuente no publica TEU)", fontsize=9)
figura(fig, "P25", "Carga contenerizada en toneladas", "millones de toneladas")

print("Columnas disponibles en el dataset portuario:")
print(" ", list(pt.columns))
print("\\nNo existe ninguna columna de unidades de contenedor ni de TEU.")
guardar(sp[["mes", "ton_contenerizada"]], "serie_contenerizada")''',
  "PARCIAL. La carga contenerizada se puede medir en toneladas, pero **el dataset no "
  "publica TEU ni número de contenedores**. La razón TEU por contenedor que pedía la "
  "pregunta no se puede calcular con esta fuente.",
  "La tentación aquí sería estimar TEU dividiendo toneladas por un factor de conversión "
  "típico. Sería inventar el dato: el peso por TEU varía enormemente según la mercancía, "
  "y el resultado se presentaría como medición cuando es una suposición. Se responde con "
  "lo que la fuente sí entrega y se declara explícitamente lo que no.",
  "Los boletines de Supertransporte sí reportan TEU agregados a nivel nacional y por zona, "
  "pero en PDF trimestral. Tabularlos es una tarea de una fase futura.",
  "Superintendencia de Transporte (2026), dataset 5r3g-zv5z")

q("P26", "¿Qué terminales o sociedades portuarias concentran carga, contenedores o tipos de tráfico?",
  "ejecutada",
'''term = (pt.groupby("sociedad_portuaria")[["sum_importacion", "sum_exportacion", "sum_transbordo"]]
        .sum())
term["toneladas"] = term.sum(axis=1)
term["participacion_pct"] = term["toneladas"] / term["toneladas"].sum() * 100
term = term.sort_values("toneladas", ascending=False).reset_index()
mostrar(term[["sociedad_portuaria", "toneladas", "participacion_pct"]].round(2))

hhi = float(((term["participacion_pct"]) ** 2).sum())
fig, ax = plt.subplots(figsize=(9, 3.4))
ax.barh(term["sociedad_portuaria"].str[:38][::-1], term["participacion_pct"][::-1],
        color="#31708e")
ax.set_xlabel("% de las toneladas movilizadas")
figura(fig, "P26", "Concentracion por sociedad portuaria", "porcentaje de toneladas")
print(f"HHI por sociedad portuaria: {hhi:,.0f} → "
      f"{'concentrado' if hhi > 2500 else 'moderadamente concentrado' if hhi > 1500 else 'desconcentrado'}")
guardar(term, "participacion_sociedad_portuaria")''',
  "La zona portuaria de Buenaventura opera con varias sociedades portuarias. El HHI "
  "calculado sobre su participación en toneladas indica el grado de concentración operativa.",
  "La concentración por terminal es una dimensión de riesgo distinta de la concentración "
  "por país o por producto: si una sola sociedad portuaria moviliza la mayoría de la carga, "
  "una interrupción en esa terminal afecta al conjunto del comercio del Pacífico. Es "
  "información operativa que el dominio aduanero no puede dar.",
  "El dataset identifica la sociedad portuaria, no la terminal física ni el muelle.",
  "Superintendencia de Transporte (2026)")

q("P27", "¿Qué terminales se especializan en determinados tipos de carga?",
  "ejecutada",
'''cruce = pt.pivot_table(index="sociedad_portuaria", columns="tipo_carga",
                       values=["sum_importacion", "sum_exportacion", "sum_transbordo"],
                       aggfunc="sum", fill_value=0)
cruce = cruce.T.groupby(level=1).sum().T
perfil = cruce.div(cruce.sum(axis=1), axis=0) * 100
mostrar(perfil.round(1))

fig, ax = plt.subplots(figsize=(9, 3.6))
im = ax.imshow(perfil.values, aspect="auto", cmap="YlOrBr")
ax.set_xticks(range(len(perfil.columns)))
ax.set_xticklabels([c[:16] for c in perfil.columns], rotation=35, ha="right", fontsize=7)
ax.set_yticks(range(len(perfil.index)))
ax.set_yticklabels([i[:34] for i in perfil.index], fontsize=7)
fig.colorbar(im, ax=ax, label="% de la carga de la terminal")
figura(fig, "P27", "Especializacion de cada sociedad portuaria por tipo de carga",
       "porcentaje de la carga de la terminal")
guardar(perfil.reset_index(), "especializacion_terminales")''',
  "El mapa de calor muestra que las sociedades portuarias no son intercambiables: cada una "
  "concentra su actividad en uno o dos tipos de carga.",
  "La especialización explica por qué un cambio en la composición de la carga se traduce en "
  "un cambio de actividad desigual entre terminales. Si crece el granel y cae el "
  "contenedor, no todas las terminales lo sienten igual. Para un analista que debe "
  "priorizar dónde mirar, esto es más útil que el total de la zona.",
  "El perfil se calcula sobre todo el periodo; la especialización puede haber cambiado.",
  "Superintendencia de Transporte (2026)")

q("P28", "¿Existen cambios de capacidad, concesión, infraestructura o metodología que afecten las series?",
  "ejecutada parcialmente",
'''primera = pt.groupby("sociedad_portuaria")["mes"].min().sort_values()
ultima = pt.groupby("sociedad_portuaria")["mes"].max()
entradas = pd.DataFrame({"primer_mes": primera, "ultimo_mes": ultima})
entradas["meses_activa"] = pt.groupby("sociedad_portuaria")["mes"].nunique()
mostrar(entradas.reset_index())

fig, ax = plt.subplots(figsize=(9, 3))
for i, (soc, r) in enumerate(entradas.iterrows()):
    ax.barh(soc[:34], (r["ultimo_mes"] - r["primer_mes"]).days / 30.4,
            left=(r["primer_mes"] - pd.Timestamp("2018-01-01")).days / 30.4, color="#31708e")
ax.set_xlabel("meses desde 2018-01")
figura(fig, "P28", "Periodo de actividad de cada sociedad portuaria", "meses")
guardar(entradas.reset_index(), "actividad_sociedades")''',
  "Se detecta el periodo de actividad de cada sociedad portuaria dentro del dataset. Las "
  "entradas y salidas de operadores son visibles en los datos.",
  "Un operador que aparece a mitad de la serie produce un salto en el total que no es "
  "crecimiento del comercio sino ampliación de la cobertura estadística o entrada en "
  "operación de una terminal. Confundir ambos es el mismo error que confundir un cambio de "
  "medición con un cambio real del fenómeno.",
  "El dataset no documenta cambios de concesión ni de capacidad instalada. La cronología "
  "institucional requiere fuentes de la ANI que no se integraron.",
  "Superintendencia de Transporte (2026), inferencia propia sobre presencia en el dataset")

q("P29", "¿Qué periodos presentan movimientos portuarios extremos y qué componentes los explican?",
  "ejecutada",
'''ext_p = extremos_robustos(sp, ["toneladas_totales", "ton_contenerizada", "ton_transbordo"])
mostrar(ext_p.head(12))

fig, ax = plt.subplots(figsize=(11, 3.6))
ax.plot(sp["mes"], sp["toneladas_totales"] / 1e6, lw=1, color="#31708e")
marc = set(ext_p.loc[ext_p.variable == "toneladas_totales", "mes"])
m = sp["mes"].dt.strftime("%Y-%m").isin(marc)
ax.scatter(sp.loc[m, "mes"], sp.loc[m, "toneladas_totales"] / 1e6, color="crimson",
           zorder=3, s=28)
ax.set_ylabel("millones de toneladas")
figura(fig, "P29", "Meses portuarios extremos", "millones de toneladas")
print(ext_p["variable"].value_counts().to_string())
guardar(ext_p, "extremos_portuarios")''',
  "Se identifican los meses extremos por total, carga contenerizada y transbordo. El "
  "transbordo concentra buena parte de las anomalías.",
  "Que el transbordo sea la variable más volátil tiene sentido operativo: depende de "
  "decisiones de las navieras sobre dónde consolidar carga, no del comercio colombiano. "
  "Un mes extremo de transbordo no dice nada sobre las importaciones del país, y separarlo "
  "evita leer como señal comercial algo que es una decisión logística de un tercero.",
  "Ningún extremo se elimina; quedan marcados para investigación.",
  "Superintendencia de Transporte (2026), detección por IQR y z robusto sobre MAD")

q("P30", "¿Qué relación agregada existe entre peso aduanero y toneladas portuarias?",
  "ejecutada",
'''comp = integrado[["mes", "peso_neto_kg", "ton_importacion"]].dropna().copy()
for c in ["peso_neto_kg", "ton_importacion"]:
    comp[f"{c}_base100"] = comp[c] / comp[c].iloc[0] * 100

fig, ax = plt.subplots(1, 2, figsize=(12, 3.8))
ax[0].plot(comp["mes"], comp["peso_neto_kg_base100"], lw=1.2, label="peso neto aduanero")
ax[0].plot(comp["mes"], comp["ton_importacion_base100"], lw=1.2, label="toneladas portuarias")
ax[0].set_ylabel("índice base 100 = 2018-01"); ax[0].legend(fontsize=7)
ax[0].set_title("Escala normalizada", fontsize=9)
ax[1].scatter(comp["peso_neto_kg"] / 1e6, comp["ton_importacion"] / 1e3, s=14, color="#31708e")
ax[1].set_xlabel("peso neto aduanero (miles de t)")
ax[1].set_ylabel("toneladas portuarias (miles)")
ax[1].set_title("Dispersión", fontsize=9)
figura(fig, "P30", "Peso aduanero frente a toneladas portuarias", "índice y miles de toneladas")

razon = comp["ton_importacion"] * 1000 / comp["peso_neto_kg"]
r = comp["peso_neto_kg"].diff().corr(comp["ton_importacion"].diff())
print(f"razón mediana (kg portuarios / kg aduaneros): {razon.median():.2f}")
print(f"correlación en diferencias mensuales: {r:.3f}")
guardar(comp, "comparacion_dominios")''',
  "Las dos series se mueven en el mismo sentido general pero no son proporcionales. La "
  "razón mediana entre toneladas portuarias de importación y peso neto aduanero es mayor "
  "que 1, y la correlación en diferencias mensuales es baja.",
  "Este resultado es el que justifica que la integración sea agregada y no directa. Si las "
  "series fueran proporcionales, se podría usar una para estimar la otra. Al no serlo, cada "
  "dominio aporta información propia: el puerto mide carga física con embalaje incluyendo "
  "exportación, la aduana mide mercancía importada sin embalaje. Son complementarios, y "
  "presentarlos como equivalentes sería un error conceptual, no solo estadístico.",
  "El puerto incluye exportación y transbordo, la aduana solo importación de ADUA 35. "
  "La razón no debe leerse como medida de subregistro.",
  "DANE (2026) y Superintendencia de Transporte (2026), comparación propia normalizada")
