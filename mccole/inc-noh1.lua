-- inc-noh1.lua
-- A shortcode like Quarto's {{< include >}}, but it strips the first level-1
-- heading from the included file (so the including chapter supplies its own
-- title). The included file is otherwise standalone Markdown; the only extra
-- rewrite needed is the internal book link @/slug/ -> ../slug/index.qmd.
-- Include paths are resolved relative to the project root (like _bin/links.lua)
-- because quarto.doc.input_file does not point at the chapter during book PDF
-- renders, which merge all chapters into a single document.

return {
  ["inc-noh1"] = function(args, kwargs, meta)
    local rel = args[1]
    local f = assert(io.open((quarto.project.directory or ".") .. "/" .. rel, "r"), "inc-noh1: cannot open " .. rel)
    local content = f:read("*all")
    f:close()
    content = content:gsub("^%s*#%s+[^\n]*\n", "", 1)
    content = content:gsub("%]%(@/([%w-]+)/%)", "](../%1/index.qmd)")
    return pandoc.read(content, "markdown").blocks
  end
}