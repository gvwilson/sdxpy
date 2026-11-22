-- Line-count shortcode.
--
-- Usage: {{< linecount path/to/file >}}
-- Counts the lines in a file (relative to the project root) and emits the number.

local root = quarto.project.directory or "."

local function s(v)
  if type(v) == "string" and v ~= "" then return v end
end

return {
  ["linecount"] = function(args, kwargs, meta)
    local file = s(args[1])
    local f = assert(io.open(root .. "/" .. file, "r"), "linecount: cannot open " .. file)
    local n = 0
    for _ in f:lines() do n = n + 1 end
    f:close()
    return pandoc.Str(tostring(n))
  end,
}
