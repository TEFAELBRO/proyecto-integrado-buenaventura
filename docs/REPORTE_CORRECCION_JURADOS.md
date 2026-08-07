# Reporte de corrección para la entrega ante jurados

Documento de entrada: `Documento_Academico_Buenaventura_V5_FINAL_CORREGIDO.docx`
Documento de salida: `Documento_Academico_Buenaventura_V5_FINAL_JURADOS.docx`
El original no se sobrescribió.

## A. Cambios realizados

1. Tabla 2: el objetivo pasa de «Ejecutar las 52 preguntas y conservar la evidencia» a «Responder o cerrar con evidencia documentada las 52 preguntas del análisis exploratorio». La evidencia (matriz_trazabilidad_eda.csv) y el resultado (38 ejecutadas, 4 parciales, 10 no viables) no se tocaron.

2. Tabla 1, paso 7: se precisó la capa donde vive el archivo, que ahora dice «vista_integrada_mensual.parquet (capa trusted)». Es el cambio que evita la confusión que originó el hallazgo de la auditoría.

3. Se añadió la referencia del Banco de la República por la tasa representativa del mercado, usada como variable de contexto. Título, entidad y dirección provienen de catalogo_fuentes.csv; no se inventó ningún metadato.

4. Se añadió la referencia de la Dirección General Marítima, consultada para evaluar la viabilidad del dominio marítimo. La dirección fue verificada: la página publica boletines trimestrales en PDF y no ofrece serie tabular histórica por evento, que es exactamente lo que el documento afirma.

5. Se añadió la referencia de la NOAA por el índice oceánico de El Niño, usado como variable de contexto. Título, entidad y dirección provienen de catalogo_fuentes.csv.

6. Tabla 16: se añadieron las tres fuentes nuevas. La de DIMAR queda con fecha de actualización verificada; las de la TRM y el índice oceánico quedan marcadas como «por verificar», que es lo que la evidencia disponible permite afirmar.

7. Consistencia de las 52 preguntas: «Análisis exploratorio completo de 52 preguntas con evidenc…» pasa a «Análisis exploratorio de las 52 preguntas del catálogo, re…».

8. Consistencia de las 52 preguntas: «Ejecución de las 52 preguntas del análisis exploratorio…» pasa a «Respuesta o cierre documentado de las 52 preguntas…».

9. Formato numérico: el documento escribía unos índices de concentración con separador de miles (4.096, umbral 2.500) y otros sin él. Se unificaron sin alterar ningún valor: 3514,24 → 3.514,24; 1351,38 → 1.351,38; 4722 → 4.722; 2988 → 2.988; 3740 → 3.740; 4217 → 4.217.
## B. Cambios que no se realizaron y por qué

1. NO se reemplazó la salida del paso 7 por «salidas de integración en capa surface». El archivo vista_integrada_mensual.parquet sí existe: está en data/trusted/ (22,036 bytes), lo escribe src/correr_integrado.py y lista_cifras.csv lo cita como origen del periodo integrado, de la razón 1,16 y de la correlación 0,115. La auditoría lo dio por inexistente probablemente porque lo buscó en la capa surface. Aplicar esa corrección habría introducido un error en un documento correcto.
## C. Referencias que requieren verificación manual

1. Banco de la República: la dirección https://www.banrep.gov.co/es/estadisticas/trm no pudo reabrirse desde el entorno de trabajo. Ábrela y confirma que responde antes de imprimir.

2. NOAA Climate Prediction Center: la dirección del índice oceánico tampoco pudo reabrirse desde el entorno de trabajo. Confírmala antes de imprimir.

3. Fecha de consulta de la TRM y del índice oceánico: el manifiesto de fuentes solo registra la descarga del DANE y de la Superintendencia. Para las dos variables de contexto se usó la fecha de corte del proyecto, 6 de agosto de 2026. Si la descarga fue otro día, ajústala.
## D. Inconsistencias detectadas

Ninguna.
## E. Confirmación sobre las cifras

Las treinta cifras principales se verificaron una por una contra el texto del documento de salida y ninguna fue alterada. El único cambio numérico es de formato: se añadió el separador de miles a los índices de concentración que no lo llevaban, para que el documento no mezcle dos convenciones. El valor de cada índice es idéntico al de `comparacion_concentracion.csv` y `hhi_anual_sociedades.csv`.
