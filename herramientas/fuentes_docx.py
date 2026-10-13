#!/usr/bin/env python3
"""Prepara copias de los capítulos para el DOCX.

Cambia las pausas «* * *» por un párrafo con el estilo «Separador» y
genera un índice fijo (indice.md) con los títulos de cada archivo, para
que el manuscrito no dependa de que Word actualice un campo de tabla de
contenido.

Uso: fuentes_docx.py DIR_SALIDA archivo1.md archivo2.md ...
"""
import re
import sys
from pathlib import Path

TITULO = re.compile(r"^#\s+(.*?)\s*(\{[^}]*\})?\s*$")
SEPARADOR = '::: {custom-style="Separador"}\n\\*\u2003\\*\u2003\\*\n:::'


def main():
    salida = Path(sys.argv[1])
    salida.mkdir(parents=True, exist_ok=True)
    titulos = []
    for ruta in sys.argv[2:]:
        texto = Path(ruta).read_text(encoding="utf-8")
        for linea in texto.splitlines():
            m = TITULO.match(linea)
            if m:
                titulos.append(m.group(1))
                break
        texto = re.sub(r"(?m)^\* \* \*$", SEPARADOR, texto)
        (salida / Path(ruta).name).write_text(texto, encoding="utf-8")
    # «1. Título» se escaparía como lista numerada: se protege el punto
    titulos = [re.sub(r"^(\d+)\.", r"\1\\.", t) for t in titulos]
    entradas = "\n\n".join(f'::: {{custom-style="Indice"}}\n{t}\n:::' for t in titulos)
    (salida / "indice.md").write_text("# Índice {.unnumbered}\n\n" + entradas + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
