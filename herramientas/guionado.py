#!/usr/bin/env python3
"""Añade puntos de partición (guiones blandos) a apariciones concretas de
palabras en el HTML del libro.

Chromium no trae diccionario de partición para el español, de modo que en
un texto justificado una palabra larga que no cabe al final de la línea
obliga a estirar la anterior. compilar.sh detecta esas líneas
(lineas_estiradas.py) y pasa aquí la palabra y el número de apariciones
previas; este script silabea con pyphen solo esa aparición, para que el
resto del texto del PDF se pueda copiar y buscar sin caracteres invisibles.
Las palabras se cuentan sobre el texto visible, como en el PDF, y nunca se
parte el texto de una URL.

Uso: guionado.py archivo.html objetivos.tsv
     (objetivos.tsv: «palabra<TAB>n» por línea; se acumula entre pasadas)
"""
import re
import sys
from pathlib import Path

LETRAS = re.compile(r"[A-Za-zÁÉÍÓÚÜÑáéíóúüñ]+")
PIEZAS = re.compile(r"<(style|script|title)\b.*?</\1>|<!--.*?-->|<[^>]+>", re.S | re.I)
EN_LINEA = {"a", "span", "em", "strong", "i", "b", "sup", "sub", "wbr", "code", "small", "cite", "q", "abbr", "mark", "u", "s"}


def main():
    html_ruta, objetivos_ruta = Path(sys.argv[1]), Path(sys.argv[2])
    objetivos = set()
    if objetivos_ruta.exists():
        for linea in objetivos_ruta.read_text(encoding="utf-8").splitlines():
            if "\t" in linea:
                palabra, n = linea.split("\t")
                objetivos.add((palabra.lower(), int(n)))
    if not objetivos:
        return
    try:
        import pyphen
    except ImportError:
        print("Aviso: pyphen no está instalado; el PDF se genera sin partición (pip install pyphen).")
        return
    dic = pyphen.Pyphen(lang="es")
    html = Path(html_ruta).read_text(encoding="utf-8")
    inicio = html.find("<body")
    # Texto visible: las etiquetas en línea no separan palabras; las de bloque, sí.
    # Cada tramo de texto guarda su posición en el HTML y si está dentro de una URL.
    visible, tramos, pos, en_url = [], [], inicio, False
    for m in PIEZAS.finditer(html, inicio):
        if m.start() > pos:
            tramos.append((sum(map(len, visible)), pos, m.start(), en_url))
            visible.append(html[pos:m.start()])
        etiqueta = re.match(r"</?([a-zA-Z0-9]+)", m.group(0))
        nombre = etiqueta.group(1).lower() if etiqueta else ""
        if nombre == "a":
            en_url = not m.group(0).startswith("</") and 'class="uri"' in m.group(0)
        if nombre not in EN_LINEA:
            visible.append("\n")
        pos = m.end()
    texto = "".join(visible)
    palabras = {p for p, _ in objetivos}
    cuentas, cambios = {}, []
    for m in LETRAS.finditer(texto):
        clave = m.group(0).lower()
        if clave not in palabras:
            continue
        n = cuentas.get(clave, 0)
        cuentas[clave] = n + 1
        if (clave, n) not in objetivos:
            continue
        tramo = next((t for t in tramos if t[0] <= m.start() and m.end() <= t[0] + t[2] - t[1]), None)
        if tramo and not tramo[3]:
            a = tramo[1] + m.start() - tramo[0]
            cambios.append((a, a + len(m.group(0)), dic.inserted(m.group(0), hyphen="­")))
    for a, b, nuevo in sorted(cambios, reverse=True):
        html = html[:a] + nuevo + html[b:]
    html_ruta.write_text(html, encoding="utf-8")


if __name__ == "__main__":
    main()
