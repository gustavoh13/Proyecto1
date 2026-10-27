#!/usr/bin/env python3
"""Segundo intento de obtener los textos abiertos que textos_abiertos.py no pudo bajar.

Para cada estudio sin texto reúne las páginas donde puede estar en acceso
abierto: la del DOI, las de todas las copias abiertas que lista OpenAlex
(repositorios institucionales incluidos) y el PDF que da Semantic Scholar. En
cada página busca la etiqueta citation_pdf_url, que las revistas publican para
los indexadores, y baja ese PDF. Si la página es el propio artículo en HTML,
guarda su texto. Las páginas que piden una verificación contra robots se dejan
como están: el texto queda sin obtener.

Uso: textos_abiertos_2.py 10-muestra-validacion.csv 11-textos-abiertos.csv carpeta_pdf/
     (actualiza 11-textos-abiertos.csv)
"""
import csv
import html
import json
import re
import sys
import time
import urllib.parse
from pathlib import Path

from textos_abiertos import pedir

PDF_META = re.compile(r'<meta[^>]+name=["\']citation_pdf_url["\'][^>]+content=["\']([^"\']+)', re.I)
PDF_META_2 = re.compile(r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+name=["\']citation_pdf_url', re.I)


def texto_html(pagina):
    pagina = re.sub(r"(?is)<(script|style|nav|header|footer)[^>]*>.*?</\1>", " ", pagina)
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"(?s)<[^>]+>", " ", pagina))).strip()


def paginas_candidatas(doi):
    candidatas = [f"https://doi.org/{doi}"]
    datos, _ = pedir("https://api.openalex.org/works/doi:" + urllib.parse.quote(doi) + "?select=locations")
    if datos:
        for l in json.loads(datos).get("locations") or []:
            if l.get("is_oa"):
                candidatas += [l.get("pdf_url"), l.get("landing_page_url")]
    time.sleep(1)
    datos, _ = pedir("https://api.semanticscholar.org/graph/v1/paper/DOI:" + urllib.parse.quote(doi)
                     + "?fields=openAccessPdf", intentos=3)
    if datos:
        candidatas.append((json.loads(datos).get("openAccessPdf") or {}).get("url"))
    return [c for c in dict.fromkeys(candidatas) if c]


def main():
    muestra = {x["eid"]: x for x in csv.DictReader(open(sys.argv[1], encoding="utf-8-sig"))}
    filas = list(csv.DictReader(open(sys.argv[2], encoding="utf-8-sig")))
    carpeta = Path(sys.argv[3])
    for r in filas:
        if r["estado"] == "descargado" or not r["doi"]:
            continue
        nombre = re.sub(r"[^\w.-]", "_", r["eid"])
        for url in paginas_candidatas(r["doi"]):
            contenido, tipo = pedir(url, intentos=2)
            if not contenido:
                continue
            if contenido[:5] == b"%PDF-":
                (carpeta / f"{nombre}.pdf").write_bytes(contenido)
                r["archivo"], r["estado"], r["pdf_url"] = f"{nombre}.pdf", "descargado", url
                break
            pagina = contenido.decode("utf-8", "replace")
            if "Just a moment" in pagina[:3000] or "challenge-platform" in pagina:
                continue
            m = PDF_META.search(pagina) or PDF_META_2.search(pagina)
            if m:
                enlace = urllib.parse.urljoin(url, html.unescape(m.group(1)))
                pdf, _ = pedir(enlace, intentos=2)
                if pdf and pdf[:5] == b"%PDF-":
                    (carpeta / f"{nombre}.pdf").write_bytes(pdf)
                    r["archivo"], r["estado"], r["pdf_url"] = f"{nombre}.pdf", "descargado", enlace
                    break
            # El artículo completo en HTML: muchas palabras y una lista de referencias
            texto = texto_html(pagina)
            if len(texto.split()) > 4000 and re.search(r"\bReferences\b|\bReferencias\b|\bBibliograf", texto):
                (carpeta / f"{nombre}.txt").write_text(texto, encoding="utf-8")
                r["archivo"], r["estado"], r["pagina_url"] = f"{nombre}.txt", "descargado (HTML)", url
                break
        print(f"{r['papel']:8} {muestra[r['eid']]['primer_autor']:22} {r['estado']}", file=sys.stderr)
        time.sleep(1)
    with open(sys.argv[2], "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=list(filas[0]))
        w.writeheader()
        w.writerows(filas)


if __name__ == "__main__":
    main()
