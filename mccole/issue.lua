-- Issue reference shortcode.
--
-- Usage: {{< issue 123 >}}
-- Renders a link to the issue in the book's repository.

local function s(v)
  if type(v) == "string" and v ~= "" then return v end
end

return {
  ["issue"] = function(args, kwargs, meta)
    local n = s(args[1])
    local repo = meta["book"] and meta["book"]["repo-url"] and pandoc.utils.stringify(meta["book"]["repo-url"]) or ""
    return pandoc.Link(pandoc.Str("#" .. n), repo .. "/issues/" .. n)
  end,
}
