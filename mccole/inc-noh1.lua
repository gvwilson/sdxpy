--
-- Include a Markdown file, stripping out the H1 header.  This is used to
-- include the content of files like LICENSE.md in Quarto pages.
--

local function include_without_h1(args, kwargs, meta)
  local rel = args[1]
  local f = assert(
    io.open((quarto.project.directory or ".") .. "/" .. rel, "r"),
    "inc-noh1: cannot open " .. rel
  )
  local content = f:read("*all")
  f:close()
  content = content:gsub("^%s*#%s+[^\n]*\n", "", 1)
  content = content:gsub("%]%(@/([%w-]+)/%)", "](../%1/index.qmd)")
  return pandoc.read(content, "markdown").blocks
end

return {
  ["inc-noh1"] = include_without_h1,
}