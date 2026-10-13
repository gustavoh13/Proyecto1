#!/usr/bin/env python3
"""Corrige la posición de los destinos internos del PDF que genera Chromium.

Chromium calcula los destinos con nombre (llamadas de nota, retornos e
índice) sin contar los márgenes de la página, de modo que al pulsar una
llamada el visor se sitúa unas líneas por encima de la nota. Además, si
una llamada abre página, deja su destino en el borde inferior de la página
anterior. Este script lee los márgenes de @page en la hoja de estilos y
recoloca cada destino en su sitio.

Uso: destinos_pdf.py libro.pdf estilos/libro.css
"""
import re
import sys

MM = 72 / 25.4


def margenes(css):
    bloque = re.search(r"@page\s*\{[^}]*?margin:\s*([^;]+);", open(css, encoding="utf-8").read())
    v = [float(x) * MM for x in re.findall(r"([\d.]+)mm", bloque.group(1))]
    # Notación abreviada de CSS: 1, 2, 3 o 4 valores
    arriba = v[0]
    derecha = v[1] if len(v) > 1 else v[0]
    abajo = v[2] if len(v) > 2 else v[0]
    izquierda = v[3] if len(v) > 3 else derecha
    return arriba, abajo, izquierda


def main():
    ruta, css = sys.argv[1], sys.argv[2]
    try:
        from pypdf import PdfWriter
        from pypdf.generic import FloatObject
    except ImportError:
        print("Aviso: pypdf no está instalado; los enlaces de las notas quedan algo desplazados (pip install pypdf).")
        return
    arriba, abajo, izquierda = margenes(css)
    pdf = PdfWriter(clone_from=ruta)
    paginas = [p.indirect_reference for p in pdf.pages]
    destinos = pdf.root_object["/Dests"].get_object()
    for nombre in destinos:
        d = destinos[nombre]
        if len(d) < 4 or d[1] != "/XYZ":
            continue
        pagina = d[0].get_object()
        alto = float(pagina.mediabox.top)
        x, y = float(d[2] or 0) + izquierda, float(d[3] or 0) - arriba
        n = paginas.index(d[0]) if d[0] in paginas else -1
        if y < abajo + 2 and 0 <= n < len(paginas) - 1:
            # Destino en el borde inferior: el elemento empieza en la página siguiente
            d[0] = paginas[n + 1]
            y = alto - arriba
        d[2] = FloatObject(x)
        d[3] = FloatObject(max(y, 0))
    pdf.write(ruta)


if __name__ == "__main__":
    main()
