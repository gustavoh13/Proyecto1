#!/usr/bin/env python3
"""Comprueba que una traducción conserva la estructura del original.

Compara el archivo original y su traducción: claves de las notas (llamadas
y definiciones), encabezados y sus atributos, pausas «* * *», comentarios
HTML, URL y número de párrafos. Avisa también de rayas (—) y de palabras
castellanas frecuentes que delatan restos sin traducir.

Uso: comparar_traduccion.py original.md traduccion.md
"""
import re
import sys
from collections import Counter
from pathlib import Path

URL = re.compile(r"https?://[^\s<>\]]+")
RESTOS = re.compile(r"\b(?:que también|pero|aunque|desde|hacia|entonces|nosotros|también|porque|cuando|sobre todo|escuela|alumnos|aprendizaje|según)\b", re.I)


def estructura(texto):
    return {
        "llamadas": Counter(re.findall(r"\[\^([^\]]+)\](?!:)", texto)),
        "definiciones": Counter(re.findall(r"^\[\^([^\]]+)\]:", texto, re.M)),
        "atributos": re.findall(r"^#+ .*?(\{[^}]*\})?\s*$", texto, re.M),
        "niveles": [len(m) for m in re.findall(r"^(#+) ", texto, re.M)],
        "pausas": len(re.findall(r"^\* \* \*$", texto, re.M)),
        "comentarios": re.findall(r"<!--.*?-->", texto, re.S),
        "url": Counter(u.rstrip(".,;)") for u in URL.findall(texto)),
        "parrafos": len([p for p in re.split(r"\n\s*\n", texto.strip()) if p.strip()]),
    }


def main():
    original = Path(sys.argv[1]).read_text(encoding="utf-8")
    traduccion = Path(sys.argv[2]).read_text(encoding="utf-8")
    a, b = estructura(original), estructura(traduccion)
    errores = [f"{k}: original {a[k]!r}\n   traducción {b[k]!r}" for k in a if a[k] != b[k]]
    rayas = traduccion.count("—")
    if rayas:
        errores.append(f"rayas (—): {rayas}")
    sospechosas = Counter(m.group(0).lower() for m in RESTOS.finditer(re.sub(r"^- .*$", "", traduccion, flags=re.M)))
    for e in errores:
        print("ERROR", e)
    if sospechosas:
        print("Revisar posibles restos en castellano:", dict(sospechosas))
    if not errores:
        print("Estructura idéntica:", Path(sys.argv[2]).name)
    sys.exit(1 if errores else 0)


if __name__ == "__main__":
    main()
