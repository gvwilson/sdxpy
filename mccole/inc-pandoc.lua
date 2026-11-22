-- inc-pandoc.lua: expand fenced code blocks with class "include".
--
-- Example:
--     ```{.include}
--     _dependencies.qmd
--     _project_audit.qmd
--     ```
--
-- Each filename is resolved relative to the file that contains the block,
-- so a bare name like `_dependencies.qmd` next to `health/slides.qmd`
-- resolves to `health/_dependencies.qmd`. Includes are not recursive.

local function read_file(filename)
  local f, err = io.open(filename, "r")
  if not f then
    error("include: cannot open '" .. filename .. "': " .. err)
  end

  local text = f:read("*a")
  f:close()
  return text
end

local function trim(s)
  return s:match("^%s*(.-)%s*$")
end

local function resolve_path(filename)
  if pandoc.path.is_absolute(filename) then
    return filename
  end

  local input = PANDOC_STATE.input_files
  if not input or #input == 0 then
    return filename
  end

  return pandoc.path.join({pandoc.path.directory(input[1]), filename})
end

function CodeBlock(el)
  if not el.classes:includes("include") then
    return nil
  end

  local blocks = pandoc.List()
  for filename in el.text:gmatch("[^\r\n]+") do
    filename = trim(filename)
    if filename ~= "" then
      local path = resolve_path(filename)
      local doc = pandoc.read(read_file(path), "markdown")
      blocks:extend(doc.blocks)
    end
  end
  return blocks
end
