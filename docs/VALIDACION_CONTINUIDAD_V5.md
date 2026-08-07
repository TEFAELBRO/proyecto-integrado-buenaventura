# Validación de continuidad sobre la V5 existente

6 de agosto de 2026 · Principio aplicado: **modificación mínima sobre lo que ya funciona**

Ningún componente se renombró por parecerse a un nombre del prompt. Solo se tocó lo que
tenía un **defecto demostrado**, y cada cambio se validó antes de pasar al siguiente.

---

## Etapa 1 · Diagnóstico del estado real

### Lo que ya estaba y funcionaba — no se tocó

| Componente | Estado | Decisión |
|---|---|---|
| `src/config.py` con `RAIZ = Path(__file__).parents[1]` | funciona en local y en clon | **conservar** |
| Capas `RAW`, `LANDING`, `TRUSTED`, `SURFACE` | centralizadas, sin rutas absolutas | **conservar** |
| `src/comun/` con 14 módulos heredados de V4 | funcionan | **conservar nombres** |
| `src/puertos.py`, `src/integracion.py` | nuevos y funcionando | **conservar** |
| `src/correr_integrado.py` | orquesta las 52 preguntas | **conservar** |
| `dashboard/app.py` con seis vistas | funciona | **conservar** |
| `EDA_52_Preguntas_Buenaventura_V5.ipynb` | 58 celdas, 0 errores | **conservar** |
| `docs/preguntas_v5.csv` | catálogo congelado P01–P52 | **conservar** |
| Cero rutas absolutas en todo el código | verificado por búsqueda | **nada que corregir** |

### Equivalencias con la plantilla institucional — documentadas, no trasladadas

| Plantilla | V5 | Justificación |
|---|---|---|
| `webapp/` | `dashboard/` | Destino institucional cumplido por el módulo técnico |
| `reportes/` | `reports/` | Salida institucional cumplida por el módulo interno |
| `src/0X_*.ipynb` | `src/correr_*.py` + `notebooks/` | La lógica vive en módulos probados; los cuadernos orquestan |

No se movió ninguna carpeta. La equivalencia es válida y queda registrada.

### Defectos demostrados

| Componente | Estado | Problema identificado | Cambio mínimo | Resultado esperado | Prueba de validación |
|---|---|---|---|---|---|
| `tests/` | **vacío** | Los 14 módulos heredados no tenían ninguna prueba en V5; V4 tenía 80 | Copiar las 8 suites y reapuntar `from src import x` a `from src.comun import x` | 80 pruebas en verde | `pytest tests -q` |
| `src/config.py` | incompleto | No define `DERIVADA`, `OBJETIVOS`, `COLUMNAS_CANONICAS` ni `CODIGOS_TEXTO`, que `src/comun/series.py` y `auditoria.py` esperan | Añadir esas constantes con **el mismo nombre que en V4** | `series.agregar_cif_kg` deja de fallar | `pytest tests/test_series_y_eda.py` |
| `src/comun/trazabilidad.py` | ruta rota | Apunta a `docs/preguntas_p01_p52.csv`, nombre de V4 que no existe en V5 | Leer `config.CATALOGO_PREGUNTAS`, con respaldo al nombre V5 | El Trazador carga las 52 preguntas de V5 | `pytest tests/test_trazabilidad.py` |
| `.gitignore` | **rompe el clon** | `data/raw/*` excluía 117 KB de datos que el pipeline necesita: un clon de GitHub no ejecutaba | Excluir solo lo pesado (`*.zip`, `*.7z`); versionar los CSV pequeños | Un clon corre el pipeline completo | Clon simulado + `correr_integrado` |
| `notebooks/datos_colab/` | duplicación | 4 archivos existían también en `data/raw/` | Borrar los duplicados; el cuaderno ya resuelve rutas | Una sola ubicación canónica por archivo | Ejecución del cuaderno |
| `src/config.py` | sin Colab ni Drive | El paquete no detectaba Colab ni permitía datos persistentes | Ampliar el **mismo** config con `en_colab()`, `usar_datos_en()` y `montar_drive()` | Datos persistentes sin un segundo sistema de rutas | Prueba de reapuntado con hash |
| `notebooks/` | sin arranque | No había cuaderno de preparación de entorno | Añadir `00_entorno.ipynb` | Clon, dependencias, Drive y prueba mínima | Ejecución de la prueba mínima |

---

## Etapas 2 a 6 · Cambios aplicados y validados

### Cambio 1 — Migrar las pruebas

**Antes:** `tests/` vacío. Los módulos heredados sin cobertura. Riesgo: un cambio en
`src/comun` rompe algo sin que nadie se entere.

**Después:** 8 archivos, **80 pruebas en verde**. La migración destapó de inmediato los
dos defectos latentes de `config.py` y `trazabilidad.py`, que llevaban horas ahí sin dar
la cara porque `correr_integrado.py` no usaba esas rutas de código.

`test_trazabilidad.py` se reescribió: el mecanismo es el mismo, pero validaba contenido
propio de V4 (preguntas restauradas, P51/P52 separadas). Ahora valida el catálogo de V5,
incluida la comprobación de que el bloque marítimo declara su inviabilidad de antemano.

**Efecto secundario:** ninguno. El pipeline sigue dando 38 ejecutadas, 10 no viables y
4 parciales.

### Cambio 2 — `.gitignore`

**Antes:** 15 archivos excluidos, de los cuales **10 eran necesarios para ejecutar**.
Un `git clone` producía un repositorio que no corría.

**Después:** 0 archivos críticos excluidos. Se sigue excluyendo lo pesado: los ZIP del
DANE (8,7 GB) viven fuera del repositorio y se documentan en el manifiesto.

**Validación:** clon simulado de 84 archivos → módulos importan, 80 pruebas pasan,
pipeline completo corre y reproduce las mismas 34 salidas y los mismos 101 meses
integrados.

### Cambio 3 — Duplicación

**Antes:** `trafico_portuario_buenaventura.csv`, `terminales_por_anio.csv`,
`terminales_por_tipo_carga.csv` y `variables_externas_mensuales.csv` existían en dos
rutas. Riesgo real: editar una copia y no la otra.

**Después:** una sola ubicación canónica por archivo. `datos_colab/` conserva únicamente
`serie_aduanera_mensual.csv`, que es una exportación en CSV que no existe en otro sitio y
evita depender de pyarrow en Colab.

**Efecto secundario detectado por la prueba integral:** el cuaderno dejó de encontrar
`variables_externas_mensuales.csv` porque su lista de rutas no incluía `data/raw/contexto`.
**Corregido**: la lista pasó de 6 a 12 ubicaciones. Revalidado en los dos casos de uso —
ejecutando desde la raíz del repositorio y desde `notebooks/` — con **0 errores en ambos**.

Este es el motivo por el que la etapa 6 existe: el cambio 3 se veía correcto por sí solo y
rompía algo a distancia.

### Cambio 4 — Colab y Drive

**Antes:** solo el cuaderno del EDA detectaba Colab. El paquete `src/` no, y no había
manera de persistir datos entre sesiones.

**Después:** el **mismo** `src/config.py` gana tres funciones. `usar_datos_en()` reasigna
las constantes que ya usaba todo el pipeline; no introduce nombres nuevos ni un segundo
juego de rutas. `montar_drive()` monta Drive y llama a la anterior. La variable de entorno
`BUENAVENTURA_DATA` permite fijar la ubicación sin tocar código.

**Validación con Drive simulado:**

1. rutas reapuntadas y todas las capas siguiéndolas;
2. lectura desde la nueva ubicación: 508 filas;
3. escritura de un parquet de prueba: 8.450 bytes;
4. **hash estable tras relectura** y contenido idéntico;
5. el archivo quedó en la capa `trusted`, no en otra;
6. rutas restauradas al terminar.

### Cambio 5 — Cuaderno de arranque

`00_entorno.ipynb`, aditivo: clona el repositorio en Colab, resuelve la raíz buscando
`src/` hacia arriba, instala desde `requirements.txt`, monta Drive de forma opcional,
corre una prueba mínima e invoca las pruebas y el pipeline.

---

## Etapa 6 · Ejecución integral

| Comprobación | Resultado |
|---|---|
| Pruebas automatizadas | **80 en verde** |
| Calidad de código (`ruff`) | **sin hallazgos** |
| Pipeline `correr_integrado` | 38 ejecutadas · 10 no viables · 4 parciales |
| Meses integrados | 101 (2018-01 a 2026-05) |
| Cuaderno del EDA desde la raíz | **0 errores** · 42 figuras · 54 CSV |
| Cuaderno del EDA desde `notebooks/` | **0 errores** · 42 figuras |
| Clon limpio de GitHub | importa, prueba y ejecuta |
| Drive simulado | lectura, escritura y hash verificados |
| Trazabilidad | 52 preguntas · **0 sin evidencia ni justificación** |
| **V4** | **80 pruebas en verde, 52/52, intacto** |
| Originales y plantilla institucional | **sin modificar** |

---

## Qué del prompt no aplicaba

**Renombrar a `CODE_ROOT`, `DATA_ROOT`, `RAW_DIR`, `REPORTS_DIR`.** V5 ya tiene `RAIZ`,
`DATA`, `RAW` y `REPORTS`, centralizados y sin rutas absolutas. Renombrarlos habría
tocado 18 módulos y 8 suites de pruebas sin resolver ningún defecto. Se conservan.

**Mover `dashboard` a `webapp` y `reports` a `reportes`.** La equivalencia ya estaba
documentada y la plantilla se cumple. Mover carpetas habría roto los imports del
dashboard y las rutas de figuras a cambio de nada.

**Crear los siete notebooks `00` a `06` del prompt V5.** La lógica vive en módulos
probados con 80 pruebas; los cuadernos que sí aportan valor propio son el de entorno y el
del EDA, y ambos existen. Fragmentar el pipeline en siete cuadernos habría movido código
probado a celdas sin pruebas.

**Reconstruir desde cero.** Explícitamente descartado por la regla de continuidad.
