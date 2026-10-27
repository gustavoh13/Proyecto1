#!/usr/bin/env python3
"""Genera en APA 7 las referencias de los estudios del corpus citados en el artículo.

Scopus solo entrega el primer autor; el resto se marca como «[+N co-authors]»
para completarlo a mano. Los títulos se pasan a mayúscula de oración y los
nombres de revista se normalizan con la grafía de cada revista.

Uso: referencias.py 04-metadatos.csv citados.txt > 08-referencias.md
     (citados.txt: «apellido<TAB>año» por línea, como figuran en 04-metadatos.csv)
"""
import csv
import re
import sys

# Palabras que conservan la mayúscula dentro de un título
PROPIOS = {
    "english", "spanish", "catalan", "chinese", "saudi", "arab", "iranian", "indonesian", "australia",
    "australian", "global", "south", "freire", "twitter", "instagram", "whatsapp", "snapchat", "vine",
    "wikipedia", "latinx", "chicanx", "district", "six", "trump", "peru", "colombian", "korean", "korea",
    "thai", "scientix", "ambassadors", "black", "u.s.", "u.k.", "europe", "european", "latin", "america",
    "american", "tiktok", "chatgpt", "genai", "gpt", "digcomp", "digcompedu", "parkland",
}
SIGLAS = {"ai", "cdl", "efl", "elt", "coil", "l2", "esl", "eap", "dei", "cdls", "ict", "he", "k-12", "3wai", "ii"}
REVISTAS = {
    "Journal of Adolescent and Adult Literacy": "Journal of Adolescent & Adult Literacy",
    "Recall": "ReCALL", "Triplec": "tripleC: Communication, Capitalism & Critique",
    "International Journal of Tesol Studies": "International Journal of TESOL Studies",
    "Learning Media and Technology": "Learning, Media and Technology",
    "E Learning and Digital Media": "E-Learning and Digital Media",
    "Knowledge Management and E Learning": "Knowledge Management & E-Learning",
    "English Teaching": "English Teaching: Practice & Critique",
    "Revista Complutense De Educacion": "Revista Complutense de Educación",
    "Journal of E Learning and Knowledge Society": "Journal of e-Learning and Knowledge Society",
    "Language Learning and Technology": "Language Learning & Technology",
    "Digital Education Review": "Digital Education Review", "Edutec": "Edutec",
    "Tesol Quarterly": "TESOL Quarterly",
    "International Journal of Applied Linguistics United Kingdom": "International Journal of Applied Linguistics",
    "Equity and Excellence in Education": "Equity & Excellence in Education",
    "Revista Fuentes": "Revista Fuentes", "Interciencia": "Interciencia",
    "Lengua Y Sociedad": "Lengua y Sociedad", "Cultura Y Educacion": "Cultura y Educación",
    "Sustainability Switzerland": "Sustainability", "Information Switzerland": "Information",
}
# Revistas que numeran solo por número, sin volumen
SOLO_NUMERO = {"Edutec", "Digital Education Review"}
# Títulos que la conversión automática no resuelve (nombres de escalas, campañas, siglas)
TITULOS = {
    "comprehensive digital literacy scale (CDLS)": "Comprehensive Digital Literacy Scale (CDLS)",
    "critical 3wAI literacy scale": "Critical 3wAI Literacy Scale",
    "chicanx/latinx": "Chicanx/Latinx",
    "U.s. Adolescents": "U.S. adolescents",
    "(in real life)": "(in real life)", " irl ": " IRL ",
    "Sifting through": "SIFTing through",
    "The one shot is enough poster campaign": "The One Shot is Enough poster campaign",
    " (la alfabetización crítica digital del futuro profesorado en tiempos de Twitter)": "",
}
# Correcciones de apellidos que Scopus separa mal
APELLIDOS = {("Urízar", "2026"): ("Herrera Urízar", "G."), ("G. Stewart", "2021"): ("Stewart", "O. G.")}


def palabra(p, inicio, todo_mayus):
    partes = p.split("-")
    salida = []
    for i, w in enumerate(partes):
        limpio = re.sub(r"^[\"“‘(#]+|[\"”’),.;:?!]+$", "", w)
        bajo = limpio.lower()
        if bajo in SIGLAS:
            nuevo = limpio.upper() if bajo not in ("l2", "k-12", "3wai") else {"l2": "L2", "3wai": "3wAI"}.get(bajo, limpio)
        elif bajo in PROPIOS:
            nuevo = {"u.s.": "U.S.", "u.k.": "U.K.", "chatgpt": "ChatGPT", "genai": "GenAI", "gpt": "GPT",
                     "tiktok": "TikTok", "digcomp": "DigComp", "digcompedu": "DigCompEdu",
                     "whatsapp": "WhatsApp"}.get(bajo, limpio[:1].upper() + limpio[1:].lower())
        elif not todo_mayus and re.search(r"[a-z][A-Z]", limpio):
            nuevo = limpio
        elif inicio and i == 0:
            nuevo = limpio[:1].upper() + limpio[1:].lower()
        else:
            nuevo = limpio.lower()
        salida.append(w.replace(limpio, nuevo, 1) if limpio else w)
    return "-".join(salida)


def oracion(titulo):
    todo_mayus = titulo.upper() == titulo
    t = re.sub(r"\s+", " ", titulo.strip())
    palabras, salida, inicio = t.split(" "), [], True
    for p in palabras:
        salida.append(palabra(p, inicio, todo_mayus))
        inicio = p.endswith((":", "?", "."))
    return " ".join(salida)


def iniciales(s):
    return " ".join(f"{c}." for c in re.findall(r"[A-ZÁÉÍÓÚÑÄÖÜ]", s)) or s


def main():
    meta = list(csv.DictReader(open(sys.argv[1], encoding="utf-8-sig")))
    citados = [l.rstrip("\n").split("\t") for l in open(sys.argv[2], encoding="utf-8") if l.strip()]
    salida = []
    for apellido, anio, *pista in citados:
        c = [m for m in meta if m["apellido"] == apellido and m["anio"] == anio
             and (not pista or pista[0].lower() in m["titulo"].lower())]
        if len(c) != 1:
            sys.exit(f"{apellido} {anio}: {len(c)} coincidencias")
        m = c[0]
        ap, ini = APELLIDOS.get((apellido, anio), (m["apellido"], iniciales(m["iniciales"])))
        n = int(m["n_autores"] or 1)
        if n == 1:
            autores = f"{ap}, {ini}"
        elif n == 2:
            autores = f"{ap}, {ini}, & [co-author]."
        else:
            autores = f"{ap}, {ini}, [+{n - 1} co-authors]."
        revista = REVISTAS.get(m["revista"], m["revista"])
        inicio_num = re.match(r"\d+(-\d+)?", m["numero"] or "")
        num = inicio_num.group(0).replace("-", "–") if inicio_num else ""
        vol = re.match(r"\d+", m["volumen"] or "")
        if revista in SOLO_NUMERO:
            # El número de Edutec y DER va en el DOI cuando Scopus lo registra como volumen
            enlace = re.search(r"\.(\d+)\.[\d-]+$", m["doi"])
            loc = f", ({enlace.group(1) if enlace else (vol.group(0) if vol else num)})"
        else:
            loc = (f", *{vol.group(0)}*" if vol else "") + (f"({num})" if num and vol else "")
            if vol and not num and re.search(r"\((\d+)", m["volumen"]):
                loc += f"({re.search(r'\((\d+)', m['volumen']).group(1)})"
        pag = (m["paginas"] or m["articulo"]).replace("-", "–")
        if pag:
            loc += f", {pag}"
        doi = f" https://doi.org/{m['doi']}" if m["doi"] else ""
        titulo = oracion(m["titulo"]).rstrip(".")
        for a, b in TITULOS.items():
            titulo = titulo.replace(a, b)
        fin = "" if titulo.endswith(("?", "!")) else "."
        salida.append((ap.lower().replace("ö", "o").replace("ü", "u"),
                       f"{autores} ({anio}). {titulo}{fin} *{revista}*{loc}.{doi}"))
    for _, s in sorted(salida):
        print(s + "\n")


if __name__ == "__main__":
    main()
