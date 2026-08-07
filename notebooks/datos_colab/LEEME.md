# Datos para el cuaderno

Esta carpeta contiene **solo lo que no existe en otro sitio del repositorio**:

| Archivo | Por qué está aquí |
|---|---|
| `serie_aduanera_mensual.csv` | Exportación en CSV de `data/trusted/serie_aduanera_mensual.parquet`, para que el cuaderno no dependa de pyarrow en Colab |

Todo lo demás (tráfico portuario, terminales, variables externas) lo lee el cuaderno
directamente de `data/raw/`, que es su ubicación canónica. **No se duplica.**

La función `ruta_dato()` del cuaderno busca en seis ubicaciones, de modo que funciona
igual si el repositorio se clona, si se ejecuta desde `notebooks/` o desde la raíz.
