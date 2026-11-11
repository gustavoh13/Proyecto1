# Trazo

App de una sola página (`index.html`) para revisar señales de estilo de IAG en un texto y redactar una declaración de uso transparente.

## Qué hace

- Revisa un texto pegado o un archivo (.txt, .md, .docx, .pdf) en el navegador, sin enviarlo a ningún servidor.
- Marca fórmulas frecuentes en la escritura con IAG, tomadas en parte de la guía “Signs of AI writing” de Wikipedia, y entrega un porcentaje aproximado calculado por párrafos.
- Genera una declaración de uso de IAG con la tríada Intención, Interacción y Criterio del proyecto CRITERIA (REDICE-26, Facultad de Educación, Universitat de Barcelona).
- Resume qué publican Turnitin, GPTZero y Pangram sobre sus métodos de detección.

## Límites

El porcentaje mide parecido de estilo con una lista de expresiones y la variación del largo de las oraciones. No identifica autoría, no está validado empíricamente y no equivale al resultado de Turnitin ni de otros detectores. No debe usarse como prueba.

## Uso

Abrir `index.html` en un navegador. Necesita conexión para cargar las tipografías y, al leer .docx o .pdf, las bibliotecas mammoth y pdf.js desde sus CDN. Los botones de segunda lectura y de descarga solo aparecen cuando la página se abre dentro de Claude.
