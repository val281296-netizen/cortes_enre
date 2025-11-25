import csv
import re
from datetime import datetime
import requests

content = requests.get(
    "https://www.enre.gov.ar/mapaCortes/datos/Datos_PaginaWeb.js"
).content.decode("utf8")

# Timestamp actual
fecha_actual = datetime.now().strftime("%Y-%m-%d")
hora_actual = datetime.now().strftime("%H:%M:%S")

def parse_tipo(s):
    if "media" in s.lower():
        return "media"
    elif "baja" in s.lower():
        return "baja"
    return "alta"


def parse_empresa(s):
    return "Edesur" if "EDESUR" in s else "Edenor"


def _(s):
    return s


def dospuntos(s):
    return s.partition(": ")[-1].title().rstrip('"')


def number(s):
    return "".join(_ for _ in s if _.isdigit())


nuevos = []

for incidente in re.findall("\[(\-.*?)\]", content):
    incidente = incidente.split(",")
    if len(incidente) == 11:
        # corte alta/media
        headers = {
            "latitud": _,
            "longitud": _,
            "nn": _,
            "tipo": parse_tipo,
            "empresa": parse_empresa,
            "partido": dospuntos,
            "localidad": dospuntos,
            "subestacion": dospuntos,
            "alimentador": dospuntos,
            "afectados": number,
            "normalizacion estimada": dospuntos,
        }
    else:
        headers = {
            "latitud": _,
            "longitud": _,
            "nn": _,
            "tipo": parse_tipo,
            "empresa": parse_empresa,
            "partido": dospuntos,
            "localidad": dospuntos,
            "afectados": number,
        }
    
 # Construir dict e incluir timestamp
    incidente_dict = {header: f(value.strip()) for (header, f), value in zip(headers.items(), incidente)}
    incidente_dict["fecha_descarga"] = fecha_actual
    incidente_dict["hora_descarga"] = hora_actual
    nuevos.append(incidente_dict)

# Guardar CSV
fieldnames = [
    "latitud",
    "longitud",
    "nn",
    "tipo",
    "empresa",
    "partido",
    "localidad",
    "subestacion",
    "alimentador",
    "afectados",
    "normalizacion estimada",
    "fecha_descarga",
    "hora_descarga",
]

with open("cortes_enre.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(nuevos)


