# Proyecto integrado de Buenaventura — versión 5

**Producto de datos que integra información aduanera y portuaria de Buenaventura**

Universidad Libre, Seccional Cali · Ingeniería del Producto de Ciencia de Datos
Juan Manuel Tejada Fajardo · Jesús Alejandro Guerrero · 2026

Construido el 6 de agosto de 2026 sobre la base metodológica de la versión 4.

---

## Qué hace y qué no hace

Integra dos dominios con fuentes oficiales verificadas, los relaciona de forma
**agregada por mes**, y pronostica únicamente los indicadores que tienen historia y
calidad suficientes.

**No construye el dominio marítimo.** Ocho de las 52 preguntas están cerradas como no
viables, con evidencia documentada de por qué. Es una respuesta válida de la
especificación V5, no una omisión.

---

## Estado de los cuatro dominios

| Dominio | Fuente | Cobertura | Estado |
|---|---|---|---|
| **Aduanero** | DANE IMPO, microdatos | 2012-01 a 2026-05 · **173 meses** | integrado |
| **Portuario** | Supertransporte `5r3g-zv5z` | 2018-01 a 2026-06 · **102 meses** | integrado |
| **Marítimo** | DIMAR | solo boletines trimestrales en PDF | **no viable** |
| **Operacional** | ETA, ATA, permanencias | sin fuente pública histórica | **no viable** |
| Contextual | TRM, ONI | 2012-01 a 2026-06 | contexto |

**Meses integrados: 101** (2018-01 a 2026-05), que es la intersección de ambos dominios.

---

## Las 52 preguntas

| Estado | Cantidad | Significado |
|---|---|---|
| ejecutada | **34** | con archivo de salida verificable |
| no viable | **10** | con evidencia documentada de por qué |
| parcial | **8** | ejecutada con limitación declarada |

Ninguna quedó sin respuesta. `data/surface/matriz_trazabilidad_eda.csv` tiene el detalle
y `data/surface/reporte_no_viabilidad.csv` justifica cada cierre.

---

## Hallazgos

### El dataset portuario es mensual, no trimestral

El diagnóstico inicial daba por hecho que Supertransporte solo publicaba boletines
trimestrales en PDF. **Es falso.** El dataset `5r3g-zv5z` de datos.gov.co entrega el dato
**mensual**, por zona portuaria, sociedad portuaria y tipo de carga, desde enero de 2018,
con licencia CC BY-SA 4.0 y descarga automatizable por API.

Eso convirtió un dominio que parecía inviable en uno con 102 observaciones mensuales.

### El puerto va por delante de la aduana

El tráfico portuario llega hasta **junio de 2026**; los microdatos aduaneros hasta
**mayo**. El puerto publica con menos rezago.

Consecuencia práctica: el dato portuario no sirve como predictor contemporáneo del CIF,
porque cuando se pronostica el CIF de un mes tampoco está publicado el puerto de ese mes.
Ambos comparten el mismo rezago de publicación.

### El modelo funciona para toneladas totales y no para carga contenerizada

Backtest walk-forward, 24 cortes:

| Indicador | Mejor modelo | WAPE | Naive 1 | ¿Gana el modelo? |
|---|---|---|---|---|
| Toneladas totales | Ridge | **6,61 %** | 9,17 % | **sí, 28 % mejor** |
| Carga contenerizada | **Naive 1** | **8,55 %** | 8,55 % | **no** |

Para la carga contenerizada, Ridge obtiene 9,45 %: **peor que repetir el último valor**.
El resultado se reporta tal cual. Un indicador que no se puede pronosticar mejor que la
referencia trivial no debe presentarse con un modelo encima.

### La integración no puede ser directa

No existe llave pública entre una declaración de importación y un movimiento de carga
portuaria. Los conceptos tampoco son equivalentes:

| | Aduanas (DANE) | Puerto (Supertransporte) |
|---|---|---|
| Unidad | declaración de importación | movimiento de carga |
| Cobertura | ADUA 35, solo importación | zona portuaria, todos los flujos |
| Peso | peso neto de la mercancía | toneladas movilizadas |
| Incluye | solo importación | importación, exportación **y transbordo** |

El transbordo es carga que cambia de buque **sin entrar ni salir del país**. Sumarlo al
comercio exterior infla el total. La serie portuaria separa ambas cosas.

---

## Estructura

```
proyecto_integrado_buenaventura/
├── data/
│   ├── raw/{aduanas,puertos,maritimo,contexto}/   fuentes inmutables con hash
│   ├── landing/ · trusted/ · surface/             30 archivos de evidencia
├── src/
│   ├── comun/        14 módulos heredados de V4 sin cambios
│   ├── config.py     nuevo: rutas y universo de fuentes
│   ├── puertos.py    nuevo: dominio portuario
│   ├── integracion.py nuevo: unión agregada y matriz de relaciones
│   └── correr_integrado.py  orquestador de las 52 preguntas
├── dashboard/app.py  seis vistas, solo lectura
├── reports/figures/  5 figuras con unidad, periodo, fuente y corte
└── docs/             catálogo de preguntas y componentes heredados
```

**Reutilización:** 14 de 18 módulos vienen de la versión 4 **sin modificar**. Métricas,
intervalos conformales, líneas base, walk-forward, hash y trazabilidad son agnósticos al
dominio: sirven igual para toneladas que para valor CIF. El detalle de qué se heredó, qué
se adaptó y qué es nuevo está en `docs/componentes_heredados.csv`.

---

## Reproducir

```bash
pip install -r requirements.txt
python -m src.correr_integrado
streamlit run dashboard/app.py
```

La descarga portuaria es reproducible con la consulta exacta documentada en
`data/raw/puertos/README_fuente.md`.

---

## Límites declarados

1. ADUA 35 es una unidad de registro administrativo, no la operación física del puerto.
2. La integración aduanera-portuaria es **agregada por mes**, nunca directa.
3. Peso neto aduanero y toneladas portuarias **no son el mismo concepto**.
4. El dataset portuario publica **toneladas, no TEU**. La razón TEU por contenedor no
   puede calcularse con esta fuente.
5. El transbordo no es comercio exterior.
6. El CIF está en dólares corrientes: parte de la variación es precio, no volumen.
7. Las alertas son señales de revisión analítica, no órdenes operativas.
8. Correlación no implica causalidad.

## Pendientes

| Pendiente | Impacto |
|---|---|
| Descargar el corte por sociedad portuaria (P26, P27) | alto para el análisis por terminal |
| Verificar y fechar las fuentes del catálogo de eventos (P41) | requisito APA |
| Ablación multidominio (P49) | justifica la integración |
| Fuente meteomarina (P40) | cierra el bloque contextual |
| Traducir códigos de país y capítulo a nombres | alto para la presentación |
| Validación con usuarios reales | la propuesta de valor sigue siendo hipótesis |
