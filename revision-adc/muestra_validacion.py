#!/usr/bin/env python3
"""Sortea la muestra de estudios que se leen a texto completo para validar la codificación.

Solo entran los estudios en acceso abierto (no hay acceso institucional a los
demás). La muestra se reparte entre los tres periodos en proporción al corpus
completo, no al conjunto abierto, que está muy cargado hacia 2024-2026; si un
periodo no tiene bastantes estudios abiertos, entran todos y el resto se
completa con el periodo más reciente. Dentro de cada periodo el orden es
aleatorio con semilla fija: los primeros forman la muestra y los siguientes son
reservas, por si un texto no se puede obtener o no es un texto de investigación.

Uso: muestra_validacion.py 03-codificacion.csv 10-muestra-validacion.csv [N]
"""
import csv
import random
import sys

SEMILLA = 20261027
PERIODOS = [("2016–2019", 2016, 2019), ("2020–2023", 2020, 2023), ("2024–2026", 2024, 2026)]


def periodo(anio):
    return next(p for p, a, b in PERIODOS if a <= int(anio) <= b)


def main():
    cod = list(csv.DictReader(open(sys.argv[1], encoding="utf-8-sig")))
    n = int(sys.argv[3]) if len(sys.argv) > 3 else 40
    abiertos = {p: sorted((x for x in cod if x["acceso_abierto"] == "True" and periodo(x["anio"]) == p),
                          key=lambda x: x["eid"]) for p, _, _ in PERIODOS}
    azar = random.Random(SEMILLA)
    for p in abiertos:
        azar.shuffle(abiertos[p])
    # Cupo proporcional al corpus completo, limitado por los estudios abiertos de cada periodo
    cupo = {p: min(len(abiertos[p]), round(n * sum(periodo(x["anio"]) == p for x in cod) / len(cod)))
            for p in abiertos}
    cupo[PERIODOS[-1][0]] += n - sum(cupo.values())
    filas = []
    for p, _, _ in PERIODOS:
        for orden, x in enumerate(abiertos[p], 1):
            filas.append({"periodo": p, "orden": orden, "papel": "muestra" if orden <= cupo[p] else "reserva",
                          "eid": x["eid"], "doi": x["doi"], "anio": x["anio"], "primer_autor": x["primer_autor"],
                          "titulo": x["titulo"], "revista": x["revista"], "idioma": x["idioma"]})
    with open(sys.argv[2], "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=list(filas[0]))
        w.writeheader()
        w.writerows(filas)
    for p, _, _ in PERIODOS:
        print(f"{p}: {cupo[p]} de {len(abiertos[p])} abiertos", file=sys.stderr)


if __name__ == "__main__":
    main()
