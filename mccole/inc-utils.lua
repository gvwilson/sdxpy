--
-- shared helpers for the {{< inc ... >}} include, used by both inc-quarto.lua
-- (Quarto shortcode) and inc-pandoc.lua (pandoc filter).
--

local M = {}

M.LANG = { py = "python", sh = "bash", sql = "sql", js = "javascript", css = "css", html = "html" }

function M.s(v)
  if type(v) == "string" and v ~= "" then return v end
end

local function escape_pattern(s)
  return (s:gsub("[%^%$%(%)%%%.%[%]%*%+%-%?]", "%%%0"))
end

function M.extract_region(content, mark)
  local m = escape_pattern(mark)
  return content:match("# mccole:" .. m .. "\n(.-)\n# mccole:/" .. m) or ""
end

function M.omit_region(content, mark)
  local m = escape_pattern(mark)
  return content:gsub("# mccole:" .. m .. "\n.-# mccole:/" .. m .. "\n", "")
end

function M.head_lines(content, n)
  local lines = {}
  for line in content:gmatch("([^\n]*)\n") do
    lines[#lines + 1] = line
    if #lines == n then break end
  end
  return table.concat(lines, "\n")
end

function M.scrub_code(content)
  local out = {}
  for line in (content .. "\n"):gmatch("(.-)\n") do
    local s = line
    s = s:gsub("%s*#%s*BUG[^\n]*", "")            -- Python/shell: # BUG …
    s = s:gsub("%s*//%s*BUG[^\n]*", "")           -- JavaScript:   // BUG …
    s = s:gsub("<!%-%-%s*BUG.-%-%->", "")         -- HTML:         <!-- BUG … -->
    s = s:gsub("/%*%s*BUG.-%*/", "")              -- CSS:          /* BUG … */
    if s:match("^%s*%-%-.*BUG") then s = "" end   -- SQL:          -- … BUG …
    if s:match("%S") then
      out[#out + 1] = s
    end
  end
  return table.concat(out, "\n")
end

return M
