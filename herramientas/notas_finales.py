#!/usr/bin/env python3
"""Convierte las notas al pie de cada capítulo en notas finales agrupadas.

Lee los capítulos en el orden recibido, numera las llamadas de cada capítulo
desde 1, las sustituye por un superíndice enlazado y escribe en el directorio
de salida una copia de cada capítulo sin definiciones más un archivo
«notas.md» con todas las notas agrupadas por capítulo.

Uso: notas_finales.py DIR_SALIDA [--titulo Notas] capitulo1.md capitulo2.md ...
"""
import re
import sys
from pathlib import Path

DEF = re.compile(r"^\[\^([^\]]+)\]:\s*(.*)$")
REF = re.compile(r"\[\^([^\]]+)\](?!:)")
TITULO = re.compile(r"^#\s+(.*?)\s*(\{[^}]*\})?\s*$")


def procesar(ruta, salida):
    lineas = Path(ruta).read_text(encoding="utf-8").splitlines()
    definiciones, cuerpo = {}, []
    for linea in lineas:
        m = DEF.match(linea)
        if m:
            definiciones[m.group(1)] = m.group(2)
        else:
            cuerpo.append(linea)
    texto = "\n".join(cuerpo).rstrip() + "\n"
    titulo = next((TITULO.match(l).group(1) for l in lineas if TITULO.match(l)), ruta)
    slug = Path(ruta).stem.split("-")[0]
    numeros, orden = {}, []

    def sustituir(m):
        clave = m.group(1)
        if clave not in definiciones:
            sys.exit(f"{ruta}: llamada sin definición [^{clave}]")
        if clave not in numeros:
            numeros[clave] = len(numeros) + 1
            orden.append(clave)
            ancla = f' {{#ref-{slug}-{numeros[clave]}}}'
        else:
            ancla = ""
        n = numeros[clave]
        if ancla:
            return f"^[[{n}](#nota-{slug}-{n})]{ancla.strip()}^"
        return f"^[{n}](#nota-{slug}-{n})^"

    texto = REF.sub(sustituir, texto)
    sobrantes = set(definiciones) - set(numeros)
    if sobrantes:
        sys.exit(f"{ruta}: notas definidas sin llamada: {sorted(sobrantes)}")
    (salida / Path(ruta).name).write_text(texto, encoding="utf-8")
    notas = [
        f"[[{numeros[c]}](#ref-{slug}-{numeros[c]})]{{#nota-{slug}-{numeros[c]}}}. {definiciones[c]}"
        for c in orden
    ]
    return titulo, notas


def main():
    salida = Path(sys.argv[1])
    salida.mkdir(parents=True, exist_ok=True)
    archivos, titulo_notas = sys.argv[2:], "Notas"
    if archivos[:1] == ["--titulo"]:
        titulo_notas, archivos = archivos[1], archivos[2:]
    bloques = []
    for ruta in archivos:
        titulo, notas = procesar(ruta, salida)
        if notas:
            bloques.append(f"## {titulo} {{.unnumbered}}\n\n" + "\n\n".join(notas))
    (salida / "notas.md").write_text(
        f"# {titulo_notas} {{.unnumbered #notas}}\n\n" + "\n\n".join(bloques) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
