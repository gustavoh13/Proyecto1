#!/usr/bin/env bash
# Compila el libro en PDF, EPUB, DOCX, HTML y un Markdown único, en castellano
# (libro/) y en catalán (libro-ca/). Sin argumentos compila las dos ediciones;
# «./compilar.sh es» o «./compilar.sh ca» compila solo una.
# En PDF, EPUB y HTML las notas al pie de cada capítulo se convierten en
# notas finales agrupadas por capítulo; el DOCX usa notas al pie de Word.
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p salida
TMP_RAIZ="$(mktemp -d)"
trap 'rm -rf "$TMP_RAIZ"' EXIT
CHROME="${CHROME:-$(command -v chromium || command -v chromium-browser || command -v google-chrome || echo /opt/pw-browsers/chromium)}"
# Las URL escritas en el texto se convierten en enlaces activos
LECTURA=(-f markdown+autolink_bare_uris)

compilar() {
  local LENGUA="$1" SRC NOMBRE NOTAS INDICE IDIOMA PLANTILLA
  case "$LENGUA" in
    es) SRC=libro;    NOMBRE=el-alma-en-la-plataforma; NOTAS="Notas"; INDICE="Índice"; IDIOMA=es-ES ;;
    ca) SRC=libro-ca; NOMBRE=lanima-a-la-plataforma;   NOTAS="Notes"; INDICE="Índex";  IDIOMA=ca-ES ;;
    *) echo "Lengua desconocida: $LENGUA (es, ca)"; exit 1 ;;
  esac
  local TMP="$TMP_RAIZ/$LENGUA"
  mkdir -p "$TMP"
  local CAPITULOS=("$SRC"/0[0-9]-*.md) APENDICES=("$SRC"/1[0-9]-*.md)
  local META="$SRC/metadata.yaml"
  echo "== $NOMBRE ($LENGUA)"

  python3 herramientas/notas_finales.py "$TMP" --titulo "$NOTAS" "${CAPITULOS[@]}"
  local FUENTES=()
  for c in "${CAPITULOS[@]}"; do FUENTES+=("$TMP/$(basename "$c")"); done
  FUENTES+=("$TMP/notas.md" "${APENDICES[@]}")

  # Markdown único para revisar (conserva las notas al pie)
  pandoc "$META" "${CAPITULOS[@]}" "${APENDICES[@]}" -s -t markdown -o "salida/$NOMBRE.md"

  pandoc "$META" "${FUENTES[@]}" "${LECTURA[@]}" \
    --toc --toc-depth=1 --split-level=1 \
    -o "salida/$NOMBRE.epub"

  # DOCX para la editorial: notas al pie nativas de Word (numeración continua)
  # y plantilla de manuscrito (Times New Roman 12, interlineado 1,5, A4)
  if [ "$LENGUA" = es ]; then PLANTILLA=estilos/plantilla.docx; else PLANTILLA="$TMP/plantilla.docx"; fi
  python3 herramientas/plantilla_word.py "$PLANTILLA" "$IDIOMA"
  python3 herramientas/fuentes_docx.py "$TMP/docx" --titulo "$INDICE" "${CAPITULOS[@]}" "${APENDICES[@]}"
  local DOCX=("$TMP/docx/indice.md")
  for c in "${CAPITULOS[@]}" "${APENDICES[@]}"; do DOCX+=("$TMP/docx/$(basename "$c")"); done
  pandoc "$META" "${DOCX[@]}" "${LECTURA[@]}" \
    --reference-doc="$PLANTILLA" \
    -o "salida/$NOMBRE.docx"

  # PDF del manuscrito (A4, el mismo formato que el DOCX), para los formularios
  # de envío que piden PDF. Se convierte una vez con LibreOffice para saber en
  # qué página empieza cada capítulo y otra con esos números en el índice.
  if command -v soffice >/dev/null; then
    local MS="$TMP/manuscrito"
    mkdir -p "$MS"
    cp "salida/$NOMBRE.docx" "$MS/$NOMBRE-manuscrito.docx"
    soffice --headless --convert-to pdf --outdir "$MS" "$MS/$NOMBRE-manuscrito.docx" >/dev/null 2>&1
    python3 herramientas/paginas_pdf.py "$MS/$NOMBRE-manuscrito.pdf" "${CAPITULOS[@]}" "${APENDICES[@]}" > "$MS/paginas.tsv"
    python3 herramientas/fuentes_docx.py "$MS/fuentes" --titulo "$INDICE" --paginas "$MS/paginas.tsv" "${CAPITULOS[@]}" "${APENDICES[@]}"
    local DOCX_MS=("$MS/fuentes/indice.md")
    for c in "${CAPITULOS[@]}" "${APENDICES[@]}"; do DOCX_MS+=("$MS/fuentes/$(basename "$c")"); done
    pandoc "$META" "${DOCX_MS[@]}" "${LECTURA[@]}" \
      --reference-doc="$PLANTILLA" \
      -o "$MS/$NOMBRE-manuscrito.docx"
    soffice --headless --convert-to pdf --outdir "$MS" "$MS/$NOMBRE-manuscrito.docx" >/dev/null 2>&1
    python3 herramientas/paginas_pdf.py "$MS/$NOMBRE-manuscrito.pdf" "${CAPITULOS[@]}" "${APENDICES[@]}" \
      | cmp -s - "$MS/paginas.tsv" || echo "Aviso: la paginación del manuscrito cambió al añadir los números al índice."
    cp "$MS/$NOMBRE-manuscrito.pdf" salida/
  else
    echo "Aviso: sin LibreOffice (soffice) no se genera el PDF del manuscrito."
  fi

  # PDF. Chromium no parte palabras en español ni en catalán: si una línea
  # justificada queda estirada, se añade partición a la palabra que no cupo
  # y se repite.
  pandoc "$META" "${FUENTES[@]}" "${LECTURA[@]}" \
    -s --toc --toc-depth=1 --embed-resources --section-divs \
    --css estilos/libro.css --lua-filter estilos/cortes-url.lua \
    -o "$TMP/libro.html"
  : > "$TMP/particion.tsv"
  local intento NUEVAS
  for intento in 1 2 3 4 5 6; do
    cp "$TMP/libro.html" "salida/$NOMBRE.html"
    python3 herramientas/guionado.py "salida/$NOMBRE.html" "$TMP/particion.tsv" "$LENGUA"
    "$CHROME" --headless --no-sandbox --disable-gpu --no-pdf-header-footer \
      --print-to-pdf="$PWD/salida/$NOMBRE.pdf" \
      "file://$PWD/salida/$NOMBRE.html" 2>/dev/null
    NUEVAS="$(python3 herramientas/lineas_estiradas.py "salida/$NOMBRE.pdf")"
    [ -z "$NUEVAS" ] && break
    echo "Líneas estiradas en la pasada $intento: $(echo "$NUEVAS" | wc -l)"
    echo "$NUEVAS" >> "$TMP/particion.tsv"
  done
  # Chromium sitúa los destinos de los enlaces internos sin contar los márgenes
  python3 herramientas/destinos_pdf.py "salida/$NOMBRE.pdf" estilos/libro.css
}

LENGUAS=("$@")
if [ ${#LENGUAS[@]} -eq 0 ]; then
  LENGUAS=(es)
  [ -f libro-ca/metadata.yaml ] && ls libro-ca/0[0-9]-*.md >/dev/null 2>&1 && LENGUAS+=(ca)
fi
for l in "${LENGUAS[@]}"; do compilar "$l"; done
echo "Listo: $(ls salida | tr '\n' ' ')"
