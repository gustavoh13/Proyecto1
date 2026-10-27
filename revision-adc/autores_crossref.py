#!/usr/bin/env python3
"""Completa con Crossref los autores y los datos bibliográficos de las referencias.

Scopus solo da el primer autor. Para cada DOI de 04-metadatos.csv (y de las
referencias teóricas con DOI) se consulta api.crossref.org y se guardan todos
los autores, la revista, el volumen, el número, las páginas y el año. Los
estudios sin DOI se buscan por título (query.bibliographic) y solo se aceptan
si el título devuelto coincide.

Uso: autores_crossref.py 04-metadatos.csv 09-crossref.json
"""
import csv
import json
import re
import sys
import time
import unicodedata
import urllib.parse
import urllib.request

AGENTE = "revision-adc/1.0 (scoping review; mailto:revision-adc@example.org)"
# Referencias teóricas y metodológicas con DOI, para verificar sus datos
EXTERNAS = {
    "Arksey 2005": "10.1080/1364557032000119616", "Kellner 2007": "10.1007/s11519-007-0004-2",
    "Luke 2012": "10.1080/00405841.2012.636324", "Mongeon 2016": "10.1007/s11192-015-1765-5",
    "New London Group 1996": "10.17763/haer.66.1.17370n67v22j160u", "Page 2021": "10.1136/bmj.n71",
    "Pangrazio 2016": "10.1080/01596306.2014.942836", "Redecker 2017": "10.2760/159770",
    "Tricco 2018": "10.7326/M18-0850", "Vuorikari 2022": "10.2760/115376",
}


def pedir(url):
    req = urllib.request.Request(url, headers={"User-Agent": AGENTE})
    for intento in range(4):
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                return json.load(r)["message"]
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return None
            time.sleep(2 ** (intento + 1))
        except urllib.error.URLError:
            time.sleep(2 ** (intento + 1))
    return None


def normal(t):
    t = unicodedata.normalize("NFKD", t or "").encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", " ", t).strip()


def ficha(m):
    anio = (m.get("published-print") or m.get("published-online") or m.get("issued") or {}).get("date-parts", [[None]])[0][0]
    return {
        "autores": [{"family": a.get("family") or a.get("name", ""), "given": a.get("given", "")}
                    for a in m.get("author", [])],
        "titulo": (m.get("title") or [""])[0], "revista": (m.get("container-title") or [""])[0],
        "volumen": m.get("volume", ""), "numero": m.get("issue", ""), "paginas": m.get("page", ""),
        "articulo": m.get("article-number", ""), "anio": anio, "doi": m.get("DOI", ""),
    }


def main():
    meta = list(csv.DictReader(open(sys.argv[1], encoding="utf-8-sig")))
    salida = {"corpus": {}, "externas": {}}
    for f in meta:
        if f["doi"]:
            m = pedir(f"https://api.crossref.org/works/{urllib.parse.quote(f['doi'])}")
        else:
            q = urllib.parse.urlencode({"query.bibliographic": f["titulo"], "rows": 1})
            res = pedir(f"https://api.crossref.org/works?{q}")
            m = (res or {}).get("items", [None])[0] if res else None
            if m and normal((m.get("title") or [""])[0])[:60] != normal(f["titulo"])[:60]:
                m = None
        salida["corpus"][f["eid"]] = ficha(m) if m else None
        time.sleep(0.1)
    for clave, doi in EXTERNAS.items():
        m = pedir(f"https://api.crossref.org/works/{urllib.parse.quote(doi)}")
        salida["externas"][clave] = ficha(m) if m else None
    json.dump(salida, open(sys.argv[2], "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    vacios = [k for k, v in salida["corpus"].items() if not v]
    print(f"{len(meta) - len(vacios)} de {len(meta)} estudios con datos de Crossref; sin datos: {vacios}", file=sys.stderr)


if __name__ == "__main__":
    main()
