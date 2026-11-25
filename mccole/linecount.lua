--
-- Count lines in a file inclusion.
-- Usage: {{< linecount path/to/file >}}
--

local root = quarto.project.directory or "."

local function s(v)
  if type(v) == "string" and v ~= "" then return v end
end

local function line_count(args, kwargs, meta)
  local file = s(args[1])
  local f = assert(io.open(root .. "/" .. file, "r"), "linecount: cannot open " .. file)
  local n = 0
  for _ in f:lines() do n = n + 1 end
  f:close()
  return pandoc.Str(tostring(n))
end

return {
  ["linecount"] = line_count,
}
