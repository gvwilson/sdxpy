--
-- Glossary reference shortcode.
-- Usage: {{< g key "display text" >}}
-- If the display text is omitted the key itself is used.
--

local function glossary_ref(args, kwargs, meta)
  local key = pandoc.utils.stringify(args[1])
  local text = args[2] or args[1]
  return pandoc.Link(text, "../glossary/index.html#" .. key)
end

return {
  ["g"] = glossary_ref,
}
