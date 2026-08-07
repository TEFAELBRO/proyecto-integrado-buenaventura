# Subir el proyecto a GitHub, paso a paso

Repositorio público, desde la terminal de Windows. Antes de los comandos va una
revisión de qué se sube y qué no, porque al ser público eso importa.

---

## Parte 0. Qué se va a subir (ya revisado)

Revisé el proyecto entero antes de escribir esta guía. Esto es lo que encontré.

**No hay nada peligroso.** Cero claves, cero tokens, cero contraseñas, cero correos
personales y cero rutas absolutas de tu computador dentro del código. Ese último punto
importa: si hubiera un `C:\Users\juanc\...` escrito en un módulo, cualquiera vería el
nombre de usuario de tu equipo y además el proyecto no correría en otra máquina.

**No se suben los microdatos del DANE.** El `.gitignore` excluye los paquetes ZIP, que
pesan 8,7 GB y viven fuera del repositorio. Lo que sí sube `data/raw/` son 49 KB de
series ya agregadas por mes. Esto es exactamente lo que la licencia del DANE permite:
prohíbe reproducir los microdatos originales, no los agregados. Tu propio documento lo
declara en el apartado 17.1.

**El peso total es de unos 20 MB en 271 archivos.** GitHub acepta sin problema hasta
100 MB por archivo. Los cuatro más pesados son el cuaderno ejecutado (3,6 MB), la
presentación (3,2 MB), el fondo de portada institucional (2,4 MB) y el PDF de la
presentación (1,9 MB).

### La única decisión que tienes que tomar

La carpeta `reports/plantilla_institucional/` contiene los fondos y los logos que extraje
del PDF de la plantilla de la universidad. Son marcas institucionales de Universidad
Libre. Publicarlas en un repositorio público de un trabajo de grado sobre esa misma
universidad es habitual y difícilmente objetable, pero es material de la institución y no
tuyo.

Si prefieres ser conservador, ejecuta esto antes de empezar y esos archivos no se suben:

```powershell
cd C:\Users\juanc\Desktop\v2_buenaventura_diplo\proyecto_integrado_buenaventura
Add-Content .gitignore "`n# Material institucional: no se redistribuye`nreports/plantilla_institucional/"
```

Ten en cuenta que si los excluyes, quien clone el repositorio no podrá reconstruir la
presentación con `docs/_construir_presentacion_institucional.py`, porque el script busca
esas imágenes. El archivo `.pptx` ya construido sí seguiría en el repositorio.

Mi recomendación: déjalos. Es un trabajo académico de esa universidad y el uso es
evidente.

---

## Parte 1. Comprobar que tienes git

Abre PowerShell. Tecla Windows, escribe `powershell`, Enter.

```powershell
git --version
```

Si responde algo como `git version 2.4x.x`, sigue a la parte 2.

Si responde que no reconoce el comando, descárgalo de <https://git-scm.com/download/win>,
instálalo dejando todas las opciones por defecto, **cierra PowerShell, ábrelo otra vez** y
repite el comando. El cierre y reapertura es necesario: si no, Windows no ve el programa
recién instalado.

### Decirle a git quién eres

Solo se hace una vez en la vida por computador. Usa el mismo correo con el que abriste
tu cuenta de GitHub.

```powershell
git config --global user.name "Juan Manuel Tejada Fajardo"
git config --global user.email "juanmanueltefa@gmail.com"
git config --global init.defaultBranch main
```

---

## Parte 2. Crear el repositorio vacío en GitHub

Esta parte sí es de clics.

1. Entra a <https://github.com> e inicia sesión.
2. Arriba a la derecha, el botón **+** y luego **New repository**.
3. En **Repository name** escribe `proyecto-integrado-buenaventura`.
4. En **Description**, algo como: `Producto de datos que integra el registro aduanero de importación y el tráfico portuario de Buenaventura. Trabajo de grado, Ciencia de Datos, Universidad Libre Cali.`
5. Marca **Public**.
6. **Muy importante: no marques nada más.** Deja sin marcar *Add a README file*, *Add .gitignore* y *Choose a license*. Tu proyecto ya trae README y .gitignore propios; si GitHub crea los suyos, el primer envío chocará y tendrás que resolver un conflicto sin necesidad.
7. Botón verde **Create repository**.

Te queda una página con instrucciones. No la cierres: ahí está la dirección que vas a
necesitar, del tipo `https://github.com/TU-USUARIO/proyecto-integrado-buenaventura.git`.

---

## Parte 3. Preparar el proyecto en tu computador

En PowerShell:

```powershell
cd C:\Users\juanc\Desktop\v2_buenaventura_diplo\proyecto_integrado_buenaventura
git init
git add .
```

Ahora **revisa qué quedó preparado antes de confirmarlo**. Este paso es el que te
protege en un repositorio público:

```powershell
git status --short
```

Verás una lista larga de líneas que empiezan por `A`. Recórrela buscando cualquier cosa
que no debería estar ahí. Si ves algún `.zip`, algún `.env` o algo con datos personales,
párate y sácalo antes de continuar.

Para comprobar de un vistazo que los pesados no entraron:

```powershell
git status --short | Select-String "\.zip|\.7z|\.env"
```

Si no imprime nada, está limpio.

Ahora confirma el conjunto:

```powershell
git commit -m "Producto de datos integrado de Buenaventura, version 5"
git branch -M main
```

---

## Parte 4. Conectar y enviar

Reemplaza `TU-USUARIO` por tu nombre de usuario real de GitHub.

```powershell
git remote add origin https://github.com/TU-USUARIO/proyecto-integrado-buenaventura.git
git push -u origin main
```

### La autenticación

Al ejecutar `git push` se abrirá una ventana de GitHub pidiéndote iniciar sesión. Acepta,
autoriza y listo: Windows guarda la credencial y no te la volverá a pedir.

Si en lugar de la ventana te pide usuario y contraseña en la terminal, ten en cuenta que
**GitHub ya no acepta tu contraseña normal**. Necesitas un token:

1. En GitHub, tu foto arriba a la derecha, **Settings**.
2. Abajo del todo en el menú izquierdo, **Developer settings**.
3. **Personal access tokens** y luego **Tokens (classic)**.
4. **Generate new token (classic)**.
5. En *Note* escribe `proyecto buenaventura`. En *Expiration* elige 90 días.
6. Marca la casilla **repo**, la primera de la lista.
7. Abajo, **Generate token**.
8. Copia el texto que aparece. **Solo se muestra una vez.** Si cierras la página lo pierdes y tendrás que generar otro.

Vuelve a la terminal: en `Username` escribe tu usuario de GitHub, y en `Password` pega el
token. No verás nada mientras pegas, es normal, la terminal no muestra las contraseñas.
Pega y da Enter.

---

## Parte 5. Comprobar que quedó bien

Recarga la página de tu repositorio en GitHub. Deberías ver las carpetas `src`,
`notebooks`, `dashboard`, `data`, `docs`, `reports` y `tests`, y el README renderizado
más abajo.

Tres comprobaciones concretas:

Abre `notebooks/EDA_52_Preguntas_Buenaventura_V5_EJECUTADO.ipynb`. GitHub renderiza los
cuadernos, así que el jurado debería ver tus 55 figuras directamente en el navegador, sin
descargar nada. Es la mejor forma de que revisen el análisis.

Entra a `data/raw/` y confirma que solo hay archivos pequeños, ningún ZIP.

Busca la pestaña de tamaño del repositorio: en **Settings**, al principio, debe rondar
los 20 MB.

---

## Parte 6. Cerrar el círculo con Colab

Tu cuaderno `notebooks/00_entorno.ipynb` está preparado para clonar el repositorio en
Google Colab, pero necesita saber la dirección. Créala así:

```powershell
cd C:\Users\juanc\Desktop\v2_buenaventura_diplo\proyecto_integrado_buenaventura\notebooks
"https://github.com/TU-USUARIO/proyecto-integrado-buenaventura.git" | Out-File -Encoding utf8 repo_url.txt
cd ..
git add notebooks/repo_url.txt
git commit -m "Registrar la direccion del repositorio para el arranque en Colab"
git push
```

Con eso, abrir `00_entorno.ipynb` en Colab clona el proyecto, instala dependencias y
corre la prueba mínima sin que nadie tenga que editar nada.

---

## Parte 7. Subir cambios de aquí en adelante

Cada vez que modifiques algo, son tres líneas:

```powershell
cd C:\Users\juanc\Desktop\v2_buenaventura_diplo\proyecto_integrado_buenaventura
git add .
git commit -m "describe aqui el cambio"
git push
```

El mensaje del commit debe decir qué cambió, no «cambios» ni «update». Un evaluador
técnico mira el historial.

---

## Si algo sale mal

**`fatal: not a git repository`** — no estás dentro de la carpeta del proyecto. Repite
el `cd` de la parte 3.

**`remote origin already exists`** — ya habías conectado un remoto. Bórralo y vuelve a
crearlo: `git remote remove origin` y luego el `git remote add` de nuevo.

**`Updates were rejected because the remote contains work that you do not have`** —
marcaste alguna casilla en el paso 6 de la parte 2 y GitHub creó archivos propios. La
salida más limpia: borra el repositorio en GitHub desde **Settings**, abajo del todo en
**Delete this repository**, y créalo otra vez sin marcar nada.

**`Authentication failed`** — el token está mal pegado o expiró. Genera uno nuevo. Si
Windows guardó una credencial vieja, límpiala: tecla Windows, escribe `Administrador de
credenciales`, entra a **Credenciales de Windows**, busca la entrada `git:https://github.com`
y quítala. El siguiente `push` te pedirá la nueva.

**El envío se queda colgado o tarda muchísimo** — son 20 MB, es normal que tome un
minuto largo con conexión lenta. Si pasa de cinco minutos, corta con Ctrl+C y reintenta.

---

## Antes de dar el enlace al jurado

Comprueba que un desconocido puede usar el repositorio. La prueba real es clonarlo en
otra carpeta y ver si corre:

```powershell
cd $env:TEMP
git clone https://github.com/TU-USUARIO/proyecto-integrado-buenaventura.git prueba-clon
cd prueba-clon
pip install -r requirements.txt
python -m pytest tests -q
python -m src.correr_integrado
```

Si las 80 pruebas pasan y el pipeline reproduce las mismas salidas, el repositorio está
completo. Si algo falla, es que el `.gitignore` está excluyendo un archivo necesario, y
eso es mejor descubrirlo tú ahora que el jurado el día de la sustentación.

Cuando termines, borra la carpeta de prueba con `cd ..` y `Remove-Item -Recurse -Force prueba-clon`.
