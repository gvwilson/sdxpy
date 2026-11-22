-- check-bib.lua
-- Check that citation keys in Quarto Markdown files match entries in a
-- BibTeX file.
--
-- Usage: lua check-bib.lua BIB_FILE MARKDOWN_FILE...
--
-- The BibTeX file contains one entry per line that starts with:
--   @type{key
-- Markdown files cite those entries as:
--   [@key]
--   [@key1; @key2; @key3]
--
-- The script reports keys that are cited but not defined (along with the file
-- that cites each one) and keys that are defined but not cited. It exits with
-- a non-zero status if either report is non-empty.

local script_dir = arg[0] and arg[0]:match("^(.*)/") or "."
package.path = script_dir .. "/?.lua;" .. package.path

local utils = require("utils")
utils.program = "check-bib.lua"

-- Returns the defined keys in file order, and a set of those keys.
local function read_bib_file(path)
  local order = {}
  local set = {}
  for key in (utils.read_file(path)):gmatch("@%a+%s*{%s*([^,%s]+)") do
    order[#order + 1] = key
    set[key] = true
  end
  return order, set
end

-- Records every "@key" citation in content as cited in path.
local function add_cited_keys(content, path, set, files)
  for bracket in content:gmatch("%[([^%]]*)%]") do
    for key in bracket:gmatch("@([%w-]+)") do
      set[key] = true
      files[key] = files[key] or {}
      files[key][path] = true
    end
  end
end

-- Returns a set of cited keys and a map of each key to the files citing it.
local function read_markdown_files(paths)
  local set = {}
  local files = {}
  for _, path in ipairs(paths) do
    add_cited_keys(utils.read_file(path), path, set, files)
  end
  return set, files
end

if #arg < 2 then
  utils.fail("usage: lua check-bib.lua BIB_FILE MARKDOWN_FILE...")
end

local defined_order, defined_set = read_bib_file(arg[1])

local markdown_files = {}
for i = 2, #arg do
  markdown_files[#markdown_files + 1] = arg[i]
end
local cited_set, cited_files = read_markdown_files(markdown_files)

local problems = false
if utils.report_missing(defined_set, cited_files, "cited but not defined:") then
  problems = true
end
if utils.report_unused(defined_order, cited_set, "defined but not cited:") then
  problems = true
end

if problems then
  os.exit(1)
end
