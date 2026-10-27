#!/usr/bin/env python3
"""Añade volumen, número, páginas y número de artículo a los estudios incluidos.

La clave sin suscripción solo da el primer autor; estos campos sí están
disponibles en la Abstract Retrieval API. El número de autores sale de la
Search API y sirve para escribir bien las citas en el texto (APA 7: un autor,
dos autores o «et al.» a partir de tres).

Uso: metadatos.py 03-codificacion.csv 04-metadatos.csv
"""
import csv
import json
import sys
import time
import urllib.parse
import urllib.request

CAMPOS = "dc:creator,prism:volume,prism:issueIdentifier,prism:pageRange,article-number"


def main():
    filas = list(csv.DictReader(open(sys.argv[1], encoding="utf-8-sig")))
    salida = []
    for f in filas:
        url = f"https://api.elsevier.com/content/abstract/eid/{f['eid']}?field={CAMPOS}"
        req = urllib.request.Request(url, headers={"Accept": "application/json"})
        with urllib.request.urlopen(req, timeout=60) as r:
            c = json.load(r)["abstracts-retrieval-response"]["coredata"] or {}
        autor = ((c.get("dc:creator") or {}).get("author") or [{}])[0]
        nombre = autor.get("preferred-name") or autor
        salida.append({
            "eid": f["eid"], "doi": f["doi"], "anio": f["anio"],
            "apellido": nombre.get("ce:surname", ""), "iniciales": nombre.get("ce:initials", ""),
            "titulo": f["titulo"], "revista": f["revista"],
            "volumen": c.get("prism:volume") or "", "numero": c.get("prism:issueIdentifier") or "",
            "paginas": c.get("prism:pageRange") or "", "articulo": c.get("article-number") or "",
        })
        consulta = urllib.parse.urlencode({"query": f"EID({f['eid']})", "field": "author-count"})
        req = urllib.request.Request(f"https://api.elsevier.com/content/search/scopus?{consulta}",
                                     headers={"Accept": "application/json"})
        with urllib.request.urlopen(req, timeout=60) as r:
            entrada = json.load(r)["search-results"]["entry"][0]
        salida[-1]["n_autores"] = (entrada.get("author-count") or {}).get("$", "")
        time.sleep(0.15)
    with open(sys.argv[2], "w", newline="", encoding="utf-8-sig") as s:
        w = csv.DictWriter(s, fieldnames=list(salida[0]))
        w.writeheader()
        w.writerows(salida)


if __name__ == "__main__":
    main()
