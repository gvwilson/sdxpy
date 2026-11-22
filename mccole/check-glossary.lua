-- check-glossary.lua
-- Check that glossary shortcode references in Markdown files match entries
-- in a glossary file.
--
-- Usage: lua check-glossary.lua GLOSSARY_FILE MARKDOWN_FILE...
--
-- The glossary file defines one entry per line as a span with an id:
--   <span id="key">display text</span>
-- Markdown files reference those entries with the shortcode:
--   {{<g key "display text" >}}
--
-- The script reports keys that are used but not defined (along with the file
-- that uses each one), keys that are defined but not used, and entries whose
-- display text is out of alphabetical order. It also reports keys that are
-- referred to more than once (along with the files they occur in). It exits
-- with a non-zero status if any report is non-empty.

local script_dir = arg[0] and arg[0]:match("^(.*)/") or "."
package.path = script_dir .. "/?.lua;" .. package.path

local utils = require("utils")
utils.program = "check-glossary.lua"

-- Returns the defined keys in file order, a set of those keys, and the
-- display text of each entry in file order.
local function read_glossary_file(path)
  local order = {}
  local set = {}
  local texts = {}
  for key, text in (utils.read_file(path)):gmatch('<span id="([%w_-]+)">([^<]*)</span>') do
    order[#order + 1] = key
    set[key] = true
    texts[#texts + 1] = text
  end
  return order, set, texts
end

-- Records every glossary key referenced by a "g" shortcode in content.
local function add_used_keys(content, path, set, files)
  for key in content:gmatch("{{<%s*g%s+([%w_-]+)") do
    set[key] = true
    files[key] = files[key] or {}
    files[key][path] = (files[key][path] or 0) + 1
  end
end

-- Returns a set of used keys and a map of each key to the files using it and
-- how many times each file uses it.
local function read_markdown_files(paths)
  local set = {}
  local files = {}
  for _, path in ipairs(paths) do
    add_used_keys(utils.read_file(path), path, set, files)
  end
  return set, files
end

-- Returns the indices of entries whose display text is out of alphabetical
-- order when compared case-insensitively.
local function out_of_order(texts)
  local result = {}
  for i = 2, #texts do
    if texts[i]:lower() < texts[i - 1]:lower() then
      result[#result + 1] = i
    end
  end
  return result
end

-- Report entries whose display text is out of alphabetical order.
-- Return true if any were found.
local function report_order(texts, label)
  local bad = out_of_order(texts)
  if #bad == 0 then
    return false
  end
  print(label)
  for _, i in ipairs(bad) do
    print(("  %s follows %s"):format(texts[i], texts[i - 1]))
  end
  return true
end

-- Returns the keys referred to more than once, mapped to the files they occur
-- in and how many times each file refers to them.
local function duplicated_keys(files)
  local result = {}
  for key, paths in pairs(files) do
    local total = 0
    for _, count in pairs(paths) do
      total = total + count
    end
    if total > 1 then
      result[key] = paths
    end
  end
  return result
end

-- Report keys referred to more than once under 'label'.
-- Return true if any were found.
local function report_duplicated(files, label)
  local duplicated = duplicated_keys(files)
  if next(duplicated) == nil then
    return false
  end
  print(label)
  for _, key in ipairs(utils.sorted_keys(duplicated)) do
    for _, path in ipairs(utils.sorted_keys(duplicated[key])) do
      print(("  %s: %s"):format(key, path))
    end
  end
  return true
end

if #arg < 2 then
  utils.fail("usage: lua check-glossary.lua GLOSSARY_FILE MARKDOWN_FILE...")
end

local defined_order, defined_set, display_texts = read_glossary_file(arg[1])

local markdown_files = {}
for i = 2, #arg do
  markdown_files[#markdown_files + 1] = arg[i]
end
local used_set, used_files = read_markdown_files(markdown_files)

local problems = false
if utils.report_missing(defined_set, used_files, "used but not defined:") then
  problems = true
end
if report_duplicated(used_files, "duplicated redefinitions:") then
  problems = true
end
if utils.report_unused(defined_order, used_set, "defined but not used:") then
  problems = true
end
if report_order(display_texts, "out of alphabetical order:") then
  problems = true
end

if problems then
  os.exit(1)
end
