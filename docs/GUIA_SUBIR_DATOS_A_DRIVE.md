# Subir los datos a Drive y llamarlos desde Colab

Tu carpeta ya existe: **Mi unidad › v2_buenaventura_datos**. Falta llenarla y decirle al
cuaderno que la use.

---

## Lo primero: qué NO vas a subir

Los 18 paquetes ZIP del DANE pesan 8,1 GB. **No los subas.** Tres razones.

Tu Drive gratuito tiene 15 GB, y esos paquetes se comerían más de la mitad. El pipeline
no los necesita: lee `serie_mensual_aduanera_v4.parquet`, que son 15 KB con los 173 meses
ya reconciliados a partir de los 6.703.351 registros. Y subir 8 GB por navegador es una
operación de horas que se corta sola con cualquier microcorte de conexión.

Esos ZIP solo harían falta si quisieras rehacer la extracción desde cero, y eso ya está
hecho y verificado. Déjalos donde están, en tu disco, respaldados.

## Lo que sí vas a subir

La carpeta `data` completa del proyecto. Son **240 KB en 52 archivos**, repartidos así:

| Capa | Archivos | Qué contiene |
|---|---|---|
| `raw` | 6 | fuentes originales agregadas: puerto, aduana reconciliada, contexto |
| `trusted` | 4 | series mensuales validadas de ambos dominios |
| `surface` | 42 | toda la evidencia de las 52 preguntas que consume el tablero |
| `landing` | vacía | se llena sola al ejecutar el pipeline |

Se sube en menos de un minuto.

---

## Paso 1. Subir la carpeta

1. Abre <https://drive.google.com> y entra a **Mi unidad › v2_buenaventura_datos**.
2. En otra ventana abre el Explorador de archivos en
   `C:\Users\juanc\Desktop\v2_buenaventura_diplo\proyecto_integrado_buenaventura`
3. **Arrastra la carpeta `data` completa** desde el Explorador hasta la ventana de Drive.
   Arrastra la carpeta, no los archivos sueltos: la estructura de subcarpetas es la que
   el proyecto espera y si la aplanas no funciona.
4. Espera a que el contador de subida llegue a 52 de 52.

Si arrastrar no te funciona, dentro de la carpeta en Drive usa el botón **+ Nuevo** y
luego **Subir carpeta**, y selecciona `data`.

Al terminar, dentro de `v2_buenaventura_datos` debes ver **una sola carpeta llamada
`data`**, y dentro de ella `raw`, `landing`, `trusted` y `surface`. Así de exacto:

```
Mi unidad
└── v2_buenaventura_datos
    └── data
        ├── raw
        │   ├── aduanas
        │   ├── contexto
        │   ├── maritimo
        │   └── puertos
        ├── landing
        ├── trusted
        └── surface
```

Si `raw`, `trusted` y `surface` te quedaron sueltas dentro de `v2_buenaventura_datos`,
sin la carpeta `data` envolviéndolas, el cuaderno no las va a encontrar. Créala en Drive
y mete las tres adentro.

---

## Paso 2. Activarlo en el cuaderno

Ya dejé `00_entorno.ipynb` apuntando a tu carpeta. Ábrelo en Colab y busca la celda de la
sección 3. Verás esto:

```python
USAR_DRIVE = False                        # ← poner en True para persistir en Drive
CARPETA_DRIVE = "v2_buenaventura_datos"   # ← carpeta dentro de «Mi unidad»
```

Cambia la primera línea a `True`. Nada más:

```python
USAR_DRIVE = True
CARPETA_DRIVE = "v2_buenaventura_datos"
```

Ejecuta la celda. Colab te va a pedir permiso para acceder a Drive: aparece una ventana,
eliges tu cuenta de Google y aceptas. Es la cuenta con la que abriste el Drive donde está
la carpeta.

La celda debe imprimir:

```
Datos persistentes en: /content/drive/MyDrive/v2_buenaventura_datos/data
raíz de datos : /content/drive/MyDrive/v2_buenaventura_datos/data
capa raw      : /content/drive/MyDrive/v2_buenaventura_datos/data/raw
capa surface  : /content/drive/MyDrive/v2_buenaventura_datos/data/surface
```

Fíjate en `MyDrive` sin espacio y sin acento. Drive te lo muestra como «Mi unidad» en
español, pero por dentro siempre se llama `MyDrive`. No lo cambies.

---

## Paso 3. Comprobar que quedó bien

Ejecuta la celda de la sección 4, la prueba mínima. Si imprime la serie portuaria con sus
102 meses, continuidad `True` y el catálogo con 52 preguntas, está leyendo desde tu Drive
y funciona.

Si quieres una comprobación más directa, pega esto en una celda nueva:

```python
from src import config
print("leyendo de:", config.DATA)
print("archivos en surface:", len(list(config.SURFACE.glob("*"))))
print("existe la serie portuaria:",
      (config.TRUSTED / "serie_portuaria_mensual.parquet").exists())
```

Debe decir 42 archivos en surface y `True` en la última línea.

---

## Para qué sirve realmente esto

Colab borra su disco cada vez que cierras la sesión. Sin Drive, ejecutas el pipeline,
generas las 42 salidas y las 55 figuras, cierras el navegador y al día siguiente no queda
nada: toca ejecutar todo otra vez.

Con Drive montado, lo que el pipeline escribe cae directamente en tu carpeta y sobrevive.
Puedes cerrar Colab, volver mañana, montar de nuevo y los resultados siguen ahí.

Hay un efecto secundario que conviene que sepas: **si ejecutas el pipeline con Drive
montado, va a sobrescribir los archivos de tu carpeta de Drive con las salidas nuevas.**
Es el comportamiento deseado, pero si por algo quieres conservar la versión con la que
sustentas, haz antes una copia de la carpeta `data` en Drive con el botón derecho y
**Hacer una copia**, o simplemente duplícala como `data_respaldo_sustentacion`.

---

## Errores frecuentes

**`FileNotFoundError` apuntando a una ruta de `MyDrive`** — la estructura de carpetas no
coincide. Vuelve al final del paso 1 y compara con el árbol. Casi siempre es que falta la
carpeta `data` envolviendo a las cuatro capas.

**«No se está ejecutando en Colab; las rutas de datos no se modifican»** — abriste el
cuaderno en tu computador, no en Colab. El montaje de Drive solo existe dentro de Colab;
en local el proyecto ya usa la carpeta `data` del disco y no necesita nada de esto.

**Colab no te pide permiso y falla el montaje** — cierra la sesión desde *Entorno de
ejecución › Desconectar y eliminar el entorno*, vuelve a abrir y ejecuta desde la primera
celda.

**Cambiaste el nombre de la carpeta en Drive** — actualiza `CARPETA_DRIVE` en la celda
para que diga exactamente el nombre nuevo, respetando mayúsculas y guiones bajos.

---

## Si de todas formas quieres los ZIP del DANE en la nube

No los pongas dentro de `v2_buenaventura_datos`: el proyecto no los busca ahí y solo
ensuciarían la carpeta. Crea una carpeta aparte, por ejemplo `v2_buenaventura_fuentes`,
y súbelos de a dos o tres por vez. Ten presente que 8,1 GB sobre 15 GB gratuitos te deja
sin espacio para casi nada más, y que ninguna parte del proyecto los va a leer desde ahí
sin que reescribas el código de extracción.
