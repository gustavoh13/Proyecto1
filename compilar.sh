#!/usr/bin/env bash
# Compila el libro en PDF, EPUB, DOCX, HTML y un Markdown único.
# Las notas al pie de cada capítulo se convierten en notas finales,
# agrupadas por capítulo, antes del glosario y la bibliografía.
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p salida
CAPITULOS=(libro/0[0-9]-*.md)
APENDICES=(libro/1[0-9]-*.md)
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
CHROME="${CHROME:-$(command -v chromium || command -v chromium-browser || command -v google-chrome || echo /opt/pw-browsers/chromium)}"

python3 herramientas/notas_finales.py "$TMP" "${CAPITULOS[@]}"
FUENTES=()
for c in "${CAPITULOS[@]}"; do FUENTES+=("$TMP/$(basename "$c")"); done
FUENTES+=("$TMP/notas.md" "${APENDICES[@]}")

# Markdown único para revisar (conserva las notas al pie)
pandoc libro/metadata.yaml "${CAPITULOS[@]}" "${APENDICES[@]}" -s -t markdown -o salida/el-alma-en-la-plataforma.md

pandoc libro/metadata.yaml "${FUENTES[@]}" \
  --toc --toc-depth=1 --split-level=1 \
  -o salida/el-alma-en-la-plataforma.epub

pandoc libro/metadata.yaml "${FUENTES[@]}" \
  --toc --toc-depth=1 \
  -o salida/el-alma-en-la-plataforma.docx

pandoc libro/metadata.yaml "${FUENTES[@]}" \
  -s --toc --toc-depth=1 --embed-resources --section-divs \
  --css estilos/libro.css \
  -o salida/el-alma-en-la-plataforma.html

"$CHROME" --headless --no-sandbox --disable-gpu --no-pdf-header-footer \
  --print-to-pdf="$PWD/salida/el-alma-en-la-plataforma.pdf" \
  "file://$PWD/salida/el-alma-en-la-plataforma.html" 2>/dev/null

echo "Listo: $(ls salida)"
