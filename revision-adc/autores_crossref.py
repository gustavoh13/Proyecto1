#!/usr/bin/env python3
"""Completa con Crossref los autores y los datos bibliográficos de las referencias.

Scopus solo da el primer autor. Para cada DOI de 04-metadatos.csv (y de las
referencias teóricas con DOI) se consulta api.crossref.org y se guardan todos
los autores, la revista, el volumen, el número, las páginas y el año. Los
estudios sin DOI se buscan por título (query.bibliographic) y solo se aceptan
si el título devuelto coincide. Se descartan las «autorías» que en realidad son
instituciones. Si Crossref no tiene autores, se prueba con doi.org (que también
resuelve DOI de mEDRA y DataCite) y después con OpenAlex.

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


INSTITUCION = re.compile(r"universit|institut|college|school|faculty|department|ministr|council|centre|center", re.I)


def personas(lista):
    """Autores personales: descarta entradas sin nombre de pila que son instituciones."""
    salida = []
    for a in lista or []:
        familia = a.get("family") or a.get("name") or a.get("literal") or ""
        if not a.get("given") and (INSTITUCION.search(familia) or "," in familia):
            continue
        salida.append({"family": familia, "given": a.get("given", "")})
    return salida


def por_doi_org(doi):
    req = urllib.request.Request(f"https://doi.org/{doi}", headers={
        "Accept": "application/vnd.citationstyles.csl+json", "User-Agent": AGENTE})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.load(r)
    except (urllib.error.URLError, ValueError):
        return None


def por_openalex(doi, titulo):
    if doi:
        url = f"https://api.openalex.org/works/doi:{urllib.parse.quote(doi)}"
    else:
        url = "https://api.openalex.org/works?" + urllib.parse.urlencode({"search": titulo, "per-page": 1})
    req = urllib.request.Request(url, headers={"User-Agent": AGENTE})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            w = json.load(r)
    except (urllib.error.URLError, ValueError):
        return None
    if "results" in w:
        w = (w["results"] or [None])[0]
        if not w or normal(w.get("title"))[:60] != normal(titulo)[:60]:
            return None
    nombres = []
    for a in w.get("authorships", []):
        completo = (a.get("author") or {}).get("display_name", "")
        partes = completo.rsplit(" ", 1)
        nombres.append({"family": partes[-1], "given": partes[0] if len(partes) > 1 else "", "completo": completo})
    return nombres


def ficha(m):
    anio = (m.get("published-print") or m.get("published-online") or m.get("issued") or {}).get("date-parts", [[None]])[0][0]
    return {
        "autores": personas(m.get("author")),
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
        datos = ficha(m) if m else None
        if not datos or not datos["autores"]:
            csl = por_doi_org(f["doi"]) if f["doi"] else None
            autores = personas(csl.get("author")) if csl else []
            fuente = "doi.org"
            if not autores:
                autores = por_openalex(f["doi"], f["titulo"]) or []
                fuente = "OpenAlex"
            if autores:
                datos = datos or {"titulo": f["titulo"], "revista": f["revista"], "volumen": "", "numero": "",
                                  "paginas": "", "articulo": "", "anio": f["anio"], "doi": f["doi"]}
                datos["autores"], datos["fuente_autores"] = autores, fuente
        salida["corpus"][f["eid"]] = datos
        time.sleep(0.1)
    for clave, doi in EXTERNAS.items():
        m = pedir(f"https://api.crossref.org/works/{urllib.parse.quote(doi)}")
        if m:
            salida["externas"][clave] = ficha(m)
        else:
            csl = por_doi_org(doi)
            salida["externas"][clave] = {"autores": personas(csl.get("author")), "titulo": csl.get("title", ""),
                                         "anio": (csl.get("issued") or {}).get("date-parts", [[None]])[0][0],
                                         "doi": doi} if csl else None
    json.dump(salida, open(sys.argv[2], "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    vacios = [k for k, v in salida["corpus"].items() if not v]
    print(f"{len(meta) - len(vacios)} de {len(meta)} estudios con datos de Crossref; sin datos: {vacios}", file=sys.stderr)


if __name__ == "__main__":
    main()
