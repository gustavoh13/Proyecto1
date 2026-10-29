#!/usr/bin/env python3
"""Genera estilos/plantilla.docx, la plantilla de Word del manuscrito.

Parte de la plantilla por defecto de pandoc y la ajusta a un formato de
manuscrito editorial: Times New Roman 12, interlineado 1,5, sangría de
primera línea, títulos en negro, notas al pie a 10 puntos, A4 y número de
página centrado en el pie.

Uso: plantilla_word.py RUTA_SALIDA [idioma, por defecto es-ES]
"""
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

FUENTE = "Times New Roman"
RFONTS = f'<w:rFonts w:ascii="{FUENTE}" w:hAnsi="{FUENTE}" w:eastAsia="{FUENTE}" w:cs="{FUENTE}" />'


def estilo(xml, sid, ppr=None, rpr=None):
    """Sustituye el pPr y el rPr de un estilo concreto."""
    patron = re.compile(r'(<w:style [^>]*w:styleId="%s".*?</w:style>)' % sid, re.S)
    m = patron.search(xml)
    if not m:
        raise SystemExit(f"Estilo no encontrado: {sid}")
    bloque = m.group(1)
    nuevo = re.sub(r"<w:pPr>.*?</w:pPr>", "", bloque, flags=re.S)
    nuevo = re.sub(r"<w:rPr>.*?</w:rPr>", "", nuevo, flags=re.S)
    extra = (f"<w:pPr>{ppr}</w:pPr>" if ppr else "") + (f"<w:rPr>{rpr}</w:rPr>" if rpr else "")
    nuevo = nuevo.replace("</w:style>", extra + "</w:style>")
    return xml.replace(bloque, nuevo)


def ajustar_estilos(xml, idioma="es-ES"):
    # Valores por defecto: fuente, tamaño, idioma e interlineado 1,5
    xml = re.sub(r"<w:rPrDefault>.*?</w:rPrDefault>",
                 f'<w:rPrDefault><w:rPr>{RFONTS}<w:sz w:val="24" /><w:szCs w:val="24" />'
                 f'<w:lang w:val="{idioma}" w:eastAsia="{idioma}" w:bidi="ar-SA" /></w:rPr></w:rPrDefault>',
                 xml, flags=re.S)
    xml = re.sub(r"<w:pPrDefault>.*?</w:pPrDefault>",
                 '<w:pPrDefault><w:pPr><w:spacing w:after="0" w:line="360" w:lineRule="auto" /></w:pPr></w:pPrDefault>',
                 xml, flags=re.S)
    cuerpo = '<w:spacing w:before="0" w:after="0" w:line="360" w:lineRule="auto" /><w:ind w:firstLine="567" /><w:jc w:val="both" />'
    xml = estilo(xml, "BodyText", ppr=cuerpo)
    xml = estilo(xml, "FirstParagraph", ppr=cuerpo.replace('w:firstLine="567"', 'w:firstLine="0"'))
    xml = estilo(xml, "Compact", ppr='<w:spacing w:before="0" w:after="60" w:line="360" w:lineRule="auto" />')
    xml = estilo(xml, "Title",
                 ppr='<w:keepNext /><w:keepLines /><w:spacing w:before="2400" w:after="240" /><w:jc w:val="center" />',
                 rpr=f'{RFONTS}<w:sz w:val="44" /><w:szCs w:val="44" />')
    xml = estilo(xml, "Subtitle",
                 ppr='<w:keepNext /><w:keepLines /><w:spacing w:before="0" w:after="1200" /><w:jc w:val="center" />',
                 rpr=f'{RFONTS}<w:i /><w:sz w:val="28" /><w:szCs w:val="28" />')
    xml = estilo(xml, "Author",
                 ppr='<w:keepNext /><w:keepLines /><w:spacing w:before="0" w:after="0" /><w:jc w:val="center" />',
                 rpr=f'{RFONTS}<w:caps /><w:sz w:val="24" /><w:szCs w:val="24" />')
    xml = estilo(xml, "Heading1",
                 ppr='<w:keepNext /><w:keepLines /><w:pageBreakBefore /><w:spacing w:before="1200" w:after="600" w:line="240" w:lineRule="auto" /><w:outlineLvl w:val="0" />',
                 rpr=f'{RFONTS}<w:sz w:val="32" /><w:szCs w:val="32" />')
    xml = estilo(xml, "Heading2",
                 ppr='<w:keepNext /><w:keepLines /><w:spacing w:before="360" w:after="120" w:line="240" w:lineRule="auto" /><w:outlineLvl w:val="1" />',
                 rpr=f'{RFONTS}<w:b /><w:bCs /><w:sz w:val="24" /><w:szCs w:val="24" />')
    xml = estilo(xml, "BlockText",
                 ppr='<w:spacing w:before="120" w:after="120" w:line="276" w:lineRule="auto" /><w:ind w:left="567" w:right="567" w:firstLine="0" /><w:jc w:val="both" />',
                 rpr='<w:sz w:val="22" /><w:szCs w:val="22" />')
    xml = estilo(xml, "FootnoteText",
                 ppr='<w:spacing w:before="0" w:after="60" w:line="240" w:lineRule="auto" /><w:jc w:val="both" />',
                 rpr='<w:sz w:val="20" /><w:szCs w:val="20" />')
    xml = estilo(xml, "TOCHeading",
                 ppr='<w:keepNext /><w:spacing w:before="0" w:after="480" w:line="240" w:lineRule="auto" /><w:outlineLvl w:val="9" />',
                 rpr=f'{RFONTS}<w:sz w:val="32" /><w:szCs w:val="32" />')
    # Estilo propio para las pausas entre secciones (* * *)
    if 'w:styleId="Separador"' not in xml:
        xml = xml.replace("</w:styles>",
            '<w:style w:type="paragraph" w:customStyle="1" w:styleId="Separador">'
            '<w:name w:val="Separador" /><w:basedOn w:val="Normal" /><w:next w:val="FirstParagraph" /><w:qFormat />'
            '<w:pPr><w:keepNext /><w:spacing w:before="240" w:after="240" /><w:jc w:val="center" /></w:pPr>'
            '<w:rPr><w:spacing w:val="60" /></w:rPr></w:style>'
            '<w:style w:type="paragraph" w:customStyle="1" w:styleId="Indice">'
            '<w:name w:val="Indice" /><w:basedOn w:val="Normal" /><w:qFormat />'
            '<w:pPr><w:tabs><w:tab w:val="right" w:leader="dot" w:pos="8787" /></w:tabs>'
            '<w:spacing w:before="0" w:after="120" /></w:pPr></w:style></w:styles>')
    # Enlaces sin color ni subrayado (índice y referencias internas)
    xml = estilo(xml, "Hyperlink", rpr='<w:color w:val="000000" />')
    # Cualquier fuente de tema que quede pasa a Times New Roman
    xml = re.sub(r'<w:rFonts w:asciiTheme="[^"]*"[^>]*/>', RFONTS, xml)
    return xml


PIE = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
    '<w:ftr xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
    'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
    '<w:p><w:pPr><w:jc w:val="center" /></w:pPr>'
    '<w:r><w:fldChar w:fldCharType="begin" /></w:r>'
    '<w:r><w:instrText xml:space="preserve"> PAGE </w:instrText></w:r>'
    '<w:r><w:fldChar w:fldCharType="separate" /></w:r>'
    '<w:r><w:t>1</w:t></w:r>'
    '<w:r><w:fldChar w:fldCharType="end" /></w:r>'
    '</w:p></w:ftr>'
)

SECCION = (
    '<w:sectPr><w:footerReference w:type="default" r:id="rIdPie1" />'
    '<w:pgSz w:w="11906" w:h="16838" />'
    '<w:pgMar w:top="1418" w:right="1418" w:bottom="1418" w:left="1701" '
    'w:header="709" w:footer="709" w:gutter="0" /></w:sectPr>'
)


def main():
    salida = Path(sys.argv[1])
    idioma = sys.argv[2] if len(sys.argv) > 2 else "es-ES"
    with tempfile.TemporaryDirectory() as tmp:
        base = Path(tmp) / "base.docx"
        subprocess.run(["pandoc", "-o", str(base), "--print-default-data-file", "reference.docx"], check=True)
        dir_x = Path(tmp) / "x"
        with zipfile.ZipFile(base) as z:
            z.extractall(dir_x)
        estilos = dir_x / "word" / "styles.xml"
        estilos.write_text(ajustar_estilos(estilos.read_text(encoding="utf-8"), idioma), encoding="utf-8")
        (dir_x / "word" / "footer1.xml").write_text(PIE, encoding="utf-8")
        rels = dir_x / "word" / "_rels" / "document.xml.rels"
        r = rels.read_text(encoding="utf-8")
        if "rIdPie1" not in r:
            r = r.replace("</Relationships>",
                          '<Relationship Id="rIdPie1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/footer" Target="footer1.xml" /></Relationships>')
            rels.write_text(r, encoding="utf-8")
        ct = dir_x / "[Content_Types].xml"
        c = ct.read_text(encoding="utf-8")
        if "footer1.xml" not in c:
            c = c.replace("</Types>",
                          '<Override PartName="/word/footer1.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.footer+xml" /></Types>')
            ct.write_text(c, encoding="utf-8")
        doc = dir_x / "word" / "document.xml"
        d = doc.read_text(encoding="utf-8")
        d = re.sub(r"<w:sectPr\s*/>|<w:sectPr>.*?</w:sectPr>", SECCION, d, flags=re.S)
        if 'xmlns:r=' not in d.split(">", 2)[1] + d[:500]:
            d = d.replace("<w:document ", '<w:document xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" ', 1)
        doc.write_text(d, encoding="utf-8")
        salida.parent.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(salida, "w", zipfile.ZIP_DEFLATED) as z:
            for f in sorted(dir_x.rglob("*")):
                if f.is_file():
                    z.write(f, f.relative_to(dir_x).as_posix())


if __name__ == "__main__":
    main()
