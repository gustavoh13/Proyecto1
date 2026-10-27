#!/usr/bin/env python3
"""Da a un .docx exportado el formato que pide Review of Education para el envío.

Las normas piden texto a doble espacio y márgenes amplios. El script pone la
página en A4 con márgenes de 2,54 cm, el texto a doble espacio (las tablas y el
código, a espacio sencillo para que sigan siendo legibles), el número de página
en el pie y deja vacías las propiedades del archivo que podrían identificar al
autor en la versión anónima.

Uso: formato_docx.py entrada.docx salida.docx "Título del artículo"
"""
import sys

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt

# Estilos del texto corrido, que van a doble espacio
DOBLE = ("Normal", "List Paragraph", "Heading 1", "Heading 2", "Heading 3")


def numero_de_pagina(seccion):
    p = seccion.footer.paragraphs[0] if seccion.footer.paragraphs else seccion.footer.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run()
    for tipo, texto in (("begin", None), (None, "PAGE"), ("end", None)):
        if tipo:
            campo = OxmlElement("w:fldChar")
            campo.set(qn("w:fldCharType"), tipo)
        else:
            campo = OxmlElement("w:instrText")
            campo.set(qn("xml:space"), "preserve")
            campo.text = texto
        run._r.append(campo)


def main():
    entrada, salida, titulo = sys.argv[1:4]
    d = Document(entrada)
    for s in d.sections:
        s.page_width, s.page_height = Cm(21.0), Cm(29.7)
        s.left_margin = s.right_margin = s.top_margin = s.bottom_margin = Cm(2.54)
        numero_de_pagina(s)
    # Los archivos de pandoc añaden «Body Text» y «First Paragraph» al texto corrido
    for estilo in d.styles:
        if estilo.name in DOBLE + ("Body Text", "First Paragraph"):
            estilo.paragraph_format.line_spacing = 2.0
            estilo.paragraph_format.space_after = Pt(6)
    # Las celdas usan el estilo Normal: se dejan a espacio sencillo
    for tabla in d.tables:
        for fila in tabla.rows:
            for celda in fila.cells:
                for p in celda.paragraphs:
                    p.paragraph_format.line_spacing = 1.0
                    p.paragraph_format.space_after = Pt(2)
    for p in d.paragraphs:
        if p.style.name == "Code":
            p.paragraph_format.line_spacing = 1.0
    cp = d.core_properties
    cp.title, cp.author, cp.last_modified_by, cp.comments, cp.keywords = titulo, "", "", "", ""
    d.save(salida)


if __name__ == "__main__":
    main()
