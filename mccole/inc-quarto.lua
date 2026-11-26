--
-- Expand {{< inc ... >}} shortcodes in Quarto pages.
--

local dir = quarto.project.directory or "."
local U = dofile(dir .. "/mccole/inc-utils.lua")

local function include_code(args, kwargs, meta)
  local file = U.s(args[1])
  local mark = U.s(kwargs["mark"])
  local omit = U.s(kwargs["omit"])
  local head = tonumber(U.s(kwargs["head"]) or "")
  local f = assert(io.open(dir .. "/" .. file, "r"), "inc: cannot open " .. file)
  local content = f:read("*all")
  f:close()
  local code = mark and U.extract_region(content, mark) or content
  if omit then code = U.omit_region(code, omit) end
  if head then code = U.head_lines(code, head) end
  code = U.scrub_code(code)
  local ext = file:match("%.([^.]+)$") or ""
  local lang = U.LANG[ext] or ""
  local classes = (lang ~= "") and { lang } or {}
  return pandoc.Blocks({ pandoc.CodeBlock(code, pandoc.Attr("", classes, { ["data-file"] = file })) })
end

return {
  ["inc"] = include_code,
}
