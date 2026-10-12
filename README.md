# El alma en la plataforma

*Ensayo sobre educación, técnica y subjetividad en tiempos neoliberales*
Gustavo Herrera Urízar

Libro de filosofía (ensayo para público culto) escrito a partir de la tesis doctoral *Las tecnologías digitales en la educación neoliberal como dispositivo en la construcción de subjetividad*. El manuscrito tiene unas 39.000 palabras (unas 150 páginas en formato A5).

## Estructura

| Archivo | Contenido |
| --- | --- |
| `libro/00-prologo.md` | Prólogo. Una inquietud |
| **Primera parte. Cómo se fabrica un alma** | Genealogía de la educación como dispositivo |
| `libro/01-parte-primera.md` | 1. Conócete a ti mismo: la *paideia* y el ciudadano virtuoso |
| `libro/02-humanitas-y-fe.md` | 2. Del orador al creyente: *humanitas*, maestro interior y escolástica |
| `libro/03-bildung.md` | 3. Darse forma: Renacimiento, Ilustración y *Bildung* |
| `libro/04-escuela-maquina.md` | 4. La escuela-máquina: del Estado al mercado |
| **Segunda parte. La máquina sin rostro** | El concepto de dispositivo y de sujeto |
| `libro/05-dispositivo.md` | 5. ¿Qué es un dispositivo? (Foucault, Deleuze, Agamben) |
| `libro/06-oikonomia.md` | 6. *Oikonomía*: gobernar sin fundamento |
| `libro/07-sujeto.md` | 7. El sujeto no es una sustancia |
| **Tercera parte. El alma neoliberal** | Diagnóstico del presente |
| `libro/08-razon-neoliberal.md` | 8. La nueva razón del mundo |
| `libro/09-etica-del-rendimiento.md` | 9. El yo que se evalúa: ética del rendimiento |
| `libro/10-tecnica.md` | 10. Técnica, memoria y veneno (Simondon, Heidegger, Stiegler) |
| `libro/11-dividuo.md` | 11. El dividuo: personalización, performatividad e IA |
| `libro/12-vigilar-jugando.md` | 12. Vigilar jugando: datos, privacidad y gamificación |
| `libro/13-mercancia-desigualdad.md` | 13. El saber como mercancía y la desigualdad que no se ve |
| **Cuarta parte. Grietas** | Resistencias y alternativa |
| `libro/14-resistencias.md` | 14. Donde hay poder, hay resistencia |
| `libro/15-edutropia.md` | 15. Edutropía |
| `libro/16-epilogo.md` | Epílogo. Conócete a ti mismo, otra vez |
| `libro/17-lecturas.md` | Notas y lecturas (bibliografía comentada por capítulo) |

## Versiones compiladas

En `salida/`: PDF maquetado (A5), EPUB, DOCX (para revisar con control de cambios) y un Markdown único.

Para regenerarlas después de editar los capítulos:

```bash
./compilar.sh
```

Requiere `pandoc`; el PDF se genera con Chromium en modo headless.

## Decisiones editoriales

- **De tesis a ensayo.** Se eliminaron la metodología, las entrevistas, los proyectos edDIT y USMOV y los anexos. El libro es puramente filosófico.
- **Voz de autor.** Primera persona, prosa continua, sin "este capítulo tiene por objetivo…", sin resúmenes de cierre repetitivos. Se conservan el origen chileno del autor, su experiencia docente y la mirada desde Cataluña.
- **Notas mínimas.** Las citas literales se limitan a textos clásicos verificables; el resto se parafrasea. La bibliografía va al final, por capítulo.
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
