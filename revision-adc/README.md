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
| `autores_crossref.py` | Completa con Crossref los coautores y verifica las referencias (necesita acceso a api.crossref.org) |

## Cómo se reproduce

```bash
python3 revision-adc/cribado_resumenes.py revision-adc/02-cribado.csv revision-adc/05-cribado-resumenes.csv
# 06-seleccion-final.csv une 02 y 05 (columna decision = decisión final)
python3 revision-adc/codificar.py revision-adc/06-seleccion-final.csv revision-adc/03-codificacion.csv
python3 revision-adc/metadatos.py revision-adc/03-codificacion.csv revision-adc/04-metadatos.csv
python3 revision-adc/analisis.py revision-adc/03-codificacion.csv revision-adc/07-analisis.json
python3 revision-adc/libro_excel.py revision-adc revision-adc/figuras-y-tablas.xlsx
python3 revision-adc/referencias.py revision-adc/04-metadatos.csv citados.txt > referencias.md
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
leído el texto. Scopus solo da el primer autor de cada estudio, así que las referencias
marcan los coautores pendientes.
