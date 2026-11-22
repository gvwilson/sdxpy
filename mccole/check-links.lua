-- check-links.lua
-- Check that "@key" links in Markdown files match definitions in a links file.
--
-- Usage: lua check-links.lua LINKS_FILE MARKDOWN_FILE...
--
-- The links file contains one definition per line:
--   [link-key]: url
-- Markdown files use those definitions as:
--   [text](@link-key)
--
-- The script reports links that are used but not defined (along with the file
-- that uses each one) and links that are defined but not used. It exits with
-- a non-zero status if either report is non-empty.

local script_dir = arg[0] and arg[0]:match("^(.*)/") or "."
package.path = script_dir .. "/?.lua;" .. package.path

local utils = require("utils")
utils.program = "check-links.lua"

-- Returns the defined keys in file order, and a set of those keys.
local function read_links_file(path)
  local order = {}
  local set = {}
  for key in (utils.read_file(path)):gmatch("%[([%w-]+)%]:%s*%S+") do
    order[#order + 1] = key
    set[key] = true
  end
  return order, set
end

-- Records every "@key" link in content as used in path.
local function add_used_links(content, path, set, files)
  for key in content:gmatch("%]%(@([%w-]+)%)") do
    set[key] = true
    files[key] = files[key] or {}
    files[key][path] = true
  end
end

-- Returns a set of used keys and a map of each key to the files using it.
local function read_markdown_files(paths)
  local set = {}
  local files = {}
  for _, path in ipairs(paths) do
    add_used_links(utils.read_file(path), path, set, files)
  end
  return set, files
end

if #arg < 2 then
  utils.fail("usage: lua check-links.lua LINKS_FILE MARKDOWN_FILE...")
end

local defined_order, defined_set = read_links_file(arg[1])

local markdown_files = {}
for i = 2, #arg do
  markdown_files[#markdown_files + 1] = arg[i]
end
local used_set, used_files = read_markdown_files(markdown_files)

local problems = false
if utils.report_missing(defined_set, used_files, "used but not defined:") then
  problems = true
end
if utils.report_unused(defined_order, used_set, "defined but not used:") then
  problems = true
end

if problems then
  os.exit(1)
end
