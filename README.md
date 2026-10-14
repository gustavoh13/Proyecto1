# El alma en la plataforma

*Escuela, datos y libertad en la era de las plataformas*
Gustavo Herrera Urízar

Ensayo de filosofía para público culto. Unas 27.300 palabras de texto principal, con notas finales en APA 7, glosario y bibliografía (lecturas comentadas y referencias).

> La escuela no ha sido sustituida por las plataformas: se ha vuelto uno de los lugares donde las plataformas aprenden a formar sujetos.

## Estructura

Cada capítulo toma un tema y lo sigue a través de las épocas, de Sócrates a la plataforma escolar, sostenido por una lectura propia que recorre todo el libro: la *pedagogía de la huella* y las cuatro operaciones de la plataforma (tiempo, visibilidad, relación y medida). No hay partes ni subtítulos internos, solo pausas (`* * *`).

| Archivo | Capítulo | Hilo |
| --- | --- | --- |
| `libro/00-prologo.md` | Prólogo. Una inquietud | Desde dónde se escribe, definición de plataforma, las cuatro tesis |
| `libro/01-el-sello-en-la-cera.md` | 1. El sello en la cera | *Paideia*, Durkheim, Sócrates y Platón, *skholé*, Hiparquia, Diotima; del sello a la huella |
| `libro/02-una-red-sin-dueno.md` | 2. Una red sin dueño | Dispositivo, la Señal, las cuatro operaciones, lo que la escuela presta a las plataformas, *oikonomía*, profanar |
| `libro/03-el-alma-prision-del-cuerpo.md` | 3. El alma, prisión del cuerpo | Kant y la silla, disciplina, objeción de Fraser, Pasolini, Spinoza y La Boétie, contra la nostalgia |
| `libro/04-escultores-de-si-mismos.md` | 4. Escultores de sí mismos | Pico, Rousseau y Sofía, Wollstonecraft, capital humano, el cuadro de mando del alumno, Ball y el docente |
| `libro/05-ser-visto.md` | 5. Ser visto | Poder pastoral, panóptico, datificación, Purdue y Georgia State, Helsingør 2022-2024, Reglamento de IA, privacidad |
| `libro/06-la-memoria-fuera-de-nosotros.md` | 6. La memoria fuera de nosotros | *Pharmakon*, Stiegler, Simondon, PISA 2015 y 2022, UNESCO 2023, quienes eligen la pantalla, IA generativa |
| `libro/07-lo-que-no-tiene-precio.md` | 7. Lo que no tiene precio | Chile hasta 2026, qué significa «gratis», Francia y Barcelona, límites del software libre, gamificación |
| `libro/08-tiempo-libre.md` | 8. Tiempo libre | Prohibición del móvil, crítica y contraconductas, Ofqual 2020, cuidado, *edutropía* en cuatro direcciones |
| `libro/09-epilogo.md` | Epílogo. Conócete a ti mismo, otra vez | Idea-fuerza y cierre en Delfos |
| `libro/10-glosario.md` | Glosario | Conceptos clave, incluidos *pedagogía de la huella* y *plataforma educativa* |
| `libro/11-lecturas.md` | Bibliografía | Lecturas comentadas por capítulo y lista de referencias en APA 7 |

Material editorial en `editorial/`: sinopsis, contracubierta, índice comentado y subtítulos alternativos (`sinopsis.md`), lo que queda pendiente para el autor (`notas-para-el-autor.md`) y los informes de auditoría documental (`auditoria/`).

## Versiones compiladas

En `salida/`: PDF maquetado (A5), EPUB, HTML, un Markdown único y un DOCX de manuscrito para la editorial (A4, Times New Roman 12, interlineado 1,5, notas al pie nativas de Word con numeración continua, índice fijo y números de página). Si la editorial prefiere notas finales, Word las convierte de una vez desde Referencias > Notas al pie > Convertir. Para los formularios de envío que piden PDF está `el-alma-en-la-plataforma-manuscrito.pdf`, el mismo manuscrito convertido con LibreOffice y con los números de página en el índice.

Para regenerarlas después de editar los capítulos:

```bash
./compilar.sh
```

Requiere `pandoc` y `python3` con `pyphen` y `pypdf` (`pip install pyphen pypdf`); el PDF se genera con Chromium en modo headless y el del manuscrito, con LibreOffice (`soffice`). La plantilla de Word la genera `herramientas/plantilla_word.py`. El script `herramientas/notas_finales.py` convierte las notas al pie de cada capítulo en notas finales agrupadas por capítulo, con la numeración reiniciada en cada uno. En los archivos de `libro/` las notas siguen escritas como notas al pie (`[^c3-kant]`), que es lo más cómodo para editar.

Ajustes del PDF que hace `compilar.sh` por su cuenta:

- **Partición de palabras.** Chromium no sabe partir palabras en español, y en un texto justificado una palabra larga que no cabe estira la línea anterior. `herramientas/lineas_estiradas.py` localiza esas líneas en el PDF y `herramientas/guionado.py` añade puntos de partición (con `pyphen`) solo a la palabra que no cupo; el ciclo se repite hasta que no queda ninguna. Así el resto del texto se puede copiar y buscar sin caracteres invisibles.
- **Enlaces internos.** `herramientas/destinos_pdf.py` corrige la posición de los destinos de las llamadas de nota y de sus retornos, que Chromium calcula sin los márgenes de la página.
- **URL.** Las URL de la bibliografía son enlaces activos en todas las versiones. En el PDF, `estilos/cortes-url.lua` solo permite cortarlas después de una barra o antes de un punto o un guion, nunca en mitad de una palabra o de un número.

## Decisiones editoriales

- **Ensayo original.** El libro se presenta como ensayo, no como tesis adaptada. El origen doctoral se menciona en una sola línea al final de la bibliografía.
- **Voz de autor.** Primera persona y una lectura propia sostenida: la escuela presta a las plataformas un público obligatorio, autoridad y tiempo largo; la *pedagogía de la huella*; las cuatro operaciones; la prohibición del móvil que deja intacta la infraestructura; la IA generativa como crisis de un sistema que solo sabía leer huellas.
- **Menos autores.** Se conservan las referencias que cambian el argumento y se podaron las que solo lo reforzaban (lista en `auditoria-referencias.md`).
- **Plataforma, definida.** El prólogo define «plataforma educativa» y distingue tipos y dueños; el capítulo 2 lo desarrolla.
- **Casos verificables.** Purdue y Georgia State, Helsingør, Vanderbilt y los detectores de IA, el experimento de Bastani, Ofqual 2020, Francia 2021-2022, el proyecto DD de Barcelona, la prohibición del móvil en Cataluña y las reformas chilenas. Donde encaja una escena propia del autor hay un comentario invisible `<!-- ESCENA DEL AUTOR -->`.
- **Objeciones con peso.** La crítica de Fraser a Foucault; la evaluación formativa; los defensores de la analítica; las pruebas estandarizadas; y, con más espacio, las tres objeciones que pedía la revisión: no idealizar la escuela anterior (cap. 3), las comunidades que eligen herramientas digitales por accesibilidad, continuidad, colaboración o falta de recursos (cap. 6) y los límites del software libre (cap. 7).
- **Generalizaciones matizadas.** «Cuando el producto es gratis…», la «providencia» algorítmica y el «precio cero» se aplican solo a los modelos a los que corresponden, distinguiendo plataformas públicas, académicas, cooperativas y corporativas.
- **Notas.** Notas finales reducidas y agrupadas por capítulo, con citas autor-año en APA 7 y localizador; lista de referencias en APA 7 precedida de lecturas comentadas.
- **Pedagogía de la huella, delimitada.** El capítulo 2 distingue tres operaciones (evidencia para conversar, registro para gestionar, registro como sustituto y criterio de valor); el concepto designa solo la tercera.
- **Fines.** La tesis no es que la escuela carezca de fines, sino que la gestión los desplaza y los sustrae a la discusión (fines declarados, objetivos administrativos y orientaciones incorporadas).
- **Desde dónde se habla.** El prólogo distingue el registro del profesor, el del investigador y el del ensayista; las escenas compuestas se presentan como tales. Las escenas situadas proceden del trabajo de campo del autor (entrevistas de 2025, proyectos edDIT y USMOV).
- **Depuración.** Tras la segunda revisión se aligeró el andamiaje: prólogo metodológico en dos párrafos, escenas compuestas identificadas una sola vez, cautelas históricas integradas en la frase, menos anuncios y recapitulaciones, y perfiles de entrevistados menos identificables.
- **Trazabilidad.** Cada cifra se ha auditado por fuente, localizador, tipo de fuente, población y alcance causal (`editorial/auditoria/`).
- **Estilo.** Sin rayas largas para los incisos, sin conectores repetidos ni fórmulas en serie.

## Correcciones respecto de la tesis

Al reescribir se corrigieron algunos datos que conviene revisar también en la tesis:

- "Hiparquía de Marne" → **Hiparquia de Maronea**.
- Wollstonecraft escribió la *Vindicación* **contra** la educación de Sofía en el *Emilio* de Rousseau, no en consonancia con él.
- Christine de Pizan es medieval tardía (1364-c. 1430), no de la Ilustración.
- La decisión de Datatilsynet de 2022 no expulsó a Google de las escuelas danesas: en 2024 se resolvió limitando los fines para los que la empresa puede usar los datos.
- La *Recomendación sobre la ética de la IA* de la UNESCO es de **2021**.
- En la tesis hay notas al pie desplazadas (por ejemplo, la cita del *Fedón* atribuida a Lipman, o la de Aristóteles a Gramsci). Además, varias citas entrecomilladas de Simondon, Heidegger, Stiegler, Latour, Castells, Turkle, Jenkins y Han no parecen literales; en el libro se han parafraseado o eliminado.

## Pendiente para el autor

Ver `editorial/notas-para-el-autor.md`: escenas propias, frases biográficas, datos de 2026 que hay que revisar antes de imprimir y agradecimientos.
