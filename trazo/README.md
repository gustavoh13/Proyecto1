# Trazo

App de una sola página (`index.html`) para revisar señales de estilo de IAG en un texto y redactar una declaración de uso transparente.

Se usa en línea en https://gustavoh13.github.io/Proyecto1/trazo/

## Qué hace

- Revisa un texto pegado o un archivo (.txt, .md, .docx, .pdf) en el navegador, sin enviarlo a ningún servidor.
- Marca fórmulas frecuentes en la escritura con IAG, tomadas en parte de la guía “Signs of AI writing” de Wikipedia, y entrega un porcentaje aproximado calculado por párrafos.
- Genera una declaración de uso de IAG con la tríada Intención, Interacción y Criterio del proyecto CRITERIA.
- Resume qué publican Turnitin, GPTZero y Pangram sobre sus métodos de detección.

## Límites

El porcentaje mide parecido de estilo con una lista de expresiones y la variación del largo de las oraciones. No identifica autoría, no está validado empíricamente y no equivale al resultado de Turnitin ni de otros detectores. No debe usarse como prueba.

## Créditos

- Autoría: Gustavo Herrera Urízar ([ORCID 0000-0003-3546-8976](https://orcid.org/0000-0003-3546-8976)), investigador principal de CRITERIA. Departamento de Didáctica y Organización Educativa, Facultad de Educación, Universitat de Barcelona.
- Proyecto: CRITERIA. Trazabilidad y criterio profesional en el uso de IAG en el portafolio docente digital (REDICE26-4122). Equipo: Joan Anton Sánchez, Carles Lindín, Lluís Parcerisa, Pablo Rivera y Ezequiel Passeron.
- Financiamiento: convocatoria [REDICE-26](https://www.ub.edu/idp/web/ca/redice26) de ayudas a proyectos de investigación en docencia universitaria, Institut de Desenvolupament Professional (IDP), Universitat de Barcelona.
- Uso de IAG: el código y los textos se redactaron con Claude (Anthropic) a partir de las indicaciones del autor, que revisó el resultado.

## Licencias

- Código: GNU GPL 3.0 o posterior (`LICENSE`).
- Contenidos: CC BY 4.0 (`LICENSE-CONTENIDOS.md`).
- Terceros: mammoth.js (BSD de 2 cláusulas), pdf.js (Apache 2.0), tipografías Atkinson Hyperlegible y Bricolage Grotesque (SIL OFL 1.1). Se cargan desde sus CDN y no se incluyen en este repositorio.

## Cómo citar

Herrera Urízar, G. (2026). *Trazo: revisión de señales de estilo de IAG y declaración de uso* [Aplicación web]. Proyecto CRITERIA (REDICE26-4122), Universitat de Barcelona. https://gustavoh13.github.io/Proyecto1/trazo/
