#!/usr/bin/env python3
"""Busca en Scopus con la Scopus Search API de Elsevier y guarda los
resultados en CSV.

La consulta usa la sintaxis de la búsqueda avanzada de Scopus, por ejemplo
TITLE-ABS-KEY("learning analytics") AND PUBYEAR > 2015. Los resultados se
recorren con cursor si la clave lo admite (suscripción institucional); si no,
por posición, con el tope de 5000 resultados que fija la API.

La clave se lee de la variable SCOPUS_API_KEY y, si existe, el token
institucional de SCOPUS_INSTTOKEN (hace falta para consultar desde fuera de
la red de la universidad). En Claude Code en la nube la clave puede
guardarse como secreto de red del entorno, con el sitio api.elsevier.com y
la cabecera X-ELS-APIKey sin prefijo; entonces la añade el proxy y la
variable no hace falta. Solo usa la biblioteca estándar.

Uso: scopus.py 'CONSULTA' [-o resultados.csv] [-n MAX] [--vista STANDARD|COMPLETE]
                 [--orden=-citedby-count]
"""
import argparse
import csv
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

URL = "https://api.elsevier.com/content/search/scopus"
# Máximo de registros por petición que admite cada vista
POR_PAGINA = {"STANDARD": 200, "COMPLETE": 25}
# Límites de una clave sin suscripción institucional, que no admite cursor
SIN_CURSOR, TOPE_SIN_CURSOR = 25, 5000
COLUMNAS = [
    "eid", "doi", "titulo", "autores", "primer_autor", "revista", "issn",
    "eissn", "volumen", "numero", "paginas", "fecha", "anio", "tipo",
    "citas", "acceso_abierto", "palabras_clave", "resumen", "enlace",
]


class SinCursor(Exception):
    """La clave no admite el cursor (solo con suscripción institucional)."""


def pedir(params, cabeceras, intentos=4):
    url = URL + "?" + urllib.parse.urlencode(params)
    for intento in range(intentos):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=cabeceras), timeout=60) as r:
                return json.load(r), r.headers
        except urllib.error.HTTPError as e:
            cuerpo = e.read().decode("utf-8", "replace")
            # 429: cuota por segundo superada; 5xx: fallo pasajero del servidor
            if (e.code == 429 or e.code >= 500) and intento < intentos - 1:
                time.sleep(2 ** (intento + 1))
                continue
            if e.code in (400, 403) and "cursor" in params and (
                    "cursor" in cuerpo or "maximum number allowed" in cuerpo):
                raise SinCursor
            motivo = {
                401: "la clave no es válida o falta el token institucional",
                403: "la clave no tiene permiso para esta vista o consulta"
                     " (COMPLETE requiere acceso institucional)",
                429: "se agotó la cuota de la clave",
            }.get(e.code, "error de la API")
            sys.exit(f"Scopus respondió {e.code}: {motivo}.\n{cuerpo[:500]}")
        except urllib.error.URLError as e:
            if intento < intentos - 1:
                time.sleep(2 ** (intento + 1))
                continue
            sys.exit(f"No se pudo conectar con api.elsevier.com ({e.reason})."
                     " Comprueba que el dominio esté permitido en el entorno.")


def fila(e):
    autores = e.get("author") or []
    nombres = "; ".join(a.get("authname", "") for a in autores) or e.get("dc:creator", "")
    enlace = next((l["@href"] for l in e.get("link", []) if l.get("@ref") == "scopus"), "")
    pagina = e.get("prism:pageRange") or ""
    return {
        "eid": e.get("eid", ""),
        "doi": e.get("prism:doi", ""),
        "titulo": e.get("dc:title", ""),
        "autores": nombres,
        "primer_autor": e.get("dc:creator", ""),
        "revista": e.get("prism:publicationName", ""),
        "issn": e.get("prism:issn", ""),
        "eissn": e.get("prism:eIssn", ""),
        "volumen": e.get("prism:volume", ""),
        "numero": e.get("prism:issueIdentifier", ""),
        "paginas": pagina,
        "fecha": e.get("prism:coverDate", ""),
        "anio": e.get("prism:coverDate", "")[:4],
        "tipo": e.get("subtypeDescription", ""),
        "citas": e.get("citedby-count", ""),
        "acceso_abierto": e.get("openaccessFlag", ""),
        "palabras_clave": (e.get("authkeywords") or "").replace(" | ", "; "),
        "resumen": e.get("dc:description", ""),
        "enlace": enlace,
    }


def main():
    p = argparse.ArgumentParser(description="Busca en Scopus y guarda los resultados en CSV.")
    p.add_argument("consulta", help="consulta con la sintaxis avanzada de Scopus")
    p.add_argument("-o", "--salida", default="scopus.csv", help="archivo CSV (por defecto scopus.csv)")
    p.add_argument("-n", "--max", type=int, default=0, help="máximo de registros (0 = todos)")
    p.add_argument("--vista", choices=POR_PAGINA, default="STANDARD",
                   help="COMPLETE añade todos los autores, palabras clave y resumen")
    p.add_argument("--orden", help="orden de Scopus, p. ej. --orden=-citedby-count (más citados) o --orden=-coverDate")
    args = p.parse_args()

    cabeceras = {"Accept": "application/json"}
    # Sin la variable, la clave la añade el proxy (secreto de red del entorno)
    if os.environ.get("SCOPUS_API_KEY"):
        cabeceras["X-ELS-APIKey"] = os.environ["SCOPUS_API_KEY"]
    if os.environ.get("SCOPUS_INSTTOKEN"):
        cabeceras["X-ELS-Insttoken"] = os.environ["SCOPUS_INSTTOKEN"]

    params = {"query": args.consulta, "view": args.vista, "cursor": "*"}
    if args.orden:
        params["sort"] = args.orden
    pagina, tope = POR_PAGINA[args.vista], 0
    escritos = total = 0
    # Con paginación por posición el orden puede variar entre peticiones y
    # repetir algún registro
    vistos = set()
    with open(args.salida, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=COLUMNAS)
        w.writeheader()
        while True:
            params["count"] = pagina
            if args.max:
                params["count"] = min(pagina, args.max - escritos)
            if tope:
                params["count"] = min(params["count"], tope - escritos)
            try:
                datos, cabeceras_resp = pedir(params, cabeceras)
            except SinCursor:
                # Sin suscripción: paginación por posición, 25 por petición y
                # como mucho los primeros 5000 resultados
                del params["cursor"]
                params["start"], pagina, tope = 0, SIN_CURSOR, TOPE_SIN_CURSOR
                continue
            res = datos["search-results"]
            total = int(res.get("opensearch:totalResults", 0))
            entradas = [e for e in res.get("entry", []) if "error" not in e]
            if args.max:
                entradas = entradas[: args.max - escritos]
            for e in entradas:
                if e.get("eid") not in vistos:
                    vistos.add(e.get("eid"))
                    w.writerow(fila(e))
            escritos += len(entradas)
            print(f"\r{escritos} de {total} registros", end="", file=sys.stderr)
            if not entradas or escritos >= total or (args.max and escritos >= args.max):
                break
            if tope:
                if escritos >= tope:
                    break
                params["start"] = escritos
            else:
                siguiente = res.get("cursor", {}).get("@next")
                if not siguiente:
                    break
                params["cursor"] = siguiente
            # La API admite unas pocas peticiones por segundo por clave
            time.sleep(0.2)
    print(file=sys.stderr)
    restantes = cabeceras_resp.get("X-RateLimit-Remaining")
    if tope and total > tope and escritos >= tope:
        print(f"Aviso: sin suscripción institucional la API solo entrega los primeros"
              f" {tope} de {total} resultados.", file=sys.stderr)
    print(f"Guardados {len(vistos)} registros en {args.salida}"
          + (f" (quedan {restantes} peticiones de la cuota semanal)" if restantes else ""),
          file=sys.stderr)


if __name__ == "__main__":
    main()
