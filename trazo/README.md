# Trazo

App de una sola página (`index.html`) para revisar señales de estilo de IAG en un texto y redactar una declaración de uso transparente. Es bilingüe: la interfaz está en castellano y en catalán, y revisa textos en las dos lenguas.

App d’una sola pàgina per revisar senyals d’estil d’IAG en un text i redactar una declaració d’ús transparent. És bilingüe: la interfície és en castellà i en català, i revisa textos en les dues llengües.

Se usa en línea en https://gustavoh13.github.io/Proyecto1/trazo/

## Qué hace

- Revisa un texto pegado o un archivo (.txt, .md, .docx, .pdf) en el navegador, sin enviarlo a ningún servidor.
- Reconoce si el texto está en castellano o en catalán y aplica la lista de señales de esa lengua. También se puede elegir el idioma a mano.
- Marca fórmulas frecuentes en la escritura con IAG, tomadas en parte de la guía “Signs of AI writing” de Wikipedia, y entrega un porcentaje aproximado calculado por párrafos.
- Genera una declaración de uso de IAG con la tríada Intención, Interacción y Criterio del proyecto CRITERIA, en el idioma de la interfaz.
- Se instala como app en Windows, Mac, iPhone, iPad y Android (botón “Instalar la app”). Usa `manifest.webmanifest`, `sw.js` y los íconos de `icons/`; una vez instalada, la revisión de textos pegados funciona sin conexión.
- Resume qué publican Turnitin, GPTZero y Pangram sobre sus métodos de detección.

## Límites

El porcentaje mide parecido de estilo con listas de expresiones en castellano y en catalán y la variación del largo de las oraciones. No identifica autoría, no está validado empíricamente y no equivale al resultado de Turnitin ni de otros detectores. No debe usarse como prueba.

## Créditos

- Autoría: Gustavo Herrera Urízar ([ORCID 0000-0003-3546-8976](https://orcid.org/0000-0003-3546-8976)), investigador principal de CRITERIA. Departamento de Didáctica y Organización Educativa, Facultad de Educación, Universitat de Barcelona.
- Proyecto: CRITERIA. Trazabilidad y criterio profesional en el uso de IAG en el portafolio docente digital (REDICE26-4122). Equipo: Joan Anton Sánchez, Carles Lindín, Pablo Rivera-Vargas y Ezequiel Passeron.
- Financiamiento: convocatoria [REDICE-26](https://www.ub.edu/idp/web/ca/redice26) de ayudas a proyectos de investigación en docencia universitaria, Institut de Desenvolupament Professional (IDP), Universitat de Barcelona.
- Uso de IAG: el código y los textos se redactaron con Claude (Anthropic) a partir de las indicaciones del autor, que revisó el resultado.

## Licencias

- Código: GNU GPL 3.0 o posterior (`LICENSE`).
- Contenidos: CC BY 4.0 (`LICENSE-CONTENIDOS.md`).
- Terceros: mammoth.js (BSD de 2 cláusulas), pdf.js (Apache 2.0), tipografías Atkinson Hyperlegible y Bricolage Grotesque (SIL OFL 1.1). Se cargan desde sus CDN y no se incluyen en este repositorio.

## Cómo citar

Herrera Urízar, G. (2026). *Trazo: revisión de señales de estilo de IAG y declaración de uso* [Aplicación web]. Proyecto CRITERIA (REDICE26-4122), Universitat de Barcelona. https://gustavoh13.github.io/Proyecto1/trazo/
