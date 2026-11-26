-- forma.lua
-- Inject the forma widget module and stylesheet when the project opts in with
-- `include-forma: true` in _quarto.yml. Quarto does not rewrite local
-- href/src in header-includes, so the paths carry a "../" prefix computed from
-- the input file's depth (same idiom as nav.lua).

local function read_file(path)
  local f = io.open(path, "r")
  if not f then return nil end
  local content = f:read("*a")
  f:close()
  return content
end

function Pandoc(doc)
  local project_dir = quarto.project.directory or "."
  local yaml = read_file(project_dir .. "/_quarto.yml") or ""
  if not yaml:match("include%-forma:%s*true") then
    return doc
  end

  local input = "index.qmd"
  if quarto.doc and quarto.doc.input_file then
    input = quarto.doc.input_file
  end

  -- Reduce the absolute input path to project-relative; its slash count is
  -- the number of "../" needed to reach the site root.
  local dir = project_dir:gsub("/+$", "")
  local rel = input
  if dir ~= "." and rel:sub(1, #dir) == dir then
    rel = rel:sub(#dir + 1)
  end
  rel = rel:gsub("^/+", "")
  local _, slash_count = rel:gsub("/", "")
  local prefix = string.rep("../", slash_count)

  doc.meta["header-includes"] = pandoc.MetaBlocks({
    pandoc.RawBlock("html", string.format('<link rel="stylesheet" href="%smccole/mccole-forma.css">', prefix)),
    pandoc.RawBlock("html", string.format('<script type="module" src="%smccole/forma.js"></script>', prefix)),
  })
  return doc
end
