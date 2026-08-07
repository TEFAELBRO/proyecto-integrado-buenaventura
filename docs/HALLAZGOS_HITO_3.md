# Hallazgos del hito 3 — EDA completo y objetivos predictivos

Proyecto integrado de Buenaventura, versión 5 · 6 de agosto de 2026

Todas las cifras de este documento provienen de `salidas_eda/` o de `data/surface/`.
Ninguna está escrita a mano.

---

## 0. Nota de versión

Actualizado el 6 de agosto de 2026 tras la auditoría del EDA y del documento. Se corrigió
el HHI portuario (3.514, calculado sobre participaciones sin redondear), se aisló el año
parcial 2026, se retiraron las inferencias sobre capacidad de sustitución y se incorporó
la descomposición del tráfico portuario.

---

## 1. El resultado que refuta la hipótesis del proyecto

La versión 5 partía de una idea implícita: **integrar dominios mejoraría el pronóstico**.
La ablación multidominio dice que no.

Objetivo `cif_usd`, 24 cortes de backtest walk-forward, 89 filas utilizables:

| Conjunto de variables | Variables | WAPE | Ganancia frente a A |
|---|---|---|---|
| **B · historia propia + calendario** | 7 | **5,875 %** | **+0,207 pp** |
| A · historia propia | 5 | 6,082 % | — |
| D · A + contexto (TRM, ONI) | 9 | 6,133 % | −0,051 pp |
| E · integrado completo | 16 | 6,167 % | −0,085 pp |
| **C · A + PUERTO** | 10 | **6,575 %** | **−0,493 pp** |
| base · drift | 0 | 6,905 % | −0,823 pp |
| base · naive 1 | 0 | 6,956 % | −0,874 pp |
| base · naive 12 | 0 | 16,487 % | −10,405 pp |

**Añadir variables portuarias empeora el pronóstico del CIF en medio punto de WAPE.**
El modelo integrado completo tampoco mejora sobre la historia propia.

### Por qué ocurre

Ambas fuentes miden el mismo comercio subyacente y comparten el mismo rezago de
publicación. El puerto no aporta información que la historia del propio CIF no contenga ya,
y sí consume grados de libertad sobre una muestra corta. Es el mismo mecanismo por el que
la TRM y el ONI tampoco aportaron en el dominio aduanero.

### Qué significa para el producto

**El valor de la integración no es predictivo: es explicativo.** Sirve para responder si un
mes cambió por valor o por volumen físico, y para localizar por qué sociedad portuaria pasa la carga.
Presentarla como una mejora del pronóstico sería afirmar lo contrario de lo que se midió.

Las cinco configuraciones sí superan a las tres líneas base, de modo que el modelo aporta
sobre no hacer nada. Lo que no aporta es la integración.

---

## 2. La zona portuaria está concentrada

| Sociedad portuaria | Participación 2018–2026 |
|---|---|
| Sociedad Portuaria Regional de Buenaventura | **51,36 %** |
| Sociedad Puerto Industrial Aguadulce | 25,28 % |
| Sociedad Portuaria Terminal de Contenedores de Buenaventura | 13,73 % |
| Grupo Portuario | 6,01 % |
| Compañía de Puertos Asociados | 3,62 % |

**HHI global: 3.514** — muy por encima del umbral de 2.500 que marca concentración.

Evolución anual del HHI:

| Año | HHI | Sociedades que reportan |
|---|---|---|
| 2018 | 4.722 | 5 |
| 2020 | 3.231 | 5 |
| **2023** | **2.988** | 5 |
| 2025 | 3.740 | 5 |
| 2026 (6 meses) | 4.217 | **3** |

Entre los **años completos**, el índice bajó de 4.722 en 2018 a 2.988 en 2023 y subió a
3.740 en 2025. El valor de 2026 **no es comparable**: cubre seis meses y solo tres
sociedades reportan. Recalculando 2025 con esas mismas tres, el índice sería 4.096, de
modo que la mayor parte del salto se explica por el cambio de cobertura del reporte y no
por una redistribución entre las que continúan.

### El contraste que solo se ve integrando

| Dimensión | HHI | Lectura |
|---|---|---|
| Capítulo arancelario | 434 | desconcentrado |
| País de origen | 1.351 | desconcentrado |
| **Sociedad portuaria** | **3.514** | **concentrado** |

Buenaventura importa mercancía variada desde orígenes variados, **pero la mueve por muy
pocas sociedades portuarias**. Ninguna de las dos fuentes por separado permite
observar ese contraste. El índice mide reparto de toneladas reportadas: no mide capacidad
instalada, utilización ni posibilidad real de sustitución.

---

## 3. La especialización matiza la concentración

| Sociedad | Contenedores | Granel sólido | General | Granel líq. | Carbón |
|---|---|---|---|---|---|
| TCBUEN | **100 %** | — | ~0 % | — | — |
| Aguadulce | 66 % | 20 % | 6 % | 0,2 % | 8 % |
| SPR Buenaventura | 55 % | 34 % | 11 % | 5 % | — |
| Grupo Portuario | — | 51 % | — | — | 49 % |
| Cía. de Puertos Asociados | — | **100 %** | — | — | — |

El índice de concentración trata a las sociedades como si fueran intercambiables, y el
cruce muestra que no movilizan lo mismo: TCBUEN no registró toneladas de granel en el
periodo y Compañía de Puertos Asociados no registró contenedores. **El reparto agregado
describe cuánto movilizó cada una, no si podrían movilizar la carga de las demás**: la
fuente no contiene capacidad instalada ni utilización.

---

## 4. Dos sociedades no aparecen reportando en 2026

Grupo Portuario cae de cerca de 1,5 millones de toneladas anuales a **3.630 en 2025** y
no aparece en los seis meses observados de 2026. Compañía de Puertos Asociados reporta hasta 2025 y tampoco aparece.

**Verificación:** se consultó mes a mes. En los seis meses de 2026 solo reportan tres
sociedades. **No es rezago de publicación.**

### Por qué importa

Un quiebre institucional en la serie no es una caída del comercio. Un modelo entrenado
sobre el total de la zona interpretaría la ausencia de dos sociedades en el reporte como una contracción
real. Antes de pronosticar el total portuario hay que decidir si se modela la zona completa
o solo las sociedades que siguen reportando.

**Limitación:** la fuente registra reporte, no operación. Los datos permiten afirmar que
dejaron de reportar, no necesariamente que dejaron de operar. La causa institucional
requiere fuentes de la ANI que no se integraron.

---

## 5. Estado de las 52 preguntas

| Estado | Cuaderno | Pipeline |
|---|---|---|
| ejecutada | 38 | 38 |
| ejecutada parcialmente | 4 | 4 |
| no viable por ausencia de fuente | 10 | 10 |
| no viable por cobertura insuficiente | — | — |
| **sin evidencia ni justificación** | **0** | **0** |

El cuaderno produce **55 figuras y 57 archivos de evidencia**, y se ejecutó de punta a
punta sin errores.

Las diez no viables son el bloque marítimo y operativo: arribos, tipos de buque, banderas,
horarios, ETA/ATA, permanencias, rankings e identificadores. Cada una documenta dónde se
buscó, qué se encontró y qué fuente haría falta.

---

## 6. Objetivos predictivos elegibles

| Indicador | Observaciones | Elegible | Modelo recomendado |
|---|---|---|---|
| `cif_usd` | 173 | sí | Ridge con historia propia + calendario |
| `peso_neto_kg` | 173 | sí | Ridge |
| `toneladas_totales` | 102 | sí | Ridge (6,61 % contra 9,17 % de naive 1) |
| `ton_contenerizada` | 102 | sí, con reserva | **Naive 1**: Ridge da 9,45 % y es peor |
| TEU | 0 | no | la fuente no lo publica |
| arribos | 0 | no | sin fuente tabular |
| permanencia media | 0 | no | sin fuente pública |

Para la carga contenerizada la recomendación es **no usar modelo**: presentarla de forma
descriptiva y, si se necesita un pronóstico, usar naive 1.

---

## 7. Qué puede y qué no puede afirmar el producto

**Puede afirmar** que el valor económico y el volumen físico del comercio de Buenaventura
se han separado en los últimos años; que la carga pasa por muy pocas sociedades portuarias altamente
especializadas; y que dos sociedades no aparecen reportando en los seis meses observados de 2026.

**No puede afirmar** nada sobre congestión, tiempos de atención, buques o sociedades portuarias
específicas asociadas a una importación concreta. Tampoco puede afirmar que integrar
dominios mejore el pronóstico, porque se midió y no lo hace.
