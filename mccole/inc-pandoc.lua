-- inc-pandoc.lua — expand {{< inc ... >}} shortcodes in pandoc (slides).
-- Shared helpers live in inc-utils.lua.

local dir = pandoc.path.directory(PANDOC_SCRIPT_FILE)
local U = dofile(pandoc.path.join({dir, "inc-utils.lua"}))

local function parse_inc(text)
  local inner = text:match("^{{%s*<%s*inc%s+(.-)%s*>}}$")
  if not inner then return nil end
  local file, rest = inner:match("^(%S+)%s*(.-)$")
  if not file then return nil end
  local kwargs = {}
  for k, v in rest:gmatch("([%w-]+)=([^%s]+)") do
    kwargs[k] = v:gsub("^[\"']", ""):gsub("[\"']$", "")
  end
  return file, kwargs
end

function Para(el)
  local text = pandoc.utils.stringify(el)
  local file, kwargs = parse_inc(text)
  if not file then return nil end

  local mark = U.s(kwargs["mark"])
  local omit = U.s(kwargs["omit"])
  local head = tonumber(U.s(kwargs["head"]) or "")

  local f = assert(io.open(file, "r"), "inc: cannot open " .. file)
  local content = f:read("*all")
  f:close()

  local code = mark and U.extract_region(content, mark) or content
  if omit then code = U.omit_region(code, omit) end
  if head then code = U.head_lines(code, head) end
  code = U.scrub_code(code)

  local ext = file:match("%.([^.]+)$") or ""
  local lang = U.LANG[ext] or ""
  local classes = (lang ~= "") and { lang } or {}

  return pandoc.CodeBlock(code, pandoc.Attr("", classes, {}))
end
