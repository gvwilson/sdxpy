-- check-formatting.lua
-- Check that consecutive {{< inc ... >}} shortcodes are separated by a blank line.
--
-- Usage: lua check-formatting.lua MARKDOWN_FILE...
--
-- Adjacent shortcode lines are parsed as one paragraph, so their code blocks
-- merge into a single <pre> in the rendered output. This script reports each
-- file/line where an {{< inc ... >}} line is immediately followed by another,
-- and exits non-zero if any are found.

local script_dir = arg[0] and arg[0]:match("^(.*)/") or "."
package.path = script_dir .. "/?.lua;" .. package.path

local utils = require("utils")
utils.program = "check-formatting.lua"

if #arg < 1 then
  utils.fail("usage: lua check-formatting.lua MARKDOWN_FILE...")
end

local problems = false

for _, path in ipairs(arg) do
  local content = utils.read_file(path)
  local lines = {}
  for line in (content .. "\n"):gmatch("(.-)\n") do
    lines[#lines + 1] = line
  end
  for i = 1, #lines - 1 do
    local a = lines[i]:gsub("%s+$", "")
    local b = lines[i + 1]:gsub("%s+$", "")
    if a:match("^{{< inc ") and b:match("^{{< inc ") then
      print(("%s:%d: adjacent {{< inc >}} lines"):format(path, i))
      problems = true
    end
  end
end

if problems then
  os.exit(1)
end
