# La lista de ccchallenge.org leida por su API publica, cruzada con los temas
# del laboratorio. Solo lee; no envia nada.
#
# Uso: python -B -X utf8 ccchallenge_lista.py
# Imprime titulos y estados, no los resumenes.
import datetime
import json
import re
import urllib.request
from collections import Counter

URL = "https://ccchallenge.org/api/papers"

peticion = urllib.request.Request(URL, headers={"User-Agent": "Mozilla/5.0"})
with urllib.request.urlopen(peticion, timeout=60) as respuesta:
    datos = json.load(respuesta)
registros = datos["items"]


def linea(x):
    titulo = " ".join(x["title"].split())
    return f'  {x["bibtex_key"]:26} {str(x["year"]):>4} {x["formalisation_status"]:22} {titulo[:95]}'


print(f"Leido de {URL} el {datetime.date.today()}")
print(f"Registros: {len(registros)} (total declarado: {datos.get('total')})")
print(f"Con resumen: {sum(1 for x in registros if x.get('abstract'))}")
print("Estados:")
for estado, cuantos in Counter(x["formalisation_status"] for x in registros).most_common():
    print(f"  {estado:22} {cuantos}")

print("\nLos tres de nuestros articulos:")
for x in registros:
    if x["bibtex_key"] in ("Gao1993", "Garner1985", "Wu1992"):
        print(linea(x))

temas = {
    "consecutivos, altura o coalescencia": r"consecutive|same height|coalesc|height|runs? of|tuple|streak",
    "pares, fusion o vecinos": r"merg|pair|neighbo|adjacent|twin|confluen",
    "densidad o casi todos": r"density|almost all|almost every|positive proportion",
    "predecesores o arboles": r"predecessor|inverse|tree|backward",
}
for tema, patron in temas.items():
    rx = re.compile(patron, re.I)
    elegidos = [x for x in registros if rx.search(x["title"]) or rx.search(x.get("abstract") or "")]
    print(f"\nTitulo o resumen con {tema}: {len(elegidos)}")
    for x in elegidos:
        print(linea(x))

print("\nCon formalizacion hecha o en marcha:")
for x in registros:
    if x["formalisation_status"] != "not_started":
        print(linea(x))
