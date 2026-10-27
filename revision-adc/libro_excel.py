#!/usr/bin/env python3
"""Genera el libro de Excel del artículo: figuras como gráficos nativos editables,
tablas con fórmulas y los materiales suplementarios S1 (estudios incluidos) y
S2 (cribado de los 469 registros).

Los datos salen de 03-codificacion.csv, 04-metadatos.csv, 06-seleccion-final.csv
y 07-analisis.json, de modo que el libro se regenera si cambian.

Uso: libro_excel.py DIR_DATOS salida.xlsx
"""
import csv
import json
import sys
from pathlib import Path

from openpyxl import Workbook
from openpyxl.chart import BarChart, LineChart, Reference
from openpyxl.chart.label import DataLabelList
from openpyxl.comments import Comment
from openpyxl.formatting.rule import ColorScaleRule
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

FUENTE = "Arial"
NEGRITA = Font(name=FUENTE, bold=True)
NORMAL = Font(name=FUENTE)
ENTRADA = Font(name=FUENTE, color="0000FF")  # valores introducidos a mano
TITULO = Font(name=FUENTE, bold=True, size=13)
NOTA = Font(name=FUENTE, italic=True, size=9, color="595959")
CABECERA = PatternFill("solid", fgColor="E7E6E6")
LINEA = Border(bottom=Side(style="thin", color="A6A6A6"))
PERIODOS = ["2016–2019", "2020–2023", "2024–2026"]
TOTALES = [18, 35, 82]

ETIQUETAS = {
    "nivel: Infantil y primaria": "Early childhood and primary", "nivel: Secundaria": "Secondary",
    "nivel: Universidad": "Higher education", "nivel: Formación docente": "Teacher education",
    "diseño: Cualitativo": "Qualitative", "diseño: Cuantitativo": "Quantitative",
    "diseño: Teórico o conceptual": "Conceptual or theoretical",
    "diseño: Diseño o intervención": "Intervention or designed teaching",
    "diseño: Revisión de literatura": "Literature review",
    "marco: Alfabetización mediática": "Media literacy and educommunication",
    "marco: Multiliteracidades y nuevos estudios de literacidad": "Multiliteracies and New Literacy Studies",
    "marco: Ciudadanía digital": "Digital citizenship",
    "marco: Perspectivas críticas de raza, género y decolonialidad": "Race, gender and decolonial perspectives",
    "marco: Pedagogía crítica (Freire)": "Critical pedagogy (Freirean)",
    "tema: Inteligencia artificial": "Artificial intelligence",
    "tema: Algoritmos, datos y plataformas": "Algorithms, data and platforms",
    "tema: Redes sociales": "Social media", "tema: Desinformación y posverdad": "Disinformation and post-truth",
    "tema: Privacidad y vigilancia": "Privacy and surveillance",
    "tema: Discurso de odio y radicalización": "Hate speech and radicalisation",
    "tema: Lenguas extranjeras": "Second or foreign language education",
    "tema: Producción digital del alumnado": "Student media production",
    "idioma: español": "Spanish",
}


def cabecera(ws, fila, valores):
    for j, v in enumerate(valores, 1):
        c = ws.cell(fila, j, v)
        c.font, c.fill, c.border = NEGRITA, CABECERA, LINEA
        c.alignment = Alignment(wrap_text=True, vertical="center")


def titulo(ws, texto, nota=None):
    ws["A1"] = texto
    ws["A1"].font = TITULO
    if nota:
        ws["A2"] = nota
        ws["A2"].font = NOTA


def anchos(ws, anchos_col):
    for j, a in enumerate(anchos_col, 1):
        ws.column_dimensions[get_column_letter(j)].width = a


def tabla_periodos(ws, fila, analisis, claves, seccion=None, tendencia=True):
    """Filas n por periodo con % calculados por fórmula. Devuelve la siguiente fila libre."""
    if seccion:
        ws.cell(fila, 1, seccion).font = NEGRITA
        fila += 1
    for k in claves:
        v = analisis["categorias"][k]
        ws.cell(fila, 1, ETIQUETAS[k]).font = NORMAL
        for j, x in enumerate(v["x"]):
            ws.cell(fila, 2 + 2 * j, x).font = NORMAL
            c = ws.cell(fila, 3 + 2 * j, f"={get_column_letter(2 + 2 * j)}{fila}/{get_column_letter(2 + 2 * j)}$4")
            c.number_format, c.font = "0.0%", NORMAL
        ws.cell(fila, 8, f"=B{fila}+D{fila}+F{fila}").font = NORMAL
        c = ws.cell(fila, 9, f"=H{fila}/H$4")
        c.number_format, c.font = "0.0%", NORMAL
        if tendencia:
            for col, val, fmt in ((10, v["z"], "0.00"), (11, v["p"], "0.000")):
                c = ws.cell(fila, col, round(val, 4))
                c.number_format, c.font = fmt, ENTRADA
        fila += 1
    return fila


def cabecera_periodos(ws, fila=3):
    cabecera(ws, fila, ["Category", "2016–2019 n", "%", "2020–2023 n", "%", "2024–2026 n", "%",
                        "Total n", "%", "Trend z", "p"])
    ws.cell(fila + 1, 1, "Studies in period (n)").font = NEGRITA
    for j, t in enumerate(TOTALES):
        c = ws.cell(fila + 1, 2 + 2 * j, t)
        c.font = ENTRADA
    ws.cell(fila + 1, 8, f"=B{fila + 1}+D{fila + 1}+F{fila + 1}").font = NEGRITA
    return fila + 2


def main():
    d = Path(sys.argv[1])
    analisis = json.load(open(d / "07-analisis.json", encoding="utf-8"))
    cod = list(csv.DictReader(open(d / "03-codificacion.csv", encoding="utf-8-sig")))
    meta = {m["eid"]: m for m in csv.DictReader(open(d / "04-metadatos.csv", encoding="utf-8-sig"))}
    sel = list(csv.DictReader(open(d / "06-seleccion-final.csv", encoding="utf-8-sig")))
    wb = Workbook()

    # Guía
    ws = wb.active
    ws.title = "README"
    titulo(ws, "Critical digital literacy in formal education, 2016–2026: figures, tables and supplementary data")
    filas = [
        ("Source", "Scopus, search of 27 October 2026; 469 records, 135 included studies. Generated by revision-adc/libro_excel.py."),
        ("Charts", "Fig2 to Fig5 hold native Excel charts. Edit the numbers in the sheet and the chart updates; edit titles, colours and axes as usual."),
        ("Colours", "Blue numbers are typed inputs (counts, test statistics computed in analisis.py). Black numbers are formulas."),
        ("Tables", "Table1 to Table7 reproduce the tables of the manuscript. Percentages are formulas over the counts."),
        ("S1_Included", "Supplementary file S1: the 135 included studies with bibliographic data and codes (1 = code present)."),
        ("S2_Screening", "The 469 records with both screening passes, the indicators and the final decision."),
        ("Placeholders", "Scopus returned only the first author of each study; co-authors still need to be completed."),
    ]
    for i, (a, b) in enumerate(filas, 3):
        ws.cell(i, 1, a).font = NEGRITA
        ws.cell(i, 2, b).font = NORMAL
        ws.cell(i, 2).alignment = Alignment(wrap_text=True)
    anchos(ws, [16, 110])

    # Figura 1: flujo
    ws = wb.create_sheet("Fig1_Flow")
    titulo(ws, "Figure 1. Two-pass selection of studies", "Counts in the flow diagram. Totals are formulas.")
    cabecera(ws, 3, ["Stage", "Records"])
    pasos = [("Records identified in Scopus", 469), ("Duplicates removed", 0),
             ("Pass 1 (titles): included", 129), ("Pass 1 (titles): excluded", 340),
             ("Pass 2 (abstracts and keywords): included", 135), ("Pass 2 (abstracts and keywords): excluded", 334),
             ("Agreement: both include", 85), ("Agreement: both exclude", 290),
             ("Disagreement: included, title names CDL", 22), ("Disagreement: included, two indicators", 28),
             ("Disagreement: excluded, insufficient evidence", 38), ("Disagreement: excluded, context or type", 6),
             ("Excluded: CDL not the focus", 320), ("Excluded: outside formal education", 12),
             ("Excluded: book reviews", 2),
             ("Second reviewer: disputed records read", 94), ("Second reviewer: agreed records sampled (20%)", 75),
             ("Second reviewer: decisions confirmed", 169)]
    for i, (a, b) in enumerate(pasos, 4):
        ws.cell(i, 1, a).font = NORMAL
        ws.cell(i, 2, b).font = ENTRADA
    f = 4 + len(pasos)
    ws.cell(f, 1, "Studies included").font = NEGRITA
    ws.cell(f, 2, "=B10+B12+B13").font = NEGRITA
    ws.cell(f + 1, 1, "Records excluded").font = NEGRITA
    ws.cell(f + 1, 2, "=B16+B17+B18").font = NEGRITA
    ws.cell(f + 2, 1, "Agreement between passes").font = NORMAL
    c = ws.cell(f + 2, 2, "=(B10+B11)/B4")
    c.number_format, c.font = "0.0%", NORMAL
    ws.cell(f + 3, 1, "Cohen's kappa").font = NORMAL
    c = ws.cell(f + 3, 2, "=((B10+B11)/B4-((B6*B8+B7*B9)/B4^2))/(1-(B6*B8+B7*B9)/B4^2)")
    c.number_format, c.font = "0.00", NORMAL
    ws.cell(f + 4, 1, "Second reviewer: agreement with final decisions").font = NORMAL
    c = ws.cell(f + 4, 2, "=B21/(B19+B20)")
    c.number_format, c.font = "0.0%", NORMAL
    anchos(ws, [48, 12])

    # Figura 2: producción anual
    ws = wb.create_sheet("Fig2_Annual")
    titulo(ws, "Figure 2. Included studies per year by language, with the Poisson trend for 2016–2025",
           "Fitted values are formulas on the two model parameters (cells F4 and F5), estimated in analisis.py. 2026 covers 1 January to 27 October.")
    cabecera(ws, 3, ["Year", "English", "Spanish", "Total", "Poisson trend"])
    ws["E3"].value = "Poisson trend"
    ws["G3"], ws["G4"], ws["G5"] = "Parameter", "Intercept (a)", "Slope per year (b)"
    ws["F3"] = "Value"
    ws["F3"].font = ws["G3"].font = NEGRITA
    ws["F4"], ws["F5"] = 1.13028609, 0.18771235
    ws["F4"].font = ws["F5"].font = ENTRADA
    ws["G6"], ws["F6"] = "Annual growth", "=EXP(F5)-1"
    ws["F6"].number_format = "0.0%"
    conteo = {}
    for (anio, idioma), n in [(tuple(k), v) for k, v in analisis["por_anio"]]:
        conteo.setdefault(anio, {})[idioma] = n
    for i, anio in enumerate(range(2016, 2027), 4):
        ws.cell(i, 1, str(anio)).font = NORMAL
        ws.cell(i, 2, conteo.get(str(anio), {}).get("inglés", 0)).font = ENTRADA
        ws.cell(i, 3, conteo.get(str(anio), {}).get("español", 0)).font = ENTRADA
        ws.cell(i, 4, f"=B{i}+C{i}").font = NORMAL
        if anio <= 2025:
            c = ws.cell(i, 5, f"=EXP($F$4+$F$5*({anio}-2016))")
            c.number_format, c.font = "0.0", NORMAL
    ws.cell(15, 1, "Total").font = NEGRITA
    for col in "BCD":
        ws[f"{col}15"] = f"=SUM({col}4:{col}14)"
        ws[f"{col}15"].font = NEGRITA
    barras = BarChart()
    barras.type, barras.grouping, barras.overlap = "col", "stacked", 100
    barras.title = "Included studies per year by language"
    barras.y_axis.title, barras.x_axis.title = "Studies", "Year"
    barras.add_data(Reference(ws, min_col=2, max_col=3, min_row=3, max_row=14), titles_from_data=True)
    barras.set_categories(Reference(ws, min_col=1, min_row=4, max_row=14))
    barras.series[0].graphicalProperties.solidFill = "BFBFBF"
    barras.series[1].graphicalProperties.solidFill = "2F75B5"
    linea = LineChart()
    linea.add_data(Reference(ws, min_col=5, min_row=3, max_row=14), titles_from_data=True)
    linea.series[0].graphicalProperties.line.dashStyle = "dash"
    linea.series[0].graphicalProperties.line.solidFill = "595959"
    linea.series[0].smooth = False
    linea.y_axis.axId = 100
    barras += linea
    barras.height, barras.width = 9, 18
    ws.add_chart(barras, "I8")
    anchos(ws, [8, 10, 10, 10, 14, 12, 20])

    # Figura 3: países y regiones
    ws = wb.create_sheet("Fig3_Countries")
    titulo(ws, "Figure 3. Countries and regions of author affiliation",
           "A study counts once for each country and region of its authors.")
    cabecera(ws, 3, ["Country", "Studies"])
    for i, (p, n) in enumerate(analisis["paises"], 4):
        ws.cell(i, 1, p).font = NORMAL
        ws.cell(i, 2, n).font = ENTRADA
    ultimo = 3 + len(analisis["paises"])
    regiones = [("Europe", 48), ("North America", 40), ("Asia", 33), ("Latin America", 7), ("Oceania", 5), ("Africa", 2)]
    cabecera(ws, 3, ["Country", "Studies", "", "Region", "Studies"])
    ws["C3"].fill = PatternFill()
    for i, (r, n) in enumerate(regiones, 4):
        ws.cell(i, 4, r).font = NORMAL
        ws.cell(i, 5, n).font = ENTRADA
    graf = BarChart()
    graf.type, graf.title = "bar", "Studies by country (top 12)"
    graf.add_data(Reference(ws, min_col=2, min_row=3, max_row=15), titles_from_data=True)
    graf.set_categories(Reference(ws, min_col=1, min_row=4, max_row=15))
    graf.y_axis.title = "Studies"
    graf.x_axis.scaling.orientation = "maxMin"
    graf.legend = None
    graf.series[0].graphicalProperties.solidFill = "2F75B5"
    graf.height, graf.width = 9, 14
    ws.add_chart(graf, "G3")
    graf2 = BarChart()
    graf2.type, graf2.title = "bar", "Studies by region"
    graf2.add_data(Reference(ws, min_col=5, min_row=3, max_row=9), titles_from_data=True)
    graf2.set_categories(Reference(ws, min_col=4, min_row=4, max_row=9))
    graf2.x_axis.scaling.orientation = "maxMin"
    graf2.legend = None
    graf2.series[0].graphicalProperties.solidFill = "A6A6A6"
    graf2.height, graf2.width = 7, 14
    ws.add_chart(graf2, "G23")
    ws.cell(ultimo + 1, 1, "Countries").font = NEGRITA
    ws.cell(ultimo + 1, 2, f"=COUNTA(A4:A{ultimo})").font = NEGRITA
    anchos(ws, [26, 10, 3, 18, 10])

    # Figura 4: objetos por periodo
    ws = wb.create_sheet("Fig4_Objects")
    titulo(ws, "Figure 4. Objects of critique by period (% of the studies in each period)",
           "Counts are inputs; percentages are formulas. Broad dictionaries (Appendix A3).")
    objetos = ["tema: Inteligencia artificial", "tema: Algoritmos, datos y plataformas", "tema: Redes sociales",
               "tema: Desinformación y posverdad"]
    cabecera(ws, 3, ["Period", "Studies"] + [ETIQUETAS[o] + " n" for o in objetos] + [ETIQUETAS[o] + " %" for o in objetos])
    for i, p in enumerate(PERIODOS, 4):
        ws.cell(i, 1, p).font = NORMAL
        ws.cell(i, 2, TOTALES[i - 4]).font = ENTRADA
        for j, o in enumerate(objetos):
            ws.cell(i, 3 + j, analisis["categorias"][o]["x"][i - 4]).font = ENTRADA
            c = ws.cell(i, 7 + j, f"={get_column_letter(3 + j)}{i}/$B{i}")
            c.number_format, c.font = "0.0%", NORMAL
    graf = LineChart()
    graf.title = "Objects of critique by period"
    graf.y_axis.title = "Share of studies"
    graf.y_axis.number_format = "0%"
    graf.add_data(Reference(ws, min_col=7, max_col=10, min_row=3, max_row=6), titles_from_data=True)
    graf.set_categories(Reference(ws, min_col=1, min_row=4, max_row=6))
    for s, color in zip(graf.series, ["2F75B5", "9DC3E6", "A6A6A6", "D9D9D9"]):
        s.graphicalProperties.line.solidFill = color
        s.graphicalProperties.line.width = 28000
        s.marker.symbol = "circle"
        s.smooth = False
    graf.height, graf.width = 9, 16
    ws.add_chart(graf, "A9")
    anchos(ws, [12, 9] + [16] * 8)

    # Figura 5: tradiciones por objetos
    ws = wb.create_sheet("Fig5_Heatmap")
    titulo(ws, "Figure 5. Theoretical traditions by objects of critique",
           "Left block: counts (inputs). Right block: share of each tradition (formulas), shaded by a colour scale.")
    marcos = [k for k in analisis["coocurrencias"]]
    temas = ["tema: Inteligencia artificial", "tema: Algoritmos, datos y plataformas", "tema: Redes sociales",
             "tema: Desinformación y posverdad", "tema: Privacidad y vigilancia", "tema: Discurso de odio y radicalización"]
    cabecera(ws, 3, ["Tradition", "Studies"] + [ETIQUETAS[t] for t in temas] + [""] + [ETIQUETAS[t] + " %" for t in temas])
    ws.cell(3, 9).fill = PatternFill()
    for i, m in enumerate(marcos, 4):
        ws.cell(i, 1, ETIQUETAS[m]).font = NORMAL
        ws.cell(i, 2, analisis["categorias"][m]["total"]).font = ENTRADA
        for j, t in enumerate(temas):
            ws.cell(i, 3 + j, analisis["coocurrencias"][m][t]).font = ENTRADA
            c = ws.cell(i, 10 + j, f"={get_column_letter(3 + j)}{i}/$B{i}")
            c.number_format, c.font = "0%", NORMAL
    fin = 3 + len(marcos)
    ws.conditional_formatting.add(f"J4:O{fin}", ColorScaleRule(start_type="num", start_value=0, start_color="FFFFFF",
                                                                end_type="num", end_value=0.4, end_color="2F75B5"))
    anchos(ws, [40, 9] + [14] * 6 + [3] + [14] * 6)

    # Tablas
    ws = wb.create_sheet("Table1_Eligibility")
    titulo(ws, "Table 1. Eligibility criteria")
    cabecera(ws, 3, ["Criterion", "Included", "Excluded"])
    criterios = [
        ("Concept", "CDL as defined in this review is a central focus of the study",
         "CDL is mentioned in passing; \"critical\" means only checking sources or generic critical thinking"),
        ("Context", "Formal education: early childhood, primary, secondary, higher education, initial and in-service teacher education",
         "Families, public libraries, communities or organisations with no link to an educational institution; informal learning"),
        ("Source", "Peer-reviewed journal articles and reviews", "Book reviews, editorials, conference proceedings"),
        ("Period and language", "2016–2026; English or Spanish", "Other periods and languages")]
    for i, fila in enumerate(criterios, 4):
        for j, v in enumerate(fila, 1):
            c = ws.cell(i, j, v)
            c.font, c.alignment = NORMAL, Alignment(wrap_text=True, vertical="top")
    anchos(ws, [20, 55, 55])

    ws = wb.create_sheet("Table2_Agreement")
    titulo(ws, "Table 2. Agreement between the two screening passes and outcome of adjudication")
    cabecera(ws, 3, ["", "Pass 2: include", "Pass 2: exclude", "Total"])
    ws["A4"], ws["B4"], ws["C4"] = "Pass 1: include", 85, 44
    ws["A5"], ws["B5"], ws["C5"] = "Pass 1: exclude", 50, 290
    ws["A6"] = "Total"
    for r in (4, 5):
        ws[f"D{r}"] = f"=B{r}+C{r}"
        ws[f"B{r}"].font = ws[f"C{r}"].font = ENTRADA
    for col in "BCD":
        ws[f"{col}6"] = f"={col}4+{col}5"
        ws[f"{col}6"].font = NEGRITA
    ws["A8"], ws["B8"] = "Observed agreement", "=(B4+C5)/D6"
    ws["B8"].number_format = "0.0%"
    ws["A9"], ws["B9"] = "Cohen's kappa", "=(B8-((D4*B6+D5*C6)/D6^2))/(1-(D4*B6+D5*C6)/D6^2)"
    ws["B9"].number_format = "0.00"
    cabecera(ws, 11, ["Outcome", "Records", "Final decision"])
    resultados = [("Both passes include", 85, "Included"), ("Both passes exclude", 290, "Excluded"),
                  ("Disagreement; title names CDL", 22, "Included"),
                  ("Disagreement; title refers to a digital technology and at least two of K, A, P", 28, "Included"),
                  ("Disagreement; insufficient evidence", 38, "Excluded"),
                  ("Disagreement; excluded in pass 1 for context or document type", 6, "Excluded")]
    for i, (a, b, c3) in enumerate(resultados, 12):
        ws.cell(i, 1, a).font = NORMAL
        ws.cell(i, 2, b).font = ENTRADA
        ws.cell(i, 3, c3).font = NORMAL
    ws["A18"], ws["B18"] = "Included", '=SUMIF(C12:C17,"Included",B12:B17)'
    ws["A19"], ws["B19"] = "Excluded", '=SUMIF(C12:C17,"Excluded",B12:B17)'
    ws["A18"].font = ws["A19"].font = NEGRITA
    anchos(ws, [70, 16, 16, 10])

    ws = wb.create_sheet("Table3_Level_design")
    titulo(ws, "Table 3. Educational level, design and language by period",
           "Trend: Cochran–Armitage test computed in analisis.py (typed values in blue).")
    f = cabecera_periodos(ws)
    f = tabla_periodos(ws, f, analisis, ["nivel: Infantil y primaria", "nivel: Secundaria", "nivel: Universidad",
                                         "nivel: Formación docente"], "Educational level")
    f = tabla_periodos(ws, f, analisis, ["diseño: Cualitativo", "diseño: Cuantitativo", "diseño: Teórico o conceptual",
                                         "diseño: Diseño o intervención", "diseño: Revisión de literatura"], "Design")
    f = tabla_periodos(ws, f, analisis, ["idioma: español"], "Language")
    ws.cell(f + 1, 1, f"Codes are not mutually exclusive. No level code: {analisis['sin_nivel']} studies; no design code: {analisis['sin_diseno']}.").font = NOTA
    anchos(ws, [36] + [11] * 10)

    ws = wb.create_sheet("Table4_Traditions")
    titulo(ws, "Table 4. Theoretical traditions by period", "Trend: Cochran–Armitage test (typed values in blue).")
    f = cabecera_periodos(ws)
    f = tabla_periodos(ws, f, analisis, ["marco: Alfabetización mediática",
                                         "marco: Multiliteracidades y nuevos estudios de literacidad",
                                         "marco: Ciudadanía digital",
                                         "marco: Perspectivas críticas de raza, género y decolonialidad",
                                         "marco: Pedagogía crítica (Freire)"])
    anchos(ws, [42] + [11] * 10)

    ws = wb.create_sheet("Table5_Robustness")
    titulo(ws, "Table 5. Robustness of the main trends to the coding dictionary",
           "Strict dictionaries keep only the least ambiguous terms (Appendix A3). Trend: Cochran–Armitage test.")
    cabecera(ws, 3, ["Category", "Dictionary", "2016–2019 n", "%", "2020–2023 n", "%", "2024–2026 n", "%", "Trend z", "p"])
    ws.cell(4, 1, "Studies in period (n)").font = NEGRITA
    for j, t in enumerate(TOTALES):
        ws.cell(4, 3 + 2 * j, t).font = ENTRADA
    fila = 5
    orden = ["tema: Inteligencia artificial", "tema: Algoritmos, datos y plataformas", "tema: Redes sociales",
             "nivel: Infantil y primaria", "nivel: Secundaria", "nivel: Universidad", "nivel: Formación docente"]
    for k in orden:
        for dic in ("amplio", "estricto"):
            v = analisis["robustez"][k][dic]
            ws.cell(fila, 1, ETIQUETAS[k] if dic == "amplio" else "").font = NORMAL
            ws.cell(fila, 2, "Broad" if dic == "amplio" else "Strict").font = NORMAL
            for j, x in enumerate(v["x"]):
                ws.cell(fila, 3 + 2 * j, x).font = ENTRADA
                c = ws.cell(fila, 4 + 2 * j, f"={get_column_letter(3 + 2 * j)}{fila}/{get_column_letter(3 + 2 * j)}$4")
                c.number_format, c.font = "0.0%", NORMAL
            for col, val, fmt in ((9, v["z"], "0.00"), (10, v["p"], "0.000")):
                c = ws.cell(fila, col, round(val, 4))
                c.number_format, c.font = fmt, ENTRADA
            fila += 1
    anchos(ws, [32, 11] + [11] * 8)

    ws = wb.create_sheet("Table6_Practices")
    titulo(ws, "Table 6. Pedagogical practices described in the corpus (illustrative)")
    cabecera(ws, 3, ["Practice", "What learners do", "Examples"])
    practicas = [
        ("Critical analysis of digital texts", "Read memes, videos, teaching materials or AI outputs for representation, bias and ideology",
         "Elmore (2019); Ho (2025); Van Poucke (2024); Weninger (2026)"),
        ("Media production and multimodal composing", "Produce video, stories, posters or multimodal texts that answer dominant narratives",
         "Watt (2019); Noble (2022); de los Ríos (2018); Damaskinidis et al. (2026)"),
        ("Virtual exchange", "Work with peers in other countries and examine how platforms shape the exchange",
         "Hauck (2019); Bilki et al. (2023); Satar et al. (2023); Ketzer-Nöltge (2022)"),
        ("Designed modules and inquiry", "Follow a sequence built around a game, a controversy or a writing task",
         "Torras et al. (2026); Gerlach et al. (2025); Spracklin (2025); Lo et al. (2024)"),
        ("Civic action", "Use digital tools to investigate and act on local or political issues",
         "Kwon (2019); Abowitz (2020); Fernández (2026); Tanksley (2024)")]
    for i, fila in enumerate(practicas, 4):
        for j, v in enumerate(fila, 1):
            c = ws.cell(i, j, v)
            c.font, c.alignment = NORMAL, Alignment(wrap_text=True, vertical="top")
    ws.cell(10, 1, "Two-author studies are listed by first author only here; see the manuscript for full citations.").font = NOTA
    anchos(ws, [34, 60, 60])

    ws = wb.create_sheet("Table7_Most_cited")
    titulo(ws, "Table 7. The ten most cited studies", "Scopus citations on 27 October 2026. Per year: citations / (2026 − year + 1).")
    cabecera(ws, 3, ["First author", "Year", "Journal", "Title", "Citations", "Per year", "DOI"])
    top = sorted(cod, key=lambda x: -int(x["citas"] or 0))[:10]
    for i, x in enumerate(top, 4):
        m = meta[x["eid"]]
        for j, v in enumerate([m["apellido"], int(x["anio"]), x["revista"], x["titulo"]], 1):
            ws.cell(i, j, v).font = NORMAL
        ws.cell(i, 5, int(x["citas"])).font = ENTRADA
        c = ws.cell(i, 6, f"=E{i}/(2026-B{i}+1)")
        c.number_format, c.font = "0.0", NORMAL
        ws.cell(i, 7, x["doi"]).font = NORMAL
    ws.cell(14, 4, "Total, ten most cited").font = NEGRITA
    ws.cell(14, 5, "=SUM(E4:E13)").font = NEGRITA
    ws.cell(15, 4, "All 135 studies").font = NORMAL
    ws.cell(15, 5, analisis["citas"]["total"]).font = ENTRADA
    ws.cell(16, 4, "Share of the ten most cited").font = NORMAL
    c = ws.cell(16, 5, "=E14/E15")
    c.number_format = "0.0%"
    anchos(ws, [18, 7, 34, 70, 10, 9, 32])

    # S1: estudios incluidos
    ws = wb.create_sheet("S1_Included")
    titulo(ws, "Supplementary file S1. The 135 included studies", "Codes: 1 = present in title, abstract or keywords (Appendix A3).")
    codigos = [k for k in cod[0] if k.split(":")[0] in ("nivel", "diseño", "marco", "tema")]
    columnas = ["EID", "DOI", "Year", "First author", "Authors (n)", "Title", "Journal", "Volume", "Issue", "Pages / article",
                "Language", "Countries", "Citations", "Open access"] + [ETIQUETAS[k] for k in codigos]
    cabecera(ws, 3, columnas)
    for i, x in enumerate(sorted(cod, key=lambda x: (meta[x["eid"]]["apellido"].lower(), x["anio"])), 4):
        m = meta[x["eid"]]
        valores = [x["eid"], x["doi"], int(x["anio"]), f"{m['apellido']}, {m['iniciales']}", int(m["n_autores"] or 1),
                   x["titulo"], x["revista"], m["volumen"], m["numero"], m["paginas"] or m["articulo"],
                   "Spanish" if x["idioma"] == "español" else "English", x["paises"], int(x["citas"] or 0),
                   "Yes" if x["acceso_abierto"] == "True" else "No"] + [1 if x[k] else None for k in codigos]
        for j, v in enumerate(valores, 1):
            ws.cell(i, j, v).font = NORMAL
    ws.freeze_panes = "A4"
    ws.auto_filter.ref = f"A3:{get_column_letter(len(columnas))}{3 + len(cod)}"
    anchos(ws, [20, 28, 6, 22, 8, 60, 34, 8, 8, 12, 9, 26, 9, 9] + [12] * len(codigos))

    # S2: cribado
    ws = wb.create_sheet("S2_Screening")
    titulo(ws, "Supplementary file S2. Screening of the 469 records",
           "K, A, P: indicators of pass 2; T names / T digital: title indicators used only in adjudication.")
    columnas = ["No.", "EID", "Year", "Title", "Journal", "Pass 1", "Pass 2", "K keywords", "A abstract", "P power",
                "T names CDL", "T digital", "Disagreement", "Rule applied", "Final decision"]
    cabecera(ws, 3, columnas)
    traduce = {"Incluido": "Included", "Excluido": "Excluded", "Excluido: la ADC no es el foco": "Excluded: CDL not the focus",
               "Excluido: contexto no formal": "Excluded: outside formal education",
               "Excluido: tipo de documento (reseña)": "Excluded: book review",
               "acuerdo entre fases": "agreement between passes",
               "exclusión por contexto o tipo de documento": "exclusion for context or document type",
               "discrepancia: el título nombra la ADC": "disagreement: title names CDL",
               "discrepancia: título digital y dos indicios de resumen o palabras clave": "disagreement: digital title and two indicators",
               "discrepancia: indicios insuficientes": "disagreement: insufficient evidence"}
    for i, x in enumerate(sel, 4):
        valores = [int(x["n"]), x["eid"], int(x["anio"]), x["titulo"], x["revista"], traduce[x["fase1"]],
                   traduce[x["fase2"]], x["K_claves"] or None, x["A_resumen"] or None, x["P_poder"] or None,
                   x["T_nombra"] or None, x["T_digital"] or None, x["discrepancia"] or None, traduce[x["regla"]],
                   traduce[x["decision"]]]
        for j, v in enumerate(valores, 1):
            ws.cell(i, j, int(v) if isinstance(v, str) and v == "1" else v).font = NORMAL
    ws.freeze_panes = "A4"
    ws.auto_filter.ref = f"A3:O{3 + len(sel)}"
    anchos(ws, [5, 20, 6, 70, 32, 26, 10, 8, 8, 8, 8, 8, 10, 40, 12])

    # S3: lista de verificación PRISMA-ScR
    ws = wb.create_sheet("S3_PRISMA-ScR")
    titulo(ws, "Supplementary file S3. PRISMA-ScR checklist", "Where each item (Tricco et al., 2018) is reported in the manuscript.")
    cabecera(ws, 3, ["No.", "Section", "Item", "Reported in"])
    items = [
        ("Title", "Identify the report as a scoping review", "Title"),
        ("Abstract", "Structured summary", "Abstract"),
        ("Introduction", "Rationale", "Introduction, paragraphs 1–4"),
        ("Introduction", "Objectives", "Introduction, RQ1–RQ4"),
        ("Methods", "Protocol and registration", "Method, Design (no protocol registered; data and code openly available)"),
        ("Methods", "Eligibility criteria", "Method, Eligibility criteria; Table 1"),
        ("Methods", "Information sources", "Method, Information source and search"),
        ("Methods", "Full search strategy", "Appendix A1"),
        ("Methods", "Selection of sources of evidence", "Method, Selection of sources; Table 2; verification by a second reviewer"),
        ("Methods", "Data charting process", "Method, Charting the data"),
        ("Methods", "Data items", "Method, Charting the data; Appendix A3"),
        ("Methods", "Critical appraisal of individual sources (optional)", "Method, Analysis: not carried out"),
        ("Methods", "Synthesis of results", "Method, Analysis"),
        ("Results", "Selection of sources of evidence", "Results, Selection; Figure 1"),
        ("Results", "Characteristics of sources of evidence", "Results; Table 3; Figures 2–3; S1"),
        ("Results", "Critical appraisal within sources (optional)", "Not applicable"),
        ("Results", "Results of individual sources of evidence", "S1; Tables 6–7"),
        ("Results", "Synthesis of results", "Results, RQ1–RQ4; Tables 3–7; Figures 2–5"),
        ("Discussion", "Summary of evidence", "Discussion"),
        ("Discussion", "Limitations", "Limitations"),
        ("Discussion", "Conclusions", "Conclusion"),
        ("Funding", "Funding", "Title page, Declarations")]
    for i, (a, b, c3) in enumerate(items, 4):
        for j, v in enumerate((i - 3, a, b, c3), 1):
            ws.cell(i, j, v).font = NORMAL
    anchos(ws, [6, 14, 50, 70])

    wb.save(sys.argv[2])


if __name__ == "__main__":
    main()
