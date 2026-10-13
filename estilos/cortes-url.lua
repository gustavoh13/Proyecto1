-- Puntos de corte en las URL que se muestran como texto (HTML y PDF).
-- Siguen la pauta habitual de las bibliografías: se corta después de «//»
-- y de «/», y antes de «.», «-», «_», «?», «#», «=», «&» y «~», nunca en
-- mitad de una palabra ni de un número. El guion queda unido al carácter
-- siguiente para que no termine una línea y parezca un guion de partición.
-- El enlace y el texto que se copia no cambian.

local function escapar(s)
  return (s:gsub("&", "&amp;"):gsub("<", "&lt;"):gsub(">", "&gt;"))
end

function Link(el)
  if not FORMAT:match("html") then return nil end
  local url = pandoc.utils.stringify(el.content)
  if url ~= el.target or #url < 30 then return nil end
  local partes, i = {}, 1
  while i <= #url do
    local c = url:sub(i, i)
    if url:sub(i, i + 1) == "//" then
      table.insert(partes, "//<wbr/>")
      i = i + 2
    elseif c == "/" then
      table.insert(partes, "/<wbr/>")
      i = i + 1
    elseif c == "-" and i < #url then
      table.insert(partes, '<wbr/><span class="sin-corte">-' .. escapar(url:sub(i + 1, i + 1)) .. "</span>")
      i = i + 2
    elseif c:match("[%._%?#=&~]") and i > 1 then
      table.insert(partes, "<wbr/>" .. escapar(c))
      i = i + 1
    else
      table.insert(partes, escapar(c))
      i = i + 1
    end
  end
  el.content = { pandoc.RawInline("html", table.concat(partes)) }
  return el
end
