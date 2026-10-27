#!/usr/bin/env python3
"""Codifica los estudios incluidos con consultas a Scopus.

La clave sin suscripción no da acceso a los resúmenes, pero Scopus sí busca
en ellos. Para cada código se consulta EID(...) AND TITLE-ABS-KEY(términos)
sobre los estudios incluidos, y un estudio recibe el código si aparece en
la respuesta: es decir, si los términos están en su título, resumen o
palabras clave.

Uso: codificar.py 02-cribado.csv 03-codificacion.csv
"""
import csv
import json
import sys
import time
import urllib.parse
import urllib.request

URL = "https://api.elsevier.com/content/search/scopus"

# (dimensión, código, términos de TITLE-ABS-KEY)
CODIGOS = [
    ("nivel", "Infantil y primaria", '"early childhood" OR preschool OR kindergarten OR "primary school" OR "primary education" OR "elementary school" OR "elementary classroom" OR "fourth-grade" OR "educación infantil" OR "educación primaria"'),
    ("nivel", "Secundaria", '"secondary school" OR "secondary education" OR "high school" OR "middle school" OR adolescen* OR teenager* OR "ninth-grade" OR "educación secundaria" OR bachillerato'),
    ("nivel", "Universidad", '"higher education" OR universit* OR undergraduate* OR college OR "graduate students" OR "educación superior"'),
    ("nivel", "Formación docente", '"teacher education" OR "teacher training" OR "pre-service" OR preservice OR "student teachers" OR "future teachers" OR "teacher candidates" OR "initial teacher" OR "formación docente" OR "formación del profesorado" OR "futuros docentes" OR "professional development"'),
    ("diseño", "Revisión de literatura", '"systematic review" OR "literature review" OR "scoping review" OR "narrative review" OR "revisión sistemática" OR "bibliometric"'),
    ("diseño", "Teórico o conceptual", 'theoretical OR "conceptual paper" OR "conceptual article" OR "we argue" OR "this essay" OR "this article argues" OR "this paper argues" OR ensayo OR "reflexión teórica"'),
    ("diseño", "Cualitativo", 'qualitative OR "case study" OR ethnograph* OR interview* OR "focus group*" OR "action research" OR narrative OR autoethnograph* OR "discourse analysis" OR cualitativ*'),
    ("diseño", "Cuantitativo", 'quantitative OR survey OR questionnaire OR "quasi-experimental" OR experiment* OR "pre-test" OR "pretest" OR scale OR psychometric OR "structural equation" OR cuantitativ* OR cuestionario'),
    ("diseño", "Diseño o intervención", 'intervention OR "design-based" OR "co-design" OR workshop* OR "teaching unit" OR module OR "didactic proposal" OR "pedagogical proposal" OR "lesson*" OR "propuesta didáctica" OR "secuencia didáctica"'),
    ("marco", "Pedagogía crítica (Freire)", 'freire* OR "critical pedagogy" OR "pedagogía crítica" OR emancipat* OR conscientiz*'),
    ("marco", "Multiliteracidades y nuevos estudios de literacidad", 'multiliterac* OR "new literacies" OR "new literacy studies" OR multimodal* OR "social semiotic*" OR "multiliteracidades"'),
    ("marco", "Alfabetización mediática", '"media literacy" OR "media education" OR educommunication OR "educomunicación" OR "alfabetización mediática" OR "media and information literacy"'),
    ("marco", "Ciudadanía digital", '"digital citizenship" OR "civic" OR citizenship OR "ciudadanía"'),
    ("marco", "Perspectivas críticas de raza, género y decolonialidad", 'race OR racism OR racial OR "critical race" OR gender OR feminis* OR queer OR decoloni* OR "género"'),
    ("tema", "Inteligencia artificial", '"artificial intelligence" OR "generative AI" OR genai OR chatgpt OR "large language model*" OR "inteligencia artificial"'),
    ("tema", "Desinformación y posverdad", 'misinformation OR disinformation OR "fake news" OR "post-truth" OR posverdad OR "desinformación" OR conspira*'),
    ("tema", "Redes sociales", '"social media" OR "social network*" OR instagram OR tiktok OR twitter OR youtube OR snapchat OR whatsapp OR "redes sociales"'),
    ("tema", "Algoritmos, datos y plataformas", 'algorithm* OR datafication OR "data literacy" OR platform* OR "big data" OR "algoritm*" OR "plataform*"'),
    ("tema", "Privacidad y vigilancia", 'privacy OR surveillance OR "privacidad" OR "vigilancia"'),
    ("tema", "Discurso de odio y radicalización", '"hate speech" OR radicali* OR extremis* OR "discurso de odio" OR fascis*'),
    ("tema", "Lenguas extranjeras", 'EFL OR ESL OR "English language teaching" OR "second language" OR "foreign language" OR L2 OR TESOL OR "lengua extranjera"'),
    ("tema", "Producción digital del alumnado", '"digital storytelling" OR "video production" OR "multimodal composing" OR "digital composing" OR podcast* OR "content creation" OR "media production" OR "relato digital"'),
]


def pedir(query):
    eids, start = set(), 0
    while True:
        url = URL + "?" + urllib.parse.urlencode({"query": query, "count": 25, "start": start, "field": "eid"})
        req = urllib.request.Request(url, headers={"Accept": "application/json"})
        with urllib.request.urlopen(req, timeout=60) as r:
            res = json.load(r)["search-results"]
        entradas = [e for e in res.get("entry", []) if "eid" in e]
        eids |= {e["eid"] for e in entradas}
        start += 25
        if start >= int(res["opensearch:totalResults"]) or not entradas:
            return eids
        time.sleep(0.2)


def main():
    filas = [f for f in csv.DictReader(open(sys.argv[1], encoding="utf-8-sig")) if f["decision"] == "Incluido"]
    todos = [f["eid"] for f in filas]
    trozos = [todos[i:i + 40] for i in range(0, len(todos), 40)]
    for dim, codigo, terminos in CODIGOS:
        hallados = set()
        for t in trozos:
            hallados |= pedir("(" + " OR ".join(f"EID({e})" for e in t) + f") AND TITLE-ABS-KEY({terminos})")
        for f in filas:
            f[f"{dim}: {codigo}"] = "1" if f["eid"] in hallados else ""
        print(f"{dim}: {codigo}: {len(hallados)}", file=sys.stderr)
    for f in filas:
        f.pop("decision")
    idioma = set()
    for t in trozos:
        idioma |= pedir("(" + " OR ".join(f"EID({e})" for e in t) + ") AND LANGUAGE(spanish)")
    for f in filas:
        f["idioma"] = "español" if f["eid"] in idioma else "inglés"
    with open(sys.argv[2], "w", newline="", encoding="utf-8-sig") as s:
        w = csv.DictWriter(s, fieldnames=list(filas[0]))
        w.writeheader()
        w.writerows(filas)


if __name__ == "__main__":
    main()
