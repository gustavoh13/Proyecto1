# El alma en la plataforma

*Ensayo sobre educación, técnica y subjetividad en tiempos neoliberales*
Gustavo Herrera Urízar

Libro de filosofía (ensayo para público culto) escrito a partir de la tesis doctoral *Las tecnologías digitales en la educación neoliberal como dispositivo en la construcción de subjetividad*. Unas 24.000 palabras.

## Estructura

El ensayo no sigue un orden cronológico ni separa teoría y aplicación. Cada capítulo toma un tema y lo sigue a través de las épocas (de Sócrates a la plataforma escolar y de vuelta), y termina abriendo la pregunta del siguiente. No hay partes ni subtítulos internos, solo pausas (`* * *`).

| Archivo | Capítulo | Hilo |
| --- | --- | --- |
| `libro/00-prologo.md` | Prólogo. Una inquietud | Desde dónde se escribe y cómo se lee el libro |
| `libro/01-el-sello-en-la-cera.md` | 1. El sello en la cera | La educación como fabricación del alma: *paideia*, Durkheim, *skholé*, Hiparquia, Aspasia, Diotima, el currículo |
| `libro/02-una-red-sin-dueno.md` | 2. Una red sin dueño | El dispositivo (Foucault, Deleuze, Agamben), la «Señal» y la notificación, *oikonomía*, providencia algorítmica, profanar |
| `libro/03-el-alma-prision-del-cuerpo.md` | 3. El alma, prisión del cuerpo | Kant y la silla, Platón, Aristóteles, Descartes e Isabel de Bohemia, disciplina, Pasolini, Spinoza, La Boétie, identidad |
| `libro/04-escultores-de-si-mismos.md` | 4. Escultores de sí mismos | De Pico y la *Bildung* al emprendedor de sí: Rousseau y Sofía, Pizan, Wollstonecraft, Du Châtelet, capital humano, Han, Ball |
| `libro/05-ser-visto.md` | 5. Ser visto | De la confesión agustiniana al panel de control: poder pastoral, panóptico, datificación, dividuo, personalización, privacidad |
| `libro/06-la-memoria-fuera-de-nosotros.md` | 6. La memoria fuera de nosotros | El *pharmakon* del *Fedro*, Stiegler, Comenio, Simondon, Heidegger, IA generativa |
| `libro/07-lo-que-no-tiene-precio.md` | 7. Lo que no tiene precio | Artes liberales y sofistas, Chile como laboratorio, PISA, plataformas gratuitas, brechas, gamificación y juego |
| `libro/08-tiempo-libre.md` | 8. Tiempo libre | Resistencias, cuidado, hooks y Garcés, acción colectiva, *edutropía* |
| `libro/09-epilogo.md` | Epílogo. Conócete a ti mismo, otra vez | Cierre circular en Delfos |
| `libro/10-glosario.md` | Glosario | Los conceptos clave explicados con sencillez |
| `libro/11-lecturas.md` | Bibliografía | Bibliografía alfabética (auditada, ver `auditoria-referencias.md`) |

## Versiones compiladas

En `salida/`: PDF maquetado (A5), EPUB, DOCX (para revisar con control de cambios) y un Markdown único.

Para regenerarlas después de editar los capítulos:

```bash
./compilar.sh
```

Requiere `pandoc`; el PDF se genera con Chromium en modo headless.

## Decisiones editoriales

- **De tesis a ensayo.** Se eliminaron la metodología, las entrevistas, los proyectos edDIT y USMOV y los anexos. El libro es puramente filosófico.
- **Voz de autor.** Primera persona y prosa continua. Se conservan el origen chileno del autor, su experiencia docente y la mirada desde Cataluña.
- **Estilo.** Sin rayas largas para los incisos (se usan comas o paréntesis), sin conectores repetidos ni fórmulas del tipo «no es X, sino Y», y sin enumeraciones de tres en tres en cada párrafo.
- **Aparato crítico.** Notas al final de cada capítulo con la referencia precisa de cada cita (numeración Stephanus/Bekker para Platón y Aristóteles; capítulo, lección o fecha para los modernos). Bibliografía alfabética al final y glosario.
- **Objeciones.** Cada capítulo discute al menos una objeción seria a su propio argumento: la crítica de Fraser y Habermas a Foucault, los límites de Han, la investigación sobre evaluación formativa, los datos de la OCDE (2015) y la UNESCO (2023), los defensores de la evaluación estandarizada y la analítica del aprendizaje, el valor de la tecnología para el alumnado con discapacidad.
- **Título.** *El alma en la plataforma* retoma la idea de la tesis de que la educación neoliberal es un proyecto "para cambiar el alma". Alternativas posibles: *La fábrica del alma*, *El emprendedor de sí mismo va a la escuela*, *Educar en la era de los dispositivos*.

## Correcciones respecto de la tesis

Al reescribir se corrigieron algunos datos que conviene revisar también en la tesis:

- Aspasia aparece en el *Menéxeno* como maestra de retórica de **Sócrates** (no de Platón), y era de Mileto.
- "Hiparquía de Marne" → **Hiparquia de Maronea**.
- Areté de Cirene era **hija** de Aristipo y enseñó a **su hijo**, Aristipo el Joven (*metrodidaktos*).
- Hipatia pertenece a la Alejandría de la **Antigüedad tardía** (siglos IV-V), no a la Grecia clásica.
- Du Châtelet tradujo los *Principia* de Newton **del latín** al francés, no del inglés.
- Wollstonecraft escribió la *Vindicación* **contra** la educación de Sofía en el *Emilio* de Rousseau, no en consonancia con él.
- Christine de Pizan es medieval tardía (1364-c. 1430), no de la Ilustración.
- La cita sobre identidades "fragmentadas y fracturadas" es de **Stuart Hall** ("Who needs identity?", 1996).
- La *Recomendación sobre la ética de la IA* de la UNESCO es de **2021**.
- En la tesis hay notas al pie desplazadas (por ejemplo, la cita del *Fedón* atribuida a Lipman, o la de Aristóteles a Gramsci). Además, varias citas entrecomilladas de Simondon, Heidegger, Stiegler, Latour, Castells, Turkle, Jenkins y Han no parecen literales; en el libro se han parafraseado.

## Pendiente para el autor

- Revisar el tono y añadir, si se quiere, anécdotas reales del aula (no se inventó ninguna).
- Escribir los agradecimientos.
- Completar los datos editoriales de la bibliografía con las ediciones que realmente se usaron.
