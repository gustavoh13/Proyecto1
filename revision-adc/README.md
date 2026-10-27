# Revisión: alfabetización digital crítica en la educación formal

Datos y código del artículo «From social media to generative AI: A scoping review of
critical digital literacy in formal education, 2016–2026», preparado para *Review of
Education* (documento: https://claude.ai/artifact/2E3hPj2qi66jQdQ7CPinNj, pestaña
*Manuscript*). Búsqueda en Scopus del 27 de octubre de 2026.

## Archivos

| Archivo | Contenido |
| --- | --- |
| `cadena-scopus.txt` | Cadena de búsqueda tal como se envió a Scopus |
| `01-registros-scopus.csv` | Los 469 registros de la búsqueda (`herramientas/scopus.py`) |
| `02-cribado.csv` | Fase 1: decisión por título y revista para cada registro |
| `05-cribado-resumenes.csv` | Fase 2: indicadores K, A y P, decisión, discrepancias y regla aplicada |
| `06-seleccion-final.csv` | Los 469 registros con las dos fases y la decisión final (135 incluidos) |
| `03-codificacion.csv` | Los 135 incluidos con nivel, diseño, tradición, objeto e idioma (1 = presente) |
| `04-metadatos.csv` | Primer autor, número de autores, volumen, número y páginas |
| `07-analisis.json` | Resultados: tendencias por periodo, crecimiento, coocurrencias, países, robustez |
| `figuras-y-tablas.xlsx` | Figuras como gráficos editables, tablas con fórmulas y suplementos S1 y S2 |
| `manuscrito-review-of-education.docx` | Exportación en Word del manuscrito |
| `09-crossref.json` | Autores, revista, volumen, número y páginas de cada estudio según Crossref (con doi.org y OpenAlex de respaldo) |
| `autores_crossref.py` | Genera `09-crossref.json` (necesita acceso a api.crossref.org) |
| `referencias.py` | Referencias APA 7 de los estudios citados y su forma en el texto |

## Cómo se reproduce

```bash
python3 revision-adc/cribado_resumenes.py revision-adc/02-cribado.csv revision-adc/05-cribado-resumenes.csv
# 06-seleccion-final.csv une 02 y 05 (columna decision = decisión final)
python3 revision-adc/codificar.py revision-adc/06-seleccion-final.csv revision-adc/03-codificacion.csv
python3 revision-adc/metadatos.py revision-adc/03-codificacion.csv revision-adc/04-metadatos.csv
python3 revision-adc/analisis.py revision-adc/03-codificacion.csv revision-adc/07-analisis.json
python3 revision-adc/autores_crossref.py revision-adc/04-metadatos.csv revision-adc/09-crossref.json
python3 revision-adc/libro_excel.py revision-adc revision-adc/figuras-y-tablas.xlsx
python3 revision-adc/referencias.py revision-adc/04-metadatos.csv revision-adc/09-crossref.json citados.txt > referencias.md
```

Los scripts usan la Scopus Search API y la Abstract Retrieval API, con la clave guardada
como secreto de red del entorno (cabecera `X-ELS-APIKey`). `analisis.py` necesita `numpy`
y `scipy`.

## Alcance y límites

La clave de Scopus disponible no devuelve el texto de los resúmenes, pero sí permite
buscar dentro de ellos. La fase 1 cribó por título y revista; la fase 2, independiente
del título, usó búsquedas en los resúmenes y las palabras clave. Las dos fases coinciden
en el 80 % de los registros (κ = 0,51) y las 94 discrepancias se resolvieron con la regla
descrita en el artículo. Una segunda persona leyó los resúmenes de las 94 discrepancias y de
75 registros con acuerdo (20 %) y confirmó las 169 decisiones. Los códigos de `03-codificacion.csv` indican que los términos de
cada categoría aparecen en el título, el resumen o las palabras clave, no que se haya
leído el texto.

Scopus solo da el primer autor de cada estudio; los demás salen de Crossref. Donde
Crossref se equivoca o no tiene el artículo, `referencias.py` fija los autores a mano y
dice de dónde salen (ORCID o la página de la revista): Jiménez Torras et al. (2026),
González-Villa y Gewerc (2026), Stewart et al. (2021), Ketzer-Nöltge y Markovic (2022) y
Salazar-Jiménez et al. (2026). También corrige las páginas de Mesquita-Romero et al. (2022),
que Scopus da como 41–51 (son 47–57), y da el título original de los seis estudios citados
que están en español, con la traducción entre corchetes. Quedan sin coautores cuatro
estudios que no se citan en el artículo y solo figuran en el suplemento S1: Bilenko et al.
(2026), Hendrix-Soto (2023), Muñoz-Saavedra (2025) y Zhang (2025).
