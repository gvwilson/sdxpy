--
-- Basic accessibility checks on the generated HTML.
--
-- Usage: lua check-html.lua HTML_FILE...
--
-- Parses each file with pandoc.read(_, "html") and reports:
-- * headings that skip a level
-- * images with no alt text (unless role=presentation or aria-hidden)
-- * links with no visible text and no aria-label/title
-- * aria-labelledby / describedby / controls / owns referencing a missing id
--

local script_dir = arg[0] and arg[0]:match("^(.*)/") or "."
package.path = script_dir .. "/?.lua;" .. package.path

local utils = require("utils")
utils.program = "check-html.lua"

if #arg < 1 then
  utils.fail("usage: lua check-html.lua HTML_FILE...")
end

local ARIA_REF = { ["aria-labelledby"] = true, ["aria-describedby"] = true,
                   ["aria-controls"] = true, ["aria-owns"] = true }

local problems = false
local function report(path, msg)
  print(path .. ": " .. msg)
  problems = true
end

for _, path in ipairs(arg) do
  local html = utils.read_file(path)
  if not html then
    report(path, "cannot read file")
  else
    local doc = pandoc.read(html, "html")
    local ids = {}
    local refs = {}
    local prev = 0

    -- Value of an attribute, or nil. el.attributes is a List of pairs.
    local function attr(el, name)
      for k, v in pairs(el.attributes) do
        if k == name then return v end
      end
      return nil
    end

    local function check(el)
      local t = el.t
      if t == "Header" then
        if prev > 0 and el.level > prev + 1 then
          report(path, string.format("heading skips H%d to H%d", prev, el.level))
        end
        prev = el.level
      elseif t == "Image" then
        local alt = pandoc.utils.stringify(el.caption or {})
        if alt == "" and attr(el, "aria-hidden") ~= "true"
           and attr(el, "role") ~= "presentation" then
          report(path, "image has no alt text")
        end
      elseif t == "Link" then
        local text = pandoc.utils.stringify(el.content or {})
        if text == "" and not attr(el, "aria-label") and not attr(el, "title") then
          report(path, "link has no text or aria-label")
        end
      end

      local id = el.identifier
      if id and id ~= "" then ids[id] = true end
      for k, v in pairs(el.attributes) do
        if ARIA_REF[k] then
          for w in v:gmatch("%S+") do
            table.insert(refs, { k, w })
          end
        end
      end

      return el
    end

    local filter = {
      Header = check, Image = check, Link = check,
      Div = check, Span = check, Code = check, CodeBlock = check, Figure = check,
    }

    for _, b in ipairs(doc.blocks) do
      if filter[b.t] then check(b) end
      pandoc.walk_block(b, filter)
    end

    -- Pandoc's HTML reader drops the id attribute on <figcaption> (its AST
    -- Caption type has no Attr), so collect ids from the raw HTML as well.
    for id in html:gmatch('id="([^"]+)"') do
      ids[id] = true
    end

    for _, r in ipairs(refs) do
      if not ids[r[2]] then
        report(path, string.format('%s references missing id "%s"', r[1], r[2]))
      end
    end
  end
end

if problems then
  os.exit(1)
end
