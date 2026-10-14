#!/usr/bin/env python3
"""Localiza en el PDF del manuscrito la página donde empieza cada capítulo.

Cada capítulo abre página, así que basta con buscar la primera página
(después del índice) cuya primera línea es el título. Imprime
«título<TAB>página» para fuentes_docx.py --paginas.

Uso: paginas_pdf.py manuscrito.pdf archivo1.md archivo2.md ...
"""
import re
import subprocess
import sys
from pathlib import Path

from fuentes_docx import TITULO


def main():
    pdf = sys.argv[1]
    titulos = []
    for ruta in sys.argv[2:]:
        for linea in Path(ruta).read_text(encoding="utf-8").splitlines():
            m = TITULO.match(linea)
            if m:
                titulos.append(m.group(1))
                break
    texto = subprocess.run(["pdftotext", "-layout", pdf, "-"], capture_output=True, text=True, check=True).stdout
    paginas = texto.split("\f")
    primeras = [next((l.strip() for l in p.splitlines() if l.strip()), "") for p in paginas]
    desde = 2  # portada e índice
    for titulo in titulos:
        n = next((i for i in range(desde, len(primeras)) if re.sub(r"\s+", " ", primeras[i]) == titulo), None)
        if n is None:
            sys.exit(f"No encuentro «{titulo}» en {pdf}")
        print(f"{titulo}\t{n + 1}")
        desde = n + 1


if __name__ == "__main__":
    main()
