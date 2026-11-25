--
-- FIXME note shortcode.
-- Renders a bold "FIXME:" label followed by the given text.
-- Usage: {{< fixme "text" >}}
--

local function s(v)
  if type(v) == "string" and v ~= "" then return v end
end

local function fixme(args, kwargs, meta)
  local text = s(args[1]) or "FIXME"
  return pandoc.Inlines({ pandoc.Strong({ pandoc.Str("FIXME: ") }), pandoc.Str(text) })
end

return {
  ["fixme"] = fixme,
}
