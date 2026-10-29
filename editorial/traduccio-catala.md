# Traducción al catalán: guía y glosario

Edición catalana de *El alma en la plataforma*: **L'ànima a la plataforma. Escola, dades i llibertat en l'era de les plataformes**. Los capítulos traducidos están en `libro-ca/`, uno por cada archivo de `libro/`.

## Registro

- Catalán normativo (IEC, GIEC), variedad central, de ensayo: culto pero llano, con la misma voz en primera persona del original.
- Traducir el sentido, no las palabras. Nada de calcos del castellano: «cal» y no «hi ha que»; «haver de» y no «tenir que»; «pel que fa a» y no «en quant a»; «a nivell de» solo en sentido literal; «doncs» solo como consecutivo; «ja que», «perquè», «atès que» según convenga; «aleshores» o «llavors»; «en canvi»; «tanmateix» con moderación.
- Mismas normas de estilo que el libro en castellano: sin rayas (—) para incisos, conectores variados, pocas construcciones «no és X sinó Y», sin absolutos que el original no tenga.
- No añadir ni quitar contenido, matices ni cautelas. Si una frase del original es ambigua, conservar la ambigüedad.

## Formato (obligatorio)

- Conservar el Markdown tal cual: encabezados y sus atributos (`{.unnumbered}`, `{#bibliografia}`), pausas `* * *`, cursivas, negritas, listas y número de párrafos.
- Las claves de las notas (`[^c3-kant]`) no se traducen ni se cambian, ni en las llamadas ni en las definiciones.
- Los comentarios HTML (`<!-- ESCENA DEL AUTOR ... -->`) y las URL se copian sin tocar.
- Comillas angulares «» y, dentro, “ ”. Apóstrofo recto (') en el archivo; pandoc lo convierte en tipográfico.
- Números como en el original: «57.000», «35 %», «2,7 millones» → «2,7 milions».

## Citas

- Las citas de obras y de entrevistas se dan en catalán, traducidas del texto castellano del libro. No se cambian autor, año ni localizador.
- Títulos de obras: los clásicos griegos y latinos con su nombre catalán habitual (*Teetet*, *Fedó*, *Fedre*, *Banquet*, *Apologia*, *República*, *Política*, *Ètica nicomaquea*). Las obras modernas conservan el título que aparece en el original, porque es el de la edición citada en la bibliografía.
- El prólogo de la edición catalana avisa, en una frase, de que las citas de obras y entrevistas en otras lenguas se dan en traducción catalana propia cuando no se indica una edición catalana.

## Notas y referencias (APA 7 en catalán)

- En las notas: «y» → «i» entre autores («Miao i Holmes, 2023»); «s. f.» → «s. d.»; «cap.», «p.», «pp.», «trad.», «ed.», «et al.», «ca.» y «a. e. c.» no cambian; «siglo» → «segle»; «véase» → «vegeu»; «Cito la traducción…» → «Cito la traducció…».
- En la lista de referencias solo se traducen los elementos de APA, no los títulos: «(Obra original publicada en 1989)» → «(Obra original publicada el 1989)»; «En J. Varela y F. Álvarez-Uría (Eds.)» → «A J. Varela i F. Álvarez-Uría (Eds.)»; «y» → «i» entre autores; «s. f.» → «s. d.»; fechas «(2020, 17 de agosto)» → «(2020, 17 d'agost)»; «[Nota de prensa]» → «[Nota de premsa]». El orden de las entradas no cambia.
- El glosario se reordena alfabéticamente según los términos catalanes.

## Glosario de traducción

| Castellano | Catalán |
| --- | --- |
| El alma en la plataforma | L'ànima a la plataforma |
| Escuela, datos y libertad en la era de las plataformas | Escola, dades i llibertat en l'era de les plataformes |
| alma | ànima |
| pedagogía de la huella | pedagogia de la petjada |
| huella; dejar huella | petjada; deixar petjada |
| rastro | rastre |
| sello; el sello en la cera | segell; el segell a la cera |
| registro, registrar | registre, registrar |
| evidencia | evidència |
| las cuatro operaciones: tiempo, visibilidad, relación y medida | les quatre operacions: temps, visibilitat, relació i mesura |
| plataforma educativa | plataforma educativa |
| entregar (una tarea); entrega | lliurar; lliurament |
| tarea (en la plataforma o en clase) | tasca |
| deberes (en casa) | deures |
| nota, calificación, calificar | nota, qualificació, qualificar |
| rendimiento, rendir | rendiment, rendir |
| sociedad del rendimiento | societat del rendiment |
| empresario de sí (mismo) | empresari de si mateix |
| capital humano | capital humà |
| dispositivo (Foucault) | dispositiu |
| poder pastoral | poder pastoral |
| contraconducta | contraconducta |
| datificación | datificació |
| analítica del aprendizaje | analítica de l'aprenentatge |
| panel (de seguimiento) | tauler (de seguiment) |
| perfil | perfil |
| algoritmo | algorisme |
| *ranking* | rànquing (sin cursiva) |
| notificación | notificació |
| gamificación | gamificació |
| inteligencia artificial generativa | intel·ligència artificial generativa |
| currículo oculto | currículum ocult |
| cuidado (como valor) | cura |
| privacidad | privacitat |
| deliberación colectiva | deliberació col·lectiva |
| tiempo libre | temps lliure |
| edutropía | edutropia |
| *skholé*, *paideia*, *pharmakon* | *skholé*, *paideia*, *pharmakon* |
| *oikonomía* | *oikonomia* |
| profanar, profanación | profanar, profanació |
| «la Señal» (Hermanos de las Escuelas Cristianas) | «el Senyal» |
| Conócete a ti mismo | Coneix-te a tu mateix |
| escuela | escola |
| colegio (España) / colegio (Chile) | escola / col·legi |
| instituto | institut |
| liceo (Chile) | liceu |
| alumno, estudiante | alumne, estudiant |
| profesor, docente, profesorado | professor, docent, professorat |
| familias | famílies |
| móvil | mòbil |
| informante (entrevistas) | informant |
| imaginemos | imaginem |

### Capítulos

| Castellano | Catalán | Archivo |
| --- | --- | --- |
| Prólogo. Una inquietud | Pròleg. Una inquietud | `00-proleg.md` |
| 1. El sello en la cera | 1. El segell a la cera | `01-el-segell-a-la-cera.md` |
| 2. Una red sin dueño | 2. Una xarxa sense amo | `02-una-xarxa-sense-amo.md` |
| 3. El alma, prisión del cuerpo | 3. L'ànima, presó del cos | `03-lanima-preso-del-cos.md` |
| 4. Escultores de sí mismos | 4. Escultors de si mateixos | `04-escultors-de-si-mateixos.md` |
| 5. Ser visto | 5. Ser vist | `05-ser-vist.md` |
| 6. La memoria fuera de nosotros | 6. La memòria fora de nosaltres | `06-la-memoria-fora-de-nosaltres.md` |
| 7. Lo que no tiene precio | 7. El que no té preu | `07-el-que-no-te-preu.md` |
| 8. Tiempo libre | 8. Temps lliure | `08-temps-lliure.md` |
| Epílogo. Conócete a ti mismo, otra vez | Epíleg. Coneix-te a tu mateix, una altra vegada | `09-epileg.md` |
| Glosario | Glossari | `10-glossari.md` |
| Bibliografía (Lecturas comentadas, Referencias) | Bibliografia (Lectures comentades, Referències) | `11-bibliografia.md` |

### Nombres propios

Plató, Aristòtil, Sòcrates, Diògenes Laerci, Hipàrquia de Maronea, Diotima, Agustí d'Hipona, Isabel de Bohèmia, Pico della Mirandola, Comenius; los autores modernos conservan su nombre (Foucault, Durkheim, Kant, Spinoza, Rousseau, Wollstonecraft, Arendt, Stiegler…). Xile, Santiago, Catalunya, Dinamarca, Anglaterra, Regne Unit.

Chile: Llei d'Inclusió Escolar (2015), Crèdit amb Aval de l'Estat (CAE), deute històric, serveis locals d'educació pública, Sistema d'Admissió Escolar, subvenció escolar preferent, Centre d'Investigació Avançada en Educació (CIAE) de la Universitat de Xile. El Colegio de Profesores conserva su nombre.

Unión Europea: Reglament (UE) 2024/1689, Reglament d'intel·ligència artificial, Reglament general de protecció de dades (RGPD).

## Comprobación

`python3 herramientas/comparar_traduccion.py libro/ARCHIVO.md libro-ca/ARXIU.md` comprueba que la traducción conserva las claves de las notas, los encabezados, las pausas, los comentarios, las URL y el número de párrafos, y que no hay rayas.

## Decisiones añadidas durante la traducción

Para que las correcciones futuras sigan el mismo criterio:

- **Ortografía:** la de la GIEC (2016), sin los acentos diacríticos suprimidos («soc», «dona», «venen»).
- **Autores en notas y referencias:** los clásicos llevan su nombre catalán, igual en la nota y en la lista (Plató, Aristòtil, Ciceró, Agustí d'Hipona, Diògenes Laerci, Comenius). Las leyes e instituciones españolas y chilenas conservan su nombre oficial en castellano cuando son autor de una referencia (Ley 20.370, Constitución Española, Universidad de Chile, Ministerio de Educación de Chile, Comunidad de Madrid); en la prosa van en catalán. Los actos y tribunales de la UE van en catalán en los dos sitios (Reglament (UE) 2024/1689, Decisió d'Execució (UE) 2023/1795, Tribunal de Justícia de la Unió Europea).
- **Títulos:** el informe de la UNESCO de 2023 se da en inglés, que es la edición citada, con la traducción catalana entre paréntesis. El artículo de Ball se cita en catalán en la prosa, como el original lo citaba en castellano, porque la frase siguiente comenta la palabra «ànima».
- **Personajes de Rousseau:** Emili y Sofia (el título de la obra, *Emilio*, es el de la edición citada).
- **Términos:** niños → infants (nen/nena cuando se oponen niños y niñas); dueño → amo; devolver (a la escuela) → retornar; fines → fins; subjetivación → subjectivació; performatividad → performativitat; empleabilidad → ocupabilitat; cuidado de sí → cura de si; ética del cuidado → ètica de la cura; medición → mesurament (para no confundirlo con la «mesura» de las cuatro operaciones); software libre → programari lliure; mercancía → mercaderia; abandono escolar → abandonament escolar; dividuo → dividu; dar clase → fer classe; subir (una tarea) → penjar; pasar asistencia → passar llista; rendición de cuentas → rendició de comptes.
