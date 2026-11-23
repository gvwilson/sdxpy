-- Code include shortcode.
--
-- Usage: {{< inc path/to/file.py mark=name omit=name head="N" >}}
-- Reads a file (relative to the project root) and emits a syntax-highlighted
-- code block. With mark=, only the "# mccole:name ... # mccole:/name" region
-- is emitted; omit= removes a marked region; head= keeps the first N lines.

local root = quarto.project.directory or "."

local function s(v)
  if type(v) == "string" and v ~= "" then return v end
end

local LANG = { py = "python", sh = "bash" }

local function extract_region(content, mark)
  return content:match("# mccole:" .. mark .. "\n(.-)\n# mccole:/" .. mark) or ""
end

local function omit_region(content, mark)
  return content:gsub("# mccole:" .. mark .. "\n.-# mccole:/" .. mark .. "\n", "")
end

local function head_lines(content, n)
  local lines = {}
  for line in content:gmatch("([^\n]*)\n") do
    lines[#lines + 1] = line
    if #lines == n then break end
  end
  return table.concat(lines, "\n")
end

local function scrub_code(content)
  local out = {}
  for line in (content .. "\n"):gmatch("(.-)\n") do
    local s = line
    s = s:gsub("%s*#%s*BUG[^\n]*", "")            -- Python/shell: # BUG …
    s = s:gsub("%s*//%s*BUG[^\n]*", "")           -- JavaScript:   // BUG …
    s = s:gsub("<!%-%-%s*BUG.-%-%->", "")         -- HTML:         <!-- BUG … -->
    s = s:gsub("/%*%s*BUG.-%*/", "")              -- CSS:          /* BUG … */
    if s:match("^%s*%-%-.*BUG") then s = "" end   -- SQL:          -- … BUG …
    if s:match("%S") then
      out[#out + 1] = s
    end
  end
  return table.concat(out, "\n")
end

return {
  ["inc"] = function(args, kwargs, meta)
    local file = s(args[1])
    local mark = s(kwargs["mark"])
    local omit = s(kwargs["omit"])
    local head = tonumber(s(kwargs["head"]) or "")
    local f = assert(io.open(root .. "/" .. file, "r"), "inc: cannot open " .. file)
    local content = f:read("*all")
    f:close()
    local code = mark and extract_region(content, mark) or content
    if omit then code = omit_region(code, omit) end
    if head then code = head_lines(code, head) end
    code = scrub_code(code)
    local ext = file:match("%.([^.]+)$") or ""
    local lang = LANG[ext] or ""
    local classes = (lang ~= "") and { lang } or {}
    return pandoc.Blocks({ pandoc.CodeBlock(code, pandoc.Attr("", classes, {})) })
  end,
}
