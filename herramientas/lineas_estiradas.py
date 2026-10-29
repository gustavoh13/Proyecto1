#!/usr/bin/env python3
"""Detecta en el PDF las líneas justificadas con huecos excesivos.

Para cada línea cuyo espacio medio entre palabras supera el 60 % de la
altura del texto, localiza la primera palabra de la línea siguiente,
que es la que no cupo y obligó a estirar la anterior. Imprime esa palabra
y el número de veces que ha aparecido antes en el libro, para que el
guionado afecte solo a esa aparición concreta.

Uso: lineas_estiradas.py libro.pdf   (salida: «palabra<TAB>n» por línea)
"""
import re
import statistics
import subprocess
import sys

UMBRAL = 0.6
LETRAS = re.compile(r"[A-Za-zÁÀÉÈÍÏÓÒÚÜÑÇáàéèíïóòúüñç]+")
PALABRA_PDF = re.compile(r'<word xMin="([\d.]+)" yMin="([\d.]+)" xMax="([\d.]+)" yMax="([\d.]+)">([^<]*)</word>')


def main():
    salida = subprocess.run(["pdftotext", "-bbox-layout", sys.argv[1], "-"],
                            capture_output=True, text=True, check=True).stdout
    # Líneas en orden de lectura, sin los números de página
    lineas = []
    for linea in re.findall(r"<line [^>]*>(.*?)</line>", salida, re.S):
        ws = PALABRA_PDF.findall(linea)
        if ws and not (len(ws) == 1 and ws[0][4].isdigit()):
            lineas.append(ws)
    # Texto corrido del libro, uniendo las palabras partidas por guion blando,
    # con la posición en que empieza cada línea
    texto, inicio_linea = [], []
    for ws in lineas:
        inicio_linea.append(sum(len(t) for t in texto))
        for w in ws:
            palabra = w[4]
            texto.append(palabra.rstrip("­") if palabra.endswith("­") else palabra + " ")
    corrido = "".join(texto).replace("­", "")
    # Las posiciones cambian al quitar los guiones blandos: se recalculan
    desfase = []
    acumulado = 0
    crudo = "".join(texto)
    for i, c in enumerate(crudo):
        desfase.append(acumulado)
        if c == "­":
            acumulado += 1
    resultados = []
    for i, ws in enumerate(lineas[:-1]):
        # Los separadores (* * *) no son texto justificado
        if len(ws) < 3 or not any(LETRAS.search(w[4]) for w in ws):
            continue
        huecos = [float(ws[k + 1][0]) - float(ws[k][2]) for k in range(len(ws) - 1)]
        alto = statistics.median(float(w[3]) - float(w[1]) for w in ws)
        if sum(huecos) / len(huecos) <= UMBRAL * alto:
            continue
        pos_crudo = inicio_linea[i + 1]
        pos = pos_crudo - (desfase[pos_crudo] if pos_crudo < len(desfase) else acumulado)
        # Primera tira de letras de cinco o más en la palabra que abre la línea
        for m in LETRAS.finditer(corrido, pos):
            if m.start() > pos + 40:
                break
            if len(m.group(0)) >= 5:
                palabra = m.group(0)
                previas = sum(1 for x in LETRAS.finditer(corrido, 0, m.start()) if x.group(0).lower() == palabra.lower())
                resultados.append(f"{palabra}\t{previas}")
                break
    if resultados:
        print("\n".join(resultados))


if __name__ == "__main__":
    main()
