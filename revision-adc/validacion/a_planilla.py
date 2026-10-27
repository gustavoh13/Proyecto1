#!/usr/bin/env python3
"""Pasa codificacion-texto-completo.jsonl a una planilla con el formato de planillas_validacion.py.

La planilla resultante tiene una fila por estudio de la muestra y por cada
reserva que se usó, con las mismas columnas que las planillas de los
codificadores, de modo que validacion.py contraste la lee como planilla de
consenso. Los estudios de la muestra sin texto llevan «Texto completo leído: No».

Uso: a_planilla.py 10-muestra-validacion.csv 11-textos-abiertos.csv codificacion-texto-completo.jsonl salida.xlsx
"""
import csv
import json
import sys
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Font

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from planillas_validacion import CATEGORIAS, DIMENSIONES, EVALUACION, columnas, hoja_codificacion  # noqa: E402

ABREV = {
    "niv": ["IP", "SEC", "UNI", "FD"], "dis": ["REV", "TEO", "CUAL", "CUAN", "INT"],
    "trad": ["FRE", "MUL", "MED", "CIU", "RGD"], "obj": ["IA", "DES", "RED", "ALG", "PRI", "ODI", "LEN", "PRO"],
}
CLAVES = [k for k in ABREV for _ in ABREV[k]]
SIGLAS = [s for k in ABREV for s in ABREV[k]]
DIM = dict(zip(["T", "I", "R"], DIMENSIONES))


def main():
    filas = list(csv.DictReader(open(sys.argv[1], encoding="utf-8-sig")))
    textos = {t["eid"]: t for t in csv.DictReader(open(sys.argv[2], encoding="utf-8-sig"))}
    cod = {x["eid"]: x for x in map(json.loads, open(sys.argv[3], encoding="utf-8"))}
    usados = [x for x in filas if x["papel"] == "muestra" or x["eid"] in cod]
    wb = Workbook()
    ws = wb.active
    ws.title = "Instrucciones"
    for i, linea in enumerate([
        "Codificación a texto completo de la muestra de validación.",
        "Codificador único: Claude (modelo de lenguaje de Anthropic), siguiendo manual-de-codificacion.md.",
        "No hay segundo codificador ni consenso: cada código lleva cita y página en la planilla para su auditoría.",
        "Filas: los 40 estudios de la muestra y las reservas que sustituyeron a los que no tenían texto abierto.",
    ], 1):
        ws.cell(i, 1, linea).font = Font(name="Arial", bold=i == 1)
    ws.column_dimensions["A"].width = 110
    hc = wb.create_sheet("Codificación")
    hoja_codificacion(hc, usados, textos)
    cols = columnas()
    papel = len(cols) + 1
    hc.cell(1, papel, "Papel").font = Font(name="Arial", bold=True)
    for i, x in enumerate(usados, 2):
        c = cod.get(x["eid"])
        valores = {"Texto completo leído": "Sí" if c else "No"}
        if c:
            valores["Elegible"] = "Sí" if c["elig"] else "No"
            valores["Notas"] = c.get("notas", "")
            if c["elig"]:
                for clave, sigla, categoria in zip(CLAVES, SIGLAS, CATEGORIAS):
                    valores[categoria] = "Sí" if sigla in c.get(clave, []) else "No"
                valores["Evaluación de resultados"] = EVALUACION[c["eval"]]
                for d, nombre in DIM.items():
                    cita = c.get("dim", {}).get(d)
                    valores[nombre] = "Sí" if cita else "No"
                    if cita:
                        valores[nombre.replace("dimensión: ", "Cita y página: ")] = f"«{cita[0]}» ({cita[1]})"
                valores["Otra tradición (cuál)"] = c.get("otra", "")
            else:
                valores["Motivo de exclusión"] = c["motivo"]
        for j, col in enumerate(cols, 1):
            if col in valores:
                hc.cell(i, j, valores[col]).font = Font(name="Arial")
        hc.cell(i, papel, x["papel"]).font = Font(name="Arial")
    wb.active = 1
    wb.save(sys.argv[4])
    print(f"{len(usados)} filas, {len(cod)} codificadas")


if __name__ == "__main__":
    main()
