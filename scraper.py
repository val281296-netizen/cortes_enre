import csv
import re

# Leer el archivo descargado previamente con curl
with open("Datos_PaginaWeb.js", "r", encoding="utf-8") as f:
    content = f.read()


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

# Buscar los incidentes entre corchetes
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

    incidente_dict = {
        header: f(value.strip())
        for (header, f), value in zip(headers.items(), incidente)
    }
    nuevos.append(incidente_dict)


# Guardar CSV
with open("cortes_enre.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(
        file,
        fieldnames=[
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
        ],
    )
    writer.writeheader()
    writer.writerows(nuevos)

print("CSV generado correctamente: cortes_enre.csv")
