# Guía de defensa para la sustentación

Material de apoyo para Juan Manuel Tejada Fajardo y Jesús Alejandro Guerrero.
Todo lo que aparece aquí está en el documento académico o en un archivo del pipeline.

## 1. Las tres frases que tienes que poder decir de memoria

Si te bloqueas, vuelve a estas tres. Sostienen toda la defensa.

**El problema.** Los datos aduaneros y portuarios de Buenaventura son públicos, pero están separados, cambian de formato y miden cosas distintas. Sin integrarlos no se puede distinguir si el comercio creció porque entró más mercancía o porque la mercancía se encareció.

**Lo que se hizo.** Se construyó un producto reproducible que integra 173 meses de aduana y 102 de puerto sobre 101 meses comunes, ejecuta 52 preguntas con evidencia archivada, pronostica solo lo que las fuentes sostienen y declara con nombre propio lo que no puede afirmar.

**El resultado que define el trabajo.** La hipótesis de partida era que integrar mejoraría el pronóstico. Se midió con ablación y resultó falsa: añadir el dominio portuario empeora el error del CIF de 6,082 % a 6,575 %. El aporte de la integración es explicativo, no predictivo, y así se reporta.

## 2. Tus cartas fuertes

Estas son las cosas que la mayoría de proyectos de este nivel no tiene. Sácalas tú, sin esperar a que las pregunten.

**Reportaste tres líneas base, no una.** Contra la referencia estacional el modelo parece mejorar 64,4 %. Contra repetir el último valor, que es la referencia exigente en esta serie, la mejora real es 15,5 %. Podías haber contado solo la primera cifra y nadie lo habría notado. Contaste las dos. Ese es el argumento de honestidad más fuerte que tienes.

**Retiraste un modelo que no funcionaba.** En carga contenerizada el modelo da 9,450 % y repetir el último valor da 8,553 %. La recomendación del trabajo es no usar modelo ahí. Un proyecto que retira su propio modelo cuando no gana es más creíble que uno donde todo funciona.

**Ninguna cifra está escrita a mano.** Hay una lista de cifras que asocia cada valor con su archivo de origen y su pregunta. La construcción del documento falla si alguien pide una cifra que no esté en esa lista. Esto lo puedes demostrar en vivo.

**Las 52 preguntas están cerradas.** 38 ejecutadas, 4 parciales, 10 no viables con la búsqueda documentada. Cero sin respuesta.

**80 pruebas automatizadas** que verifican reglas del propio producto, no solo que el código corra: que las variables no miren al futuro, que los intervalos no se deriven de una métrica puntual, que una pregunta sin salida no se marque como ejecutada.

**Corregiste tu propio diagnóstico.** El proyecto arrancó suponiendo que los datos portuarios solo existían en boletines trimestrales en PDF. Verificaste y era falso: el conjunto es mensual y descargable por interfaz de programación. Eso convirtió un dominio inviable en uno con 102 observaciones.

## 3. Las diez preguntas que te van a hacer, con la respuesta

### «Entonces la integración no sirvió. ¿Su proyecto falló?»

No. La pregunta de investigación era si integrar aporta y hasta dónde. La respuesta medida es que aporta de forma explicativa y no predictiva, y eso es un resultado, no un fracaso. Sin la integración no se puede separar volumen de valor unitario, ni mostrar que la caída del total portuario venía del transbordo. Un proyecto que solo puede terminar bien si confirma su hipótesis no está midiendo nada.

### «Una mejora del 15,5 % es poca cosa»

Es poca y está medida. La alternativa era reportar el 64,4 % contra la referencia estacional, que en esta serie es una referencia débil porque la autocorrelación en el rezago 1 es 0,917 y en el rezago 12 apenas 0,590. Reportar solo esa cifra habría descrito la debilidad de la referencia, no la calidad del modelo.

### «¿Por qué no usaron redes neuronales o modelos más potentes?»

Se probó gradient boosting y quedó por debajo. En carga contenerizada dio 10,817 % frente a 9,450 % de la regresión regularizada y 8,553 % de repetir el último valor. Con 101 meses comunes y 173 aduaneros, un modelo con más capacidad aprende ruido. La restricción no es de ambición sino de tamaño de muestra, y a eso se suma la exigencia de interpretabilidad que está declarada en la delimitación metodológica.

### «Diez preguntas no viables es casi el 20 % sin responder»

No quedaron sin responder: su respuesta es que la fuente no existe en el ámbito público. Se consultaron cuatro vías de acceso y está documentado en el anexo B. DIMAR publica solo boletines trimestrales en PDF sin desagregación por evento, y los datos de ETA, ATA y permanencias vienen de sistemas de terminal o de AIS comercial, sin acceso ni presupuesto. Inventar esas variables habría sido el error grave.

### «El índice de concentración de 3.514 indica un riesgo para el puerto»

El índice mide reparto de toneladas reportadas. No mide capacidad instalada, utilización ni posibilidad real de sustitución entre sociedades. De hecho el cruce por tipo de carga muestra que no son intercambiables: una no registró granel en todo el periodo y otra no registró contenedores. Con esta fuente no se puede concluir riesgo operativo.

### «En 2026 el índice sube a 4.217, hay más concentración»

Ese valor no es comparable. Cubre seis meses y solo tres sociedades reportan. Recalculando 2025 con esas mismas tres sociedades el índice sería 4.096, de modo que la mayor parte del salto se explica por el cambio de cobertura del reporte y no por una redistribución entre las que continúan.

### «¿Esas dos sociedades quebraron?»

No lo sabemos y el trabajo no lo afirma. La fuente registra reporte, no operación. Lo único que puede sostenerse es que no aparecen en los reportes de los seis meses observados de 2026, y se verificó mes a mes para descartar rezago de publicación. La causa institucional requeriría fuentes de la ANI que no se integraron.

### «¿Cómo sé que no hay fuga de información en el modelo?»

Tres mecanismos. Todas las variables predictoras se construyen con datos anteriores al mes que se predice y las medias móviles se calculan sobre la serie ya desplazada. Los escaladores se ajustan dentro del conjunto de entrenamiento de cada corte, no sobre la serie completa. Y existe una prueba automatizada que detiene el proceso si alguna variable presenta correlación casi perfecta con el objetivo del mismo mes.

### «El valor por kilogramo subió, ¿es inflación?»

No se puede afirmar. El CIF está en dólares corrientes y el cociente entre valor y kilogramo es un valor unitario implícito, afectado por la mezcla de mercancías, el seguro y el flete. No es un precio de mercado. Lo que sí puede afirmarse es la descomposición: del 80,4 % de crecimiento, el volumen aporta 52,2 % y el valor unitario 47,0 %, con un residuo declarado de menos de un punto.

### «Su modelo de negocio no está validado»

Correcto, y así se declara en el capítulo 13 antes de presentarlo. No hay entrevistas ni pilotos. Por eso la primera recomendación del trabajo es validar las reglas de alerta con al menos un usuario real antes de considerarlas operativas.

## 4. Palabras que no debes decir

El jurado no va a atacar tus números, va a atacar tus verbos. Estas seis sustituciones te protegen.

| No digas | Di |
|---|---|
| «terminal» | «sociedad portuaria», que es lo que la fuente identifica |
| «dejaron de operar» | «no aparecen reportando en los seis meses observados de 2026» |
| «precio por kilogramo» | «valor unitario implícito» |
| «el puerto influye en el CIF» | «las series se asocian», y solo si hablas de correlación |
| «el modelo predice» a secas | «el modelo pronostica con un error medido de X %» |
| «la alerta indica que hay que actuar» | «la alerta es una señal de revisión analítica» |

## 5. Cifras de bolsillo

Llévalas anotadas. Si te preguntan un número y dudas, di la cifra y de dónde sale.

| Concepto | Valor |
|---|---|
| Registros aduaneros procesados | 6.703.351 |
| Meses de aduana / puerto / integrados | 173 / 102 / 101 |
| Periodo integrado | 2018-01 a 2026-05 |
| WAPE del mejor modelo de CIF | 5,875 % |
| Repetir el último valor (CIF) | 6,956 % |
| Mejora real / contra la estacional | 15,5 % / 64,4 % |
| Ablación: solo historia vs. historia + puerto | 6,082 % vs. 6,575 % |
| Toneladas totales: modelo vs. referencia | 6,613 % vs. 9,174 %, mejora 27,9 % |
| Carga contenerizada: modelo vs. referencia | 9,450 % vs. 8,553 %, el modelo pierde |
| Cobertura nominal / empírica | 80 % / entre 75,0 % y 91,7 % |
| Crecimiento del CIF y su descomposición | 80,4 % = 52,2 % volumen + 47,0 % valor unitario |
| Tráfico portuario por flujo | importación +19,6 %, exportación +1,3 %, transbordo −85,2 %, total −13,3 % |
| HHI capítulo / país / sociedad portuaria | 433,74 / 1.351,38 / 3.514,24 |
| Mayor sociedad portuaria | 51,36 % |
| Preguntas ejecutadas / parciales / no viables | 38 / 4 / 10 |
| Pruebas automatizadas | 80 |
| Autocorrelación del CIF, rezago 1 y 12 | 0,917 y 0,590 |

## 6. Herramientas para la exposición

**El tablero en ejecución.** `streamlit run dashboard/app.py`. Es tu mejor momento: nada convence más que filtrar en vivo. Ábrelo antes de empezar, no durante.

**Las pruebas, si te retan.** `python -m pytest tests -q` en la terminal. Ochenta en verde en unos segundos. Ten la terminal abierta en otra ventana por si alguien pone en duda la calidad del código.

**La lista de cifras.** `data/surface/lista_cifras.csv`. Si alguien pregunta de dónde sale un número, lo abres y le muestras el archivo y la pregunta que lo originó. Es el argumento que cierra cualquier discusión sobre trazabilidad.

**La matriz de trazabilidad.** `data/surface/matriz_trazabilidad_eda.csv` para el estado de las 52 preguntas, y `reporte_no_viabilidad.csv` para las diez cerradas.

**Respaldos.** Ten abiertos el PDF de la presentación y el cuaderno ya ejecutado con sus 55 figuras. Si el tablero no arranca, sigues teniendo la demostración.

**Antes de salir de casa:** corre el pipeline y las pruebas una vez, abre el tablero, comprueba que la fuente Montserrat esté instalada en el equipo donde vas a exponer y compara una diapositiva contra el PDF.

## 7. El reparto de los quince minutos

| Bloque | Tiempo | Diapositivas | Qué tiene que quedar |
|---|---|---|---|
| Contexto | 3 min | 1 a 16 | El problema, la pregunta y hasta dónde llega el alcance |
| Producto de datos | 10 min | 17 a 27 | Metodología, los cuatro hallazgos y la demostración en vivo |
| Cierre | 2 min | 28 a 33 | Conclusiones, recomendaciones y fuentes |

Tres minutos para dieciséis diapositivas significa unos once segundos por lámina. No las leas: cada una tiene un gráfico que dice lo que tú vas a resumir en una frase. La lámina de formulación y la de objetivo general son las dos únicas del bloque de contexto donde conviene detenerse.

Los diez minutos del producto son donde se decide la nota. Dedica dos a la metodología, cuatro a los hallazgos, dos a la demostración y dos al despliegue y la trazabilidad.

## 8. Reparto entre los dos

Conviene que se note que ambos conocen todo el trabajo, no que cada uno memorizó su parte. Una división que funciona bien: uno abre con el contexto y cierra con las conclusiones, el otro lleva la metodología y la demostración en vivo. En las preguntas, el que no está respondiendo mira a quien pregunta y toma nota, no al computador.

## 9. Lo que no debes hacer

No pidas disculpas por los resultados negativos. Ese es tu mejor material: preséntalo como decisión metodológica, no como limitación lamentable.

No prometas nada que el producto no haga. Si preguntan por congestión, tiempos de atención o buques, la respuesta es que no hay fuente pública y está documentado.

No leas las diapositivas. Están construidas para que tú hables encima de un gráfico.

No improvises cifras. Si no la recuerdas, di que está en la lista de cifras y que puedes abrirla.

No discutas con el jurado. Si señalan algo que no habías considerado, reconócelo y di cómo lo mediría una segunda fase. El trabajo ya tiene ocho recomendaciones escritas justamente para eso.
