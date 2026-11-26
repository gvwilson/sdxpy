--
-- shared helpers for the {{< inc ... >}} include, used by both inc-quarto.lua
-- (Quarto shortcode) and inc-pandoc.lua (pandoc filter).
--

local M = {}

M.LANG = { py = "python", sh = "bash", sql = "sql", js = "javascript", css = "css", html = "html", json = "json" }

function M.s(v)
  if type(v) == "string" and v ~= "" then return v end
end

local function escape_pattern(s)
  return (s:gsub("[%^%$%(%)%%%.%[%]%*%+%-%?]", "%%%0"))
end

-- True if `line` contains `token` as a whole marker (followed by a non-word
-- character or end of line); word chars are alphanumeric, '_' and '-', so
-- `mccole:foo` does not match `mccole:foobar`.
local function has_marker(line, token)
  local pat = escape_pattern(token)
  return line:find(pat .. "[^%w_-]") ~= nil or line:find(pat .. "$") ~= nil
end

function M.extract_region(content, mark)
  local start_tok = "mccole:" .. mark
  local end_tok = "mccole:/" .. mark
  local lines = {}
  local in_region = false
  for line in (content .. "\n"):gmatch("(.-)\n") do
    if in_region then
      if has_marker(line, end_tok) then break end
      lines[#lines + 1] = line
    elseif has_marker(line, start_tok) then
      in_region = true
    end
  end
  return table.concat(lines, "\n")
end

function M.omit_region(content, mark)
  local start_tok = "mccole:" .. mark
  local end_tok = "mccole:/" .. mark
  local lines = {}
  local skipping = false
  for line in (content .. "\n"):gmatch("(.-)\n") do
    if skipping then
      if has_marker(line, end_tok) then skipping = false end
    elseif has_marker(line, start_tok) then
      skipping = true
    else
      lines[#lines + 1] = line
    end
  end
  return table.concat(lines, "\n")
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
