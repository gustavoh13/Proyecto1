# Revisión: alfabetización digital crítica en la educación formal

Datos de la revisión publicada en https://claude.ai/artifact/HfwT4tVU3YSjkARNGCF3Lq
y del artículo https://claude.ai/artifact/2E3hPj2qi66jQdQ7CPinNj
(Scopus, 2016-2026, inglés y español, consulta del 27 de octubre de 2026).

| Archivo | Contenido |
| --- | --- |
| `cadena-scopus.txt` | Cadena de búsqueda tal como se envió a Scopus |
| `01-registros-scopus.csv` | Los 469 registros que devolvió la búsqueda (`herramientas/scopus.py`) |
| `02-cribado.csv` | Los mismos registros con la decisión de cribado (columna `decision`) |
| `03-codificacion.csv` | Los 129 incluidos, con nivel, diseño, marco, tema e idioma (1 = presente) |
| `codificar.py` | Script que asigna esos códigos con consultas a Scopus |
| `04-metadatos.csv` | Volumen, número y páginas de los incluidos (`metadatos.py`) |
| `metadatos.py` | Script que los obtiene de la Abstract Retrieval API |

El cribado se hizo por título y revista, con un solo revisor, porque la clave de
Scopus disponible no da acceso a los resúmenes. Los códigos de `03-codificacion.csv`
indican que los términos de cada categoría aparecen en el título, el resumen o las
palabras clave del estudio, no que se haya leído el texto. Para repetir la
codificación: `python3 revision-adc/codificar.py revision-adc/02-cribado.csv revision-adc/03-codificacion.csv`.
