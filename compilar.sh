#!/usr/bin/env bash
# Compila el manuscrito de libro/ en EPUB, HTML y PDF dentro de salida/.
# Requiere pandoc; para el PDF usa Chromium en modo headless.
set -euo pipefail

cd "$(dirname "$0")"
mkdir -p salida

CAPITULOS=(libro/[0-9][0-9]-*.md)
CHROME="${CHROME:-$(command -v chromium || command -v chromium-browser || command -v google-chrome || echo /opt/pw-browsers/chromium)}"

# Manuscrito único en Markdown (útil para enviar a editoriales)
pandoc libro/metadata.yaml "${CAPITULOS[@]}" -s -t markdown -o salida/el-alma-en-la-plataforma.md

# EPUB
pandoc libro/metadata.yaml "${CAPITULOS[@]}" \
  --toc --toc-depth=1 --split-level=1 --reference-location=section \
  -o salida/el-alma-en-la-plataforma.epub

# DOCX (para revisión con control de cambios)
pandoc libro/metadata.yaml "${CAPITULOS[@]}" \
  --toc --toc-depth=1 \
  -o salida/el-alma-en-la-plataforma.docx

# HTML maquetado para impresión
pandoc libro/metadata.yaml "${CAPITULOS[@]}" \
  -s --toc --toc-depth=1 --embed-resources \
  --section-divs --reference-location=section \
  --css estilos/libro.css \
  -o salida/el-alma-en-la-plataforma.html

# PDF a partir del HTML
"$CHROME" --headless --no-sandbox --disable-gpu --no-pdf-header-footer \
  --print-to-pdf="$PWD/salida/el-alma-en-la-plataforma.pdf" \
  "file://$PWD/salida/el-alma-en-la-plataforma.html" 2>/dev/null

echo "Listo: $(ls salida)"
