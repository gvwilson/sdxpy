-- Index entry shortcode.
--
-- Usage: {{< i "display" "term" url="..." >}}
-- Renders the display text; the index term is a no-op for now.

return {
  ["i"] = function(args, kwargs, meta)
    local display = args[2] or args[1]
    if display == nil then return pandoc.Str("") end
    return pandoc.Str(display)
  end,
}
