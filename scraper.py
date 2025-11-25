import httpx
import csv
import re

URL = "https://www.enre.gov.ar/mapaCortes/datos/Datos_PaginaWeb.js"

# Cabeceras tipo navegador para evitar bloqueos
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/118.0.5993.90 Safari/537.36",
}

def parse_tipo(s):
    if "media" in s.lower():
        return "media"
    elif "baja" in s.lower():
        return "baja"
    return "alta"

def parse_empresa(s):
    return "Edesur" if "EDESUR" in s else "Edenor"

def dospuntos(s):
    return s.partition(": ")[-1].title().rstrip('"')

def number(s):
    return "".join(_ for _ in s if _.isdigit())

def parse_incidentes(content):
    nuevos = []
    for incidente in re.findall(r"\[(\-.*?)\]", content):
        incidente = incidente.split(",")
        if len(incidente) == 11:
            headers = {
                "latitud": str,
                "longitud": str,
                "nn": str,
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
                "latitud": str,
                "longitud": str,
                "nn": str,
                "tipo": parse_tipo,
                "empresa": parse_empresa,
                "partido": dospuntos,
                "localidad": dospuntos,
                "afectados": number,
            }
        incidente_dict = {header: func(value.strip()) 
                          for (header, func), value in zip(headers.items(), incidente)}
        nuevos.append(incidente_dict)
    return nuevos

def main():
    with httpx.Client(headers=HEADERS, timeout=20.0, verify=True) as client:
        r = client.get(URL)
        r.raise_for_status()
        content = r.text

    incidentes = parse_incidentes(content)

    fieldnames = [
        "latitud", "longitud", "nn", "tipo", "empresa", "partido",
        "localidad", "subestacion", "alimentador", "afectados",
        "normalizacion estimada"
    ]

    with open("cortes_enre.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(incidentes)

if __name__ == "__main__":
    main()
