-- nav.lua
-- Read chapters and appendices from _quarto.yml and expose them to the
-- HTML template as "chapters" and "appendices" (raw HTML nav lists),
-- "home" (a page-relative path to the site index), and "heading" (the
-- current page's title, used for the <title> element). The page heading
-- is also prepended to the document body as a raw H1 so it renders above
-- the content. Links are prefixed with "../" for pages nested a directory
-- deep, so they resolve without JavaScript.

local function read_file(path)
  local f = io.open(path, "r")
  if not f then return nil end
  local content = f:read("*a")
  f:close()
  return content
end

-- Collect the `- <path>` entries under `key:` (a list indented below the
-- key). Stops at the first non-list, non-blank line at or above the key's
-- indentation. Good enough for the simple `book: chapters:/appendices:`
-- lists this template uses.
local function extract_list(yaml, key)
  local result = {}
  local lines = {}
  for line in (yaml .. "\n"):gmatch("(.-)\n") do
    table.insert(lines, line)
  end
  for i, line in ipairs(lines) do
    local indent = line:match("^(%s*)" .. key .. ":%s*$")
    if indent then
      for j = i + 1, #lines do
        local l = lines[j]
        local path = l:match("^%s*%-%s*(%S+)%s*$")
        if path then
          table.insert(result, path)
        elseif not l:match("^%s*$") then
          local lindent = l:match("^(%s*)")
          if #lindent <= #indent then
            break
          end
        end
      end
    end
  end
  return result
end

-- Title of a chapter: its first level-1 heading, attributes stripped.
local function chapter_title(project_dir, path)
  local content = read_file(project_dir .. "/" .. path)
  if not content then return path end
  for line in (content .. "\n"):gmatch("(.-)\n") do
    local title = line:match("^#%s+(.-)%s*$")
    if title then
      return title:gsub("%s*%{.*%}%s*$", "")
    end
  end
  return path
end

local function book_title(yaml)
  local t = yaml:match('title:%s*"([^"]*)"')
  if t then return t end
  t = yaml:match("title:%s*'([^']*)'")
  if t then return t end
  return yaml:match("title:%s*(%S+)") or "Home"
end

local function build_list(project_dir, paths, prefix)
  local items = {}
  for _, path in ipairs(paths) do
    local href = prefix .. path:gsub("%.qmd$", ".html")
    local title = chapter_title(project_dir, path)
    table.insert(items, string.format('<li><a href="%s">%s</a></li>', href, title))
  end
  return '<ul class="topnav-list">' .. table.concat(items) .. '</ul>'
end

function Pandoc(doc)
  local project_dir = quarto.project.directory or "."
  local input = "index.qmd"
  if quarto.doc and quarto.doc.input_file then
    input = quarto.doc.input_file
  end

  -- input_file is absolute; reduce to a project-relative path so its
  -- directory depth is the number of "../" needed to reach the site root.
  local dir = project_dir:gsub("/+$", "")
  local rel = input
  if dir ~= "." and rel:sub(1, #dir) == dir then
    rel = rel:sub(#dir + 1)
  end
  rel = rel:gsub("^/+", "")

  local _, slash_count = rel:gsub("/", "")
  local prefix = string.rep("../", slash_count)

  local yaml = read_file(project_dir .. "/_quarto.yml")
  if yaml then
    local chapters = extract_list(yaml, "chapters")
    local appendices = extract_list(yaml, "appendices")

    -- The home page (index.qmd) is the "Home" link, so drop it from Chapters.
    local menu_chapters = {}
    for _, c in ipairs(chapters) do
      if c ~= "index.qmd" then
        table.insert(menu_chapters, c)
      end
    end

    local heading
    if rel == "index.qmd" then
      heading = book_title(yaml)
    else
      heading = chapter_title(project_dir, rel)
    end

    doc.meta.home = prefix .. "index.html"
    doc.meta.heading = heading
    doc.meta.chapters = pandoc.RawBlock("html", build_list(project_dir, menu_chapters, prefix))
    doc.meta.appendices = pandoc.RawBlock("html", build_list(project_dir, appendices, prefix))

    table.insert(doc.blocks, 1, pandoc.RawBlock("html", '<h1 class="title">' .. heading .. '</h1>'))
  end
  return doc
end
