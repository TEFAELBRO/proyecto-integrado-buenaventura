# Cómo ejecutar el EDA de 52 preguntas en Google Colab

1. Subir a Colab `EDA_52_Preguntas_Buenaventura_V5.ipynb`.
2. Subir también la carpeta `datos_colab/` (3 archivos, 41 KB en total).
3. Ejecutar todas las celdas: `Entorno de ejecución → Ejecutar todo`.

## Qué hace cada cosa

| Celda | Contenido |
|---|---|
| Preparación | Detecta Colab, instala dependencias y crea `salidas_eda/` |
| Utilidades | `figura()` imprime unidad, periodo, fuente y corte al pie de cada gráfico |
| Carga | Descarga el dominio portuario **en vivo** de datos.gov.co; carga el aduanero del repo |
| Evaluación | Backtest walk-forward y cobertura conformal |
| P01 a P52 | Enunciado → código → gráfico → respuesta → explicación → limitación |
| Cierre | Matriz de trazabilidad y conteo por estado |

## Con y sin internet

Con conexión, el cuaderno descarga la desagregación por **sociedad portuaria** y responde
P26 y P27 completas.

Sin conexión, cae al respaldo local, que solo trae tipo de carga. En ese caso **P26 y P27
declaran modo degradado y no calculan**, en lugar de imprimir un HHI de 10.000 que no
mide concentración sino ausencia de desagregación.

## Salidas

Al terminar quedan en `salidas_eda/`:

- una figura por pregunta que lo requiere, con su pie completo;
- un CSV por resultado numérico;
- `matriz_trazabilidad_eda.csv` con el estado de las 52.

## Estados posibles

| | Estado | Cuántas |
|---|---|---|
| 🟢 | ejecutada | 36 |
| 🟡 | ejecutada parcialmente | 4 |
| 🔴 | no viable por ausencia de fuente | 11 |
| 🔴 | no viable por cobertura insuficiente | 1 |

Las once no viables corresponden al bloque marítimo y operativo. **No son preguntas sin
responder**: cada una documenta dónde se buscó, qué se encontró y qué fuente haría falta.
