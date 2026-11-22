-- publish.lua
-- Copy a rendered Quarto book into a shared site tree. The shared tree
-- keeps the Quarto scaffolding (site_libs, assets) under a consolidated
-- '../mccole/' directory one level above the book, so this script rewrites
-- every reference to those directories accordingly.
--
-- Usage: pandoc lua mccole/publish.lua SOURCE DESTINATION [SNIPPET]
--   SOURCE      directory of rendered HTML (e.g. 'docs')
--   DESTINATION directory to write into (e.g. '~/third/docs/change')
--   SNIPPET     optional path to an HTML fragment inserted as the last
--               element inside each page's <head>

local script_dir = arg[0] and arg[0]:match("^(.*)/") or "."
package.path = script_dir .. "/?.lua;" .. package.path

local utils = require("utils")
utils.program = "publish.lua"

-- Join two path components with a single slash.
local function join(base, name)
  return base .. "/" .. name
end

-- True if path is an existing directory. list_directory errors on files and
-- on non-existent paths, so a successful call is exactly the check we want.
local function is_dir(path)
  return pcall(pandoc.system.list_directory, path)
end

-- Write a string to a file.
local function write_file(path, content)
  local f = io.open(path, "wb")
  if not f then
    utils.fail("cannot write " .. path)
  end
  f:write(content)
  f:close()
end

-- Rewrite a src="..." or href="..." attribute value so that it points at
-- the shared '../mccole/' tree. Replacing the bare directory name also
-- handles nested references.
local function relocate(value)
  value = value:gsub("mccole", "../mccole")
  value = value:gsub("site_libs", "../mccole/site_libs")
  return value
end

-- Rewrite every src and href attribute in the whole document in one pass.
local function rewrite_references(content)
  content = content:gsub('src="[^"]*"', relocate)
  content = content:gsub('href="[^"]*"', relocate)
  return content
end

-- Insert the snippet as the last element inside <head>.
local function insert_snippet(content, snippet)
  return content:gsub("</head>", snippet .. "\n</head>", 1)
end

-- True if the path names an HTML file.
local function is_html(path)
  return path:lower():match("%.html$") ~= nil
end

-- Copy one file, transforming it if it is HTML.
local function copy_one(src, dst, snippet)
  if is_html(src) then
    local content = utils.read_file(src)
    content = rewrite_references(content)
    if snippet then
      content = insert_snippet(content, snippet)
    end
    write_file(dst, content)
  else
    pandoc.system.copy(src, dst)
  end
end

-- Recursively copy a directory, skipping 'assets', 'site_libs', and '.nojekyll'.
local function copy_tree(src_dir, dst_dir, snippet)
  local names = pandoc.system.list_directory(src_dir)
  table.sort(names)
  for _, name in ipairs(names) do
    if name ~= "mccole" and name ~= "site_libs" then
      local src = join(src_dir, name)
      local dst = join(dst_dir, name)
      if is_dir(src) then
        pandoc.system.make_directory(dst, false)
        copy_tree(src, dst, snippet)
      elseif name ~= ".nojekyll" then
        copy_one(src, dst, snippet)
      end
    end
  end
end

if #arg < 2 or #arg > 3 then
  utils.fail("usage: publish.lua SOURCE DESTINATION [SNIPPET]")
end

local source = (arg[1]):gsub("/+$", "")
local dest = (arg[2]):gsub("/+$", "")

local snippet = nil
if arg[3] then
  snippet = utils.read_file(arg[3])
  snippet = snippet:gsub("%s+$", "")
end

-- Remove any previous copy, then rebuild the destination directory.
if is_dir(dest) then
  pandoc.system.remove_directory(dest, true)
end
pandoc.system.make_directory(dest, true)

copy_tree(source, dest, snippet)
