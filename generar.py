
import json
from pathlib import Path
from datetime import datetime
from html import escape

# 1. Ubicacion de las carpetas
BASE = Path(__file__).parent

ARCHIVO_DATOS = BASE / "datos" / "noticias.json"
ARCHIVO_PLANTILLA = BASE / "plantillas" / "noticias.html"
ARCHIVO_HTML = BASE / "html" / "index.html"


# 2. Leer los datos de las noticias
with open(ARCHIVO_DATOS, "r", encoding="utf-8") as archivo:
    noticias = json.load(archivo)


# 3. Ordenar de la mas reciente a la mas antigua
noticias.sort(
    key=lambda noticia: datetime.strptime(
        noticia["fecha"], "%Y-%m-%d"
    ),
    reverse=True
)


# 4. Leer la plantilla de las tarjetas
with open(ARCHIVO_PLANTILLA, "r", encoding="utf-8") as archivo:
    plantilla = archivo.read()


# 5. Generar las tarjetas automaticamente
tarjetas = ""

for noticia in noticias:

    fecha = datetime.strptime(
        noticia["fecha"], "%Y-%m-%d"
    ).strftime("%d/%m/%Y")

    if noticia.get("imagen"):
        imagen = f'''
        <img src="{escape(noticia["imagen"], quote=True)}"
             alt="{escape(noticia["titulo"], quote=True)}">
        '''
    else:
        imagen = ""

    tarjeta = plantilla.replace(
        "{{titulo}}", escape(noticia["titulo"])
    )

    tarjeta = tarjeta.replace(
        "{{fecha}}", fecha
    )

    tarjeta = tarjeta.replace(
        "{{texto}}", escape(noticia["texto"])
    )

    tarjeta = tarjeta.replace(
        "{{imagen}}", imagen
    )

    tarjetas += tarjeta + "\n"

    
# 6. Insertar las tarjetas en el HTML
with open(ARCHIVO_HTML, "r", encoding="utf-8") as archivo:
    contenido = archivo.read()

inicio = "<!-- INICIO_NOTICIAS_AUTOMATICAS -->"
fin = "<!-- FIN_NOTICIAS_AUTOMATICAS -->"

if inicio not in contenido or fin not in contenido:
    raise ValueError("No se encontraron los marcadores de noticias.")

antes, resto = contenido.split(inicio, 1)
_, despues = resto.split(fin, 1)

contenido_final = (
    antes + inicio + "\n" +
    tarjetas +
    fin + despues
)


# 7. Guardar el HTML actualizado
with open(ARCHIVO_HTML, "w", encoding="utf-8") as archivo:
    archivo.write(contenido_final)

print("¡Noticias generadas correctamente!")
print(f"Cantidad de noticias: {len(noticias)}")
