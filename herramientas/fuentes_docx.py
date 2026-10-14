#!/usr/bin/env python3
"""Prepara copias de los capítulos para el DOCX.

Cambia las pausas «* * *» por un párrafo con el estilo «Separador» y
genera un índice fijo (indice.md) con los títulos de cada archivo, para
que el manuscrito no dependa de que Word actualice un campo de tabla de
contenido. Con --paginas (líneas «título<TAB>página», de paginas_pdf.py)
el índice lleva además el número de página, para el PDF del manuscrito.

Uso: fuentes_docx.py DIR_SALIDA [--paginas paginas.tsv] archivo1.md ...
"""
import re
import sys
from pathlib import Path

TITULO = re.compile(r"^#\s+(.*?)\s*(\{[^}]*\})?\s*$")
SEPARADOR = '::: {custom-style="Separador"}\n\\*\u2003\\*\u2003\\*\n:::'


def main():
    salida = Path(sys.argv[1])
    salida.mkdir(parents=True, exist_ok=True)
    archivos, paginas = sys.argv[2:], {}
    if archivos[:1] == ["--paginas"]:
        for linea in Path(archivos[1]).read_text(encoding="utf-8").splitlines():
            titulo, pagina = linea.split("\t")
            paginas[titulo] = pagina
        archivos = archivos[2:]
    titulos = []
    for ruta in archivos:
        texto = Path(ruta).read_text(encoding="utf-8")
        for linea in texto.splitlines():
            m = TITULO.match(linea)
            if m:
                titulos.append(m.group(1))
                break
        texto = re.sub(r"(?m)^\* \* \*$", SEPARADOR, texto)
        (salida / Path(ruta).name).write_text(texto, encoding="utf-8")
    # El número de página va tras un tabulador con puntos guía (estilo «Indice»)
    tab = "`<w:r><w:tab/></w:r>`{=openxml}"
    numeros = [f"{tab}{paginas[t]}" if t in paginas else "" for t in titulos]
    # «1. Título» se escaparía como lista numerada: se protege el punto
    titulos = [re.sub(r"^(\d+)\.", r"\1\\.", t) for t in titulos]
    entradas = "\n\n".join(f'::: {{custom-style="Indice"}}\n{t}{n}\n:::' for t, n in zip(titulos, numeros))
    (salida / "indice.md").write_text("# Índice {.unnumbered}\n\n" + entradas + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
