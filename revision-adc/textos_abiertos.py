#!/usr/bin/env python3
"""Busca en OpenAlex la versión en acceso abierto de los estudios sorteados y descarga los PDF.

Para cada DOI de 10-muestra-validacion.csv guarda el estado de acceso abierto,
la licencia y los enlaces (PDF y página del artículo), e intenta bajar el PDF.
Solo se acepta un archivo que empiece como un PDF; si la página pide una
verificación contra robots o devuelve HTML, el texto queda como «no descargado»
y se indica el enlace para bajarlo a mano. Los PDF van a una carpeta aparte que
no se sube al repositorio.

Uso: textos_abiertos.py 10-muestra-validacion.csv 11-textos-abiertos.csv carpeta_pdf/
"""
import csv
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

AGENTE = "revision-adc/1.0 (scoping review; full-text validation)"


def pedir(url, intentos=4, tiempo=60):
    for intento in range(intentos):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": AGENTE, "Accept": "*/*"})
            with urllib.request.urlopen(req, timeout=tiempo) as r:
                return r.read(), r.headers.get("Content-Type", "")
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503) and intento < intentos - 1:
                time.sleep(5 * (intento + 1))
                continue
            return None, f"HTTP {e.code}"
        except Exception as e:
            if intento < intentos - 1:
                time.sleep(3)
                continue
            return None, type(e).__name__
    return None, "sin respuesta"


def main():
    filas = list(csv.DictReader(open(sys.argv[1], encoding="utf-8-sig")))
    carpeta = Path(sys.argv[3])
    carpeta.mkdir(parents=True, exist_ok=True)
    salida = []
    for x in filas:
        r = {"eid": x["eid"], "papel": x["papel"], "doi": x["doi"], "oa_status": "", "licencia": "",
             "pdf_url": "", "pagina_url": "", "archivo": "", "estado": ""}
        if x["doi"]:
            datos, _ = pedir("https://api.openalex.org/works/doi:" + urllib.parse.quote(x["doi"])
                             + "?select=open_access,best_oa_location,locations")
            if datos:
                w = json.loads(datos)
                mejor = w.get("best_oa_location") or {}
                r["oa_status"] = (w.get("open_access") or {}).get("oa_status", "")
                r["licencia"] = mejor.get("license") or ""
                r["pagina_url"] = mejor.get("landing_page_url") or (w.get("open_access") or {}).get("oa_url") or ""
                candidatos = [mejor.get("pdf_url")] + [l.get("pdf_url") for l in w.get("locations") or []
                                                       if l.get("is_oa")]
                candidatos = [c for c in dict.fromkeys(candidatos) if c]
                r["pdf_url"] = candidatos[0] if candidatos else ""
                for c in candidatos:
                    contenido, tipo = pedir(c, intentos=2)
                    if contenido and contenido[:5] == b"%PDF-":
                        nombre = re.sub(r"[^\w.-]", "_", x["eid"]) + ".pdf"
                        (carpeta / nombre).write_bytes(contenido)
                        r["archivo"], r["estado"], r["pdf_url"] = nombre, "descargado", c
                        break
                    r["estado"] = f"no descargado ({tipo or 'no es PDF'})"
                if not candidatos:
                    r["estado"] = "sin PDF en OpenAlex"
            time.sleep(1)
        else:
            r["estado"] = "sin DOI"
        salida.append(r)
        print(f"{x['papel']:8} {x['eid']} {r['estado']}", file=sys.stderr)
    with open(sys.argv[2], "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=list(salida[0]))
        w.writeheader()
        w.writerows(salida)


if __name__ == "__main__":
    main()
