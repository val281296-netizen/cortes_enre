import csv
import re
import requests
import os

# URL del ENRE
URL = "https://www.enre.gov.ar/mapaCortes/datos/Datos_PaginaWeb.js"

# Descargar el contenido (ignorar SSL)
try:
    content = requests.get(URL, verify=False, timeout=20).text
except Exception as e:
    print("Error al descargar los datos:", e)
    exit(1)


# Funciones de parsing
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

for incidente in re.findall(r"\[(\-.*?)\]", content):
    incidente = incidente.split(",")
    if len(incidente) == 11:
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
    # Build dict seguro
    incidente_dict = {
        header: f(value.strip())
        for (header, f), value in zip(headers.items(), incidente)
    }
    nuevos.append(incidente_dict)

# Guardar CSV
csv_file = "cortes_enre.csv"
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
]

with open(csv_file, "w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(nuevos)

print(f"{csv_file} generado correctamente con {len(nuevos)} incidentes.")
