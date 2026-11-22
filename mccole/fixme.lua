-- FIXME note shortcode.
--
-- Usage: {{< fixme "text" >}}
-- Renders a bold "FIXME:" label followed by the given text.

local function s(v)
  if type(v) == "string" and v ~= "" then return v end
end

return {
  ["fixme"] = function(args, kwargs, meta)
    local text = s(args[1]) or "FIXME"
    return pandoc.Inlines({ pandoc.Strong({ pandoc.Str("FIXME: ") }), pandoc.Str(text) })
  end,
}
