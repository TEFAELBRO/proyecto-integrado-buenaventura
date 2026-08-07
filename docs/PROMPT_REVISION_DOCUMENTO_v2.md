# Prompt de revisión del documento académico, versión 2

Corrige tres defectos del prompt original: una instrucción que estaba basada en un
hallazgo falso, unas reservas bibliográficas innecesarias porque el metadato sí existe
en el proyecto, y la ausencia de una verificación cruzada entre el documento, el
catálogo de cifras y la presentación.

---

Actúa como revisor académico y técnico de un proyecto universitario de Ciencia de Datos.

Te entrego el documento académico final del proyecto Buenaventura V5 y el repositorio
del proyecto, cuya raíz es `proyecto_integrado_buenaventura/`.

Tu tarea es dejar el documento listo para entrega ante jurados, corrigiendo únicamente
lo que esté demostrado.

## Regla que gobierna todo lo demás

**Verifica antes de corregir.** Ninguna instrucción de esta lista se aplica por el
hecho de estar escrita aquí. Antes de tocar el documento, comprueba en el repositorio
que el defecto existe. Si la comprobación contradice la instrucción, no la apliques,
deja el documento como está y regístralo en el reporte con la evidencia que encontraste.

Esta regla existe porque una auditoría previa afirmó que
`vista_integrada_mensual.parquet` no existía y sí existe: está en `data/trusted/`, lo
escribe `src/correr_integrado.py` y `lista_cifras.csv` lo cita como origen de tres
cifras. Aplicar esa corrección habría metido un error en un documento correcto.

## Restricciones de contenido

No cambies el enfoque del proyecto. No inventes resultados, cifras, fuentes, archivos ni
metodologías. No elimines resultados negativos. No reescribas el documento completo.
Conserva estilo académico, estructura, tablas, numeración y formato.

Mantén el lenguaje prudente. No afirmes causalidad donde solo hay asociación. Conserva
«valor unitario implícito» y nunca lo cambies por «precio». Conserva que la integración
es agregada por mes calendario y nunca directa. Conserva el hallazgo de que las
variables portuarias no mejoran el pronóstico del valor CIF.

## Correcciones a evaluar

**1. Tabla 2, objetivos específicos.** Si aparece una formulación del tipo «Ejecutar las
52 preguntas y conservar la evidencia», reemplázala por «Responder o cerrar con
evidencia documentada las 52 preguntas del análisis exploratorio». El resultado real es
38 ejecutadas, 4 parciales y 10 no viables: la redacción debe dejar claro que «no
viable» es un resultado documentado y no una pregunta omitida. Conserva la evidencia
`matriz_trazabilidad_eda.csv` y el resultado sin tocarlos.

**2. Tabla 1, salidas de cada paso.** Para cada archivo citado como salida, comprueba
que existe en el repositorio y en qué capa. Si existe pero en una capa distinta de la
que un lector supondría, añade la capa entre paréntesis en lugar de cambiar el nombre.
Solo si el archivo no existe en ninguna capa, reemplaza la celda por una descripción
genérica de la salida y regístralo como corrección mayor.

**3, 4 y 5. Referencias de las fuentes de contexto y de las consultadas.** El documento
usa la tasa representativa del mercado y el índice oceánico como variables de contexto,
y menciona a DIMAR como fuente consultada para concluir la no viabilidad del dominio
marítimo. Comprueba si las tres están en la lista de referencias.

Antes de marcar cualquier dato como faltante, léelo de
`data/surface/catalogo_fuentes.csv` y de `src/config.py`, donde están registradas las
seis fuentes del proyecto con entidad, nombre, dirección, formato, cobertura y licencia.
Ese catálogo es evidencia del proyecto: no es invención usarlo. Solo marca
`[VERIFICAR ANTES DE ENTREGA]` un dato que no esté ni en el documento ni en el catálogo.

Añade las referencias en orden alfabético, con el mismo formato de las existentes, y
agrega las filas correspondientes a la tabla de verificación de fuentes en línea. En la
columna de fecha de actualización escribe «por verificar» para las direcciones que no
hayas podido abrir, en lugar de inventar una fecha.

Deja claro en el texto que DIMAR fue consultada para evaluar la viabilidad del dominio
marítimo y que sus boletines no proporcionan la serie tabular histórica requerida.

**6. Consistencia sobre las 52 preguntas.** Busca en todo el documento frases que puedan
leerse como que las 52 fueron ejecutadas. Sustitúyelas por formulaciones del tipo «las
52 preguntas fueron respondidas o cerradas con evidencia» o el desglose 38 / 4 / 10. No
toques la matriz del anexo A.

**7. Consistencia de cifras contra el catálogo.** No compares el documento contra una
lista escrita a mano. Compáralo contra `data/surface/lista_cifras.csv`, que es el
catálogo verificado del proyecto, y contra `cifras_usadas_documento.csv`. Reporta
cualquier valor del documento que no aparezca en el catálogo, y cualquier cifra del
catálogo que el documento cite con otro valor. No corrijas ninguna automáticamente:
repórtalas.

**8. Consistencia de formato numérico.** Comprueba si el documento mezcla convenciones,
por ejemplo índices con separador de miles y otros sin él. Unifícalo sin alterar ningún
valor y enumera en el reporte cada cadena que cambiaste.

**9. Hallazgos que no se pueden suavizar.** Verifica que siguen en el texto, y déjalos
intactos: la integración es agregada por mes calendario; no existe llave pública
declaración-buque; el dominio portuario no mejora el pronóstico del valor CIF y su
aporte es descriptivo y explicativo; la carga contenerizada no debe modelarse porque la
referencia simple funciona mejor; el dominio marítimo y el operativo no son viables con
las fuentes públicas encontradas; las sociedades ausentes en 2026 solo pueden
describirse como sin reporte; el índice de concentración mide toneladas reportadas y no
capacidad instalada; el valor CIF por kilogramo es un valor unitario implícito.

Busca además estas expresiones prohibidas y reporta si aparecen: «dejaron de operar»,
«precio por kilogramo», «el puerto influye», «terminal» usado como sinónimo de sociedad
portuaria.

**10. Coherencia con la presentación.** Compara la formulación del problema, el objetivo
general y los objetivos específicos del documento contra
`reports/Presentacion_Buenaventura_V5_INSTITUCIONAL.pptx`. El jurado tiene ambos
delante. Si difieren, la redacción que manda es la del documento: reporta la diferencia
para que se corrija la presentación, no el documento.

**11. Forma.** Revisa coherencia de títulos, numeración, nombres de tablas, fuente
debajo de cada tabla, consistencia de referencias, APA séptima edición y fechas de
recuperación solo donde correspondan. No rediseñes el documento.

## Entrega

Guarda una copia nueva llamada
`Documento_Academico_Buenaventura_V5_FINAL_JURADOS.docx` sin sobrescribir el original, y
entrega un reporte con cinco apartados:

A. Cambios realizados, cada uno con la evidencia que lo justificó.
B. Cambios que no se realizaron, con la comprobación que los descartó.
C. Referencias que requieren verificación manual.
D. Inconsistencias detectadas, sin corregir.
E. Confirmación explícita de que las cifras principales no fueron alteradas.
