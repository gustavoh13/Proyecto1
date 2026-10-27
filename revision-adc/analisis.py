#!/usr/bin/env python3
"""Análisis de los estudios incluidos: tablas, pruebas de tendencia y robustez.

Lee 03-codificacion.csv y escribe 07-analisis.json con todo lo que el
artículo informa: distribución por año e idioma, categorías por periodo con
la prueba de tendencia de Cochran-Armitage, crecimiento anual estimado con
una regresión de Poisson (2016-2025), coocurrencias entre tradiciones y
objetos de la crítica, países, y la comparación con diccionarios estrictos
(consultados de nuevo en Scopus) para comprobar que las tendencias no
dependen de los términos elegidos.

Uso: analisis.py 03-codificacion.csv 07-analisis.json
"""
import csv
import json
import math
import sys
import time
import urllib.parse
import urllib.request
from collections import Counter

import numpy as np
from scipy import stats

URL = "https://api.elsevier.com/content/search/scopus"
PERIODOS = ["2016-2019", "2020-2023", "2024-2026"]

# Diccionarios estrictos: solo los términos menos ambiguos de cada categoría
ESTRICTOS = {
    "nivel: Infantil y primaria": '"primary school*" OR "primary education" OR "elementary school*" OR "early childhood"',
    "nivel: Secundaria": '"secondary school*" OR "secondary education" OR "high school*"',
    "nivel: Universidad": '"higher education" OR "university students" OR undergraduate*',
    "nivel: Formación docente": '"pre-service teacher*" OR "preservice teacher*" OR "teacher education" OR "initial teacher education"',
    "tema: Inteligencia artificial": '"generative AI" OR "generative artificial intelligence" OR chatgpt OR "large language model*" OR genai',
    "tema: Algoritmos, datos y plataformas": 'platform* OR algorithm* OR datafication',
    "tema: Redes sociales": '"social media"',
}


def periodo(anio):
    a = int(anio)
    return PERIODOS[0] if a <= 2019 else PERIODOS[1] if a <= 2023 else PERIODOS[2]


def cochran_armitage(x, n):
    """Prueba de tendencia para proporciones ordenadas (puntuaciones 1, 2, 3)."""
    x, n, t = np.array(x, float), np.array(n, float), np.arange(1, len(x) + 1, dtype=float)
    p = x.sum() / n.sum()
    if p in (0, 1):
        return float("nan"), float("nan")
    T = (t * (x - n * p)).sum()
    var = p * (1 - p) * ((n * t ** 2).sum() - (n * t).sum() ** 2 / n.sum())
    z = T / math.sqrt(var)
    return z, 2 * stats.norm.sf(abs(z))


def poisson(anios, y):
    """Regresión de Poisson log(mu) = a + b * año, por IRLS, con IC al 95 %."""
    X = np.column_stack([np.ones(len(anios)), np.array(anios, float) - anios[0]])
    y = np.array(y, float)
    beta = np.array([math.log(y.mean()), 0.0])
    for _ in range(100):
        mu = np.exp(X @ beta)
        W = np.diag(mu)
        beta_n = beta + np.linalg.solve(X.T @ W @ X, X.T @ (y - mu))
        if np.abs(beta_n - beta).max() < 1e-10:
            beta = beta_n
            break
        beta = beta_n
    mu = np.exp(X @ beta)
    cov = np.linalg.inv(X.T @ np.diag(mu) @ X)
    disp = float(((y - mu) ** 2 / mu).sum() / (len(y) - 2))
    # Si hay sobredispersión se escala el error típico (cuasi-Poisson)
    se = math.sqrt(cov[1, 1] * max(disp, 1.0))
    b = float(beta[1])
    return {"tasa_anual": math.exp(b) - 1, "ic95": [math.exp(b - 1.96 * se) - 1, math.exp(b + 1.96 * se) - 1],
            "dispersion": disp, "p": float(2 * stats.norm.sf(abs(b / se)))}


def coinciden(eids, terminos):
    hallados = set()
    for i in range(0, len(eids), 40):
        trozo = " OR ".join(f"EID({e})" for e in eids[i:i + 40])
        consulta = f"({trozo}) AND TITLE-ABS-KEY({terminos})"
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


def por_periodo(filas, marca):
    n = [sum(1 for f in filas if periodo(f["anio"]) == p) for p in PERIODOS]
    x = [sum(1 for f in filas if periodo(f["anio"]) == p and marca(f)) for p in PERIODOS]
    z, pval = cochran_armitage(x, n)
    return {"n": n, "x": x, "total": sum(x), "z": z, "p": pval}


def main():
    filas = list(csv.DictReader(open(sys.argv[1], encoding="utf-8-sig")))
    codigos = [k for k in filas[0] if k.split(":")[0] in ("nivel", "diseño", "marco", "tema")]
    res = {"n": len(filas)}
    res["por_anio"] = sorted(Counter((f["anio"], f["idioma"]) for f in filas).items())
    anios = list(range(2016, 2026))
    res["crecimiento_2016_2025"] = poisson(anios, [sum(1 for f in filas if int(f["anio"]) == a) for a in anios])
    res["categorias"] = {k: por_periodo(filas, lambda f, k=k: f[k] == "1") for k in codigos}
    res["categorias"]["idioma: español"] = por_periodo(filas, lambda f: f["idioma"] == "español")
    res["sin_nivel"] = sum(1 for f in filas if not any(f[k] for k in codigos if k.startswith("nivel")))
    res["sin_diseno"] = sum(1 for f in filas if not any(f[k] for k in codigos if k.startswith("diseño")))
    marcos = [k for k in codigos if k.startswith("marco")]
    temas = [k for k in codigos if k.startswith("tema")]
    res["coocurrencias"] = {m: {t: sum(1 for f in filas if f[m] and f[t]) for t in temas} for m in marcos}
    res["paises"] = Counter(p for f in filas for p in f["paises"].split("; ") if p).most_common()
    res["revistas"] = Counter(f["revista"] for f in filas).most_common(12)
    res["citas"] = {"total": sum(int(f["citas"] or 0) for f in filas),
                    "mediana": float(np.median([int(f["citas"] or 0) for f in filas]))}
    res["acceso_abierto"] = sum(1 for f in filas if f["acceso_abierto"] == "True")
    eids = [f["eid"] for f in filas]
    robustez = {}
    for k, terminos in ESTRICTOS.items():
        hallados = coinciden(eids, terminos)
        robustez[k] = {"amplio": res["categorias"][k], "estricto": por_periodo(filas, lambda f: f["eid"] in hallados)}
    res["robustez"] = robustez
    json.dump(res, open(sys.argv[2], "w", encoding="utf-8"), ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
