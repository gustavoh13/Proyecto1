#!/usr/bin/env python3
"""Añade la codificación a texto completo de un estudio a codificacion-texto-completo.jsonl.

Lee un objeto JSON por la entrada estándar con claves abreviadas, comprueba que
los códigos existen y lo guarda (si el estudio ya estaba, lo sustituye). Las
abreviaturas corresponden a las categorías de 03-codificacion.csv:

  niv  IP Infantil y primaria · SEC Secundaria · UNI Universidad · FD Formación docente
  dis  REV Revisión · TEO Teórico o conceptual · CUAL Cualitativo · CUAN Cuantitativo · INT Diseño o intervención
  trad FRE Freire · MUL Multiliteracidades/NEL · MED Alfabetización mediática · CIU Ciudadanía digital
       RGD Raza, género y decolonialidad
  obj  IA · DES Desinformación · RED Redes sociales · ALG Algoritmos, datos y plataformas
       PRI Privacidad y vigilancia · ODI Odio y radicalización · LEN Lenguas extranjeras · PRO Producción del alumnado
  eval 0, 1, 2 o 3 (manual de codificación, variable 4)
  dim  {"T": ["cita", "p. N"], "I": [...], "R": [...]}: solo las dimensiones presentes

Uso: echo '{"eid": ..., "elig": true, ...}' | registrar.py
"""
import json
import sys
from pathlib import Path

ARCHIVO = Path(__file__).with_name("codificacion-texto-completo.jsonl")
VALIDOS = {
    "niv": {"IP", "SEC", "UNI", "FD"}, "dis": {"REV", "TEO", "CUAL", "CUAN", "INT"},
    "trad": {"FRE", "MUL", "MED", "CIU", "RGD"}, "obj": {"IA", "DES", "RED", "ALG", "PRI", "ODI", "LEN", "PRO"},
}


def main():
    x = json.load(sys.stdin)
    assert x["eid"].startswith("2-s2.0-"), x["eid"]
    if x.get("leido", True) and x["elig"]:
        for k, validos in VALIDOS.items():
            assert set(x.get(k, [])) <= validos, (k, x.get(k))
        assert x["eval"] in (0, 1, 2, 3)
        assert set(x.get("dim", {})) <= {"T", "I", "R"} and all(len(v) == 2 for v in x.get("dim", {}).values())
    elif x.get("leido", True):
        assert x.get("motivo"), "falta el motivo de exclusión"
    filas = [json.loads(l) for l in ARCHIVO.read_text(encoding="utf-8").splitlines()] if ARCHIVO.exists() else []
    filas = [f for f in filas if f["eid"] != x["eid"]] + [x]
    ARCHIVO.write_text("".join(json.dumps(f, ensure_ascii=False) + "\n" for f in filas), encoding="utf-8")
    print(f"{len(filas)} estudios codificados")


if __name__ == "__main__":
    main()
