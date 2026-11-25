--
-- Index entry shortcode.
-- Usage: {{< i "display" "term" url="..." >}}
--

local function index_entry(args, kwargs, meta)
  local display = args[2] or args[1]
  if display == nil then return pandoc.Str("") end
  return pandoc.Str(display)
end

return {
  ["i"] = index_entry,
}
