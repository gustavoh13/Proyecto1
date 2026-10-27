#!/usr/bin/env python3
"""Segunda fase de cribado, independiente del título, y arbitraje de discrepancias.

La clave sin suscripción no devuelve los resúmenes, pero Scopus sí busca en
ellos. Para cada conjunto de términos se consulta EID(...) AND ABS(...) o
KEY(...) y se anota qué registros coinciden. La fase 2 no mira el título:
incluye un registro si sus palabras clave nombran la ADC, o si su resumen la
nombra y además aborda una dimensión de poder.

Cuando las dos fases no coinciden decide una regla fijada de antemano: se
incluye si el título nombra la ADC, o si el título se refiere a tecnologías
digitales y hay al menos dos indicios entre palabras clave, resumen y
dimensión de poder. Las exclusiones por contexto o tipo de documento de la
fase 1 se mantienen.

Uso: cribado_resumenes.py 02-cribado.csv 05-cribado-resumenes.csv
"""
import csv
import json
import re
import sys
import time
import urllib.parse
import urllib.request

URL = "https://api.elsevier.com/content/search/scopus"

CONJUNTOS = {
    # Nombra de forma explícita una alfabetización crítica de lo digital
    "adc_explicita": '"critical digital literac*" OR "critical digital media literac*" OR "critical media literac*" '
                     'OR "critical AI literac*" OR "critical data literac*" OR "critical algorithmic literac*" '
                     'OR "critical internet literac*" OR "critical information literac*" '
                     'OR "alfabetización digital crítica" OR "alfabetización crítica digital" '
                     'OR "literacidad digital crítica" OR "literacidades digitales críticas" '
                     'OR "competencia digital crítica" OR "alfabetización mediática crítica"',
    # Dimensión sociopolítica: poder, ideología, desigualdad, plataformas
    "dimension_poder": 'power OR ideolog* OR hegemon* OR "social justice" OR emancipat* OR oppress* '
                       'OR inequalit* OR inequit* OR racis* OR sexis* OR capitalis* OR "political economy" '
                       'OR surveillance OR datafication OR platformi* OR "critical pedagog*" OR "critical literac*" '
                       'OR democra* OR activis* OR decoloni* OR colonial* OR "critical race" OR resistan* OR justice '
                       'OR marginali* OR gender OR feminis* OR queer '
                       'OR poder OR "justicia social" OR desigualdad* OR hegemónic* OR género',
    # Pensamiento crítico genérico (indicio de un uso de "crítico" ajeno a la ADC)
    "pensamiento_critico": '"critical thinking" OR "pensamiento crítico"',
}
# Los mismos términos, buscados por separado en las palabras clave y en el resumen
NOMBRA_ADC = CONJUNTOS["adc_explicita"]

# El título nombra una alfabetización crítica de lo digital (o un equivalente explícito)
TITULO_NOMBRA = re.compile(
    r"critical\s+(digital\s+|internet\s+|AI\s+|data\s+|algorithmic\s+|race\s+(digital|algorithmic)\s+)"
    r"(media\s+)?(literac|competence)"
    r"|critical\s+media\s+literac|critical\s+(and|&)\s+digital|\(critical\)\s+digital\s+literac|\bCDL\b"
    r"|alfabetizaci[oó]n\s+(digital\s+cr[ií]tica|cr[ií]tica\s+digital)|literacidad(es)?\s+digital(es)?\s+cr[ií]tica"
    r"|competencia\s+digital\s+cr[ií]tica", re.I)
# El título se refiere a tecnologías digitales
TITULO_DIGITAL = re.compile(
    r"digital|online|internet|\bweb\b|\bAI\b|artificial intelligence|chatgpt|\bgpt|genai|chatbot|social media|"
    r"social network|platform|tiktok|instagram|snapchat|whatsapp|twitter|youtube|wikipedia|video ?game|cyber|"
    r"virtual|algorithm|\bdata\b|metaverse|technolog|#|coding|programming|computer|e-learning|mobile|wearable|"
    r"immersive|extended reality", re.I)


def coinciden(eids, terminos):
    hallados = set()
    for i in range(0, len(eids), 40):
        trozo = " OR ".join(f"EID({e})" for e in eids[i:i + 40])
        consulta = f"({trozo}) AND (ABS({terminos}) OR KEY({terminos}))"
        inicio = 0
        while True:
            url = URL + "?" + urllib.parse.urlencode({"query": consulta, "count": 25, "start": inicio, "field": "eid"})
            req = urllib.request.Request(url, headers={"Accept": "application/json"})
            with urllib.request.urlopen(req, timeout=60) as r:
                res = json.load(r)["search-results"]
            entradas = [e for e in res.get("entry", []) if "eid" in e]
            hallados |= {e["eid"] for e in entradas}
            inicio += 25
            if inicio >= int(res["opensearch:totalResults"]) or not entradas:
                break
            time.sleep(0.2)
    return hallados


def coinciden_campo(eids, campo, terminos):
    """Como coinciden, pero en un solo campo (KEY o ABS)."""
    hallados = set()
    for i in range(0, len(eids), 40):
        trozo = " OR ".join(f"EID({e})" for e in eids[i:i + 40])
        consulta = f"({trozo}) AND {campo}({terminos})"
        inicio = 0
        while True:
            url = URL + "?" + urllib.parse.urlencode({"query": consulta, "count": 25, "start": inicio, "field": "eid"})
            req = urllib.request.Request(url, headers={"Accept": "application/json"})
            with urllib.request.urlopen(req, timeout=60) as r:
                res = json.load(r)["search-results"]
            entradas = [e for e in res.get("entry", []) if "eid" in e]
            hallados |= {e["eid"] for e in entradas}
            inicio += 25
            if inicio >= int(res["opensearch:totalResults"]) or not entradas:
                break
            time.sleep(0.2)
    return hallados


def arbitrar(f):
    """Decisión final: los acuerdos se mantienen y las discrepancias pasan por la regla."""
    if f["fase1"].startswith("Excluido: contexto") or f["fase1"].startswith("Excluido: tipo"):
        f["regla"] = "exclusión por contexto o tipo de documento"
        return "Excluido"
    if not f["discrepancia"]:
        f["regla"] = "acuerdo entre fases"
        return "Incluido" if f["fase1"] == "Incluido" else "Excluido"
    if f["T_nombra"]:
        f["regla"] = "discrepancia: el título nombra la ADC"
        return "Incluido"
    indicios = sum(1 for k in ("K_claves", "A_resumen", "P_poder") if f[k])
    if f["T_digital"] and indicios >= 2:
        f["regla"] = "discrepancia: título digital y dos indicios de resumen o palabras clave"
        return "Incluido"
    f["regla"] = "discrepancia: indicios insuficientes"
    return "Excluido"


def main():
    filas = list(csv.DictReader(open(sys.argv[1], encoding="utf-8-sig")))
    eids = [f["eid"] for f in filas]
    claves = coinciden_campo(eids, "KEY", NOMBRA_ADC)
    resumen = coinciden_campo(eids, "ABS", NOMBRA_ADC)
    poder = coinciden(eids, CONJUNTOS["dimension_poder"])
    generico = coinciden(eids, CONJUNTOS["pensamiento_critico"])
    for f in filas:
        f["fase1"] = f.pop("decision")
        f["K_claves"] = "1" if f["eid"] in claves else ""
        f["A_resumen"] = "1" if f["eid"] in resumen else ""
        f["P_poder"] = "1" if f["eid"] in poder else ""
        f["pensamiento_critico"] = "1" if f["eid"] in generico else ""
        f["T_nombra"] = "1" if TITULO_NOMBRA.search(f["titulo"]) else ""
        f["T_digital"] = "1" if TITULO_DIGITAL.search(f["titulo"]) else ""
        # Fase 2: las palabras clave nombran la ADC, o el resumen la nombra y aborda el poder
        f["fase2"] = "Incluido" if (f["K_claves"] or (f["A_resumen"] and f["P_poder"])) else "Excluido"
        f["discrepancia"] = "1" if (f["fase1"] == "Incluido") != (f["fase2"] == "Incluido") else ""
        f["decision"] = arbitrar(f)
    campos = ["n", "eid", "anio", "titulo", "revista", "fase1", "T_nombra", "T_digital", "K_claves", "A_resumen",
              "P_poder", "pensamiento_critico", "fase2", "discrepancia", "regla", "decision"]
    with open(sys.argv[2], "w", newline="", encoding="utf-8-sig") as s:
        w = csv.DictWriter(s, fieldnames=campos, extrasaction="ignore")
        w.writeheader()
        w.writerows(filas)


if __name__ == "__main__":
    main()
