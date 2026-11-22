-- shortcodes.lua
-- Handlers for the book's {{< ... >}} shortcodes: i, inc, issue, and fixme.
-- (The glossary {{< g >}} shortcode lives in glossary.lua.)

local root = quarto.project.directory or "."

-- Shortcode args arrive as strings; a missing named arg is an empty string.
local function s(v)
  if type(v) == "string" and v ~= "" then return v end
end

local LANG = { py = "python", sh = "bash" }

-- The "mark" identifiers are simple [a-z_]+ names, so they need no pattern escaping.
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

return {
  -- index entry (no-op for now): {{< i "display" "term" url="..." >}}
  ["i"] = function(args, kwargs, meta)
    local display = args[2] or args[1]
    if display == nil then return pandoc.Str("") end
    return pandoc.Str(display)
  end,

  -- code include: {{< inc path/to/file.py mark=name omit=name head="N" >}}
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
    local ext = file:match("%.([^.]+)$") or ""
    local lang = LANG[ext] or ""
    local classes = (lang ~= "") and { lang } or {}
    return pandoc.Blocks({ pandoc.CodeBlock(code, pandoc.Attr("", classes, {})) })
  end,

  -- issue reference: {{< issue 123 >}}
  ["issue"] = function(args, kwargs, meta)
    local n = s(args[1])
    return pandoc.Link(pandoc.Str("#" .. n), "https://github.com/gvwilson/sdxpy/issues/" .. n)
  end,

  -- fixme note: {{< fixme "text" >}}
  ["fixme"] = function(args, kwargs, meta)
    local text = s(args[1]) or "FIXME"
    return pandoc.Inlines({ pandoc.Strong({ pandoc.Str("FIXME: ") }), pandoc.Str(text) })
  end,
}
