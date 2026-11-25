--
-- Resolve "@key" link targets using config/links.md, failing if a key is
-- missing. The links file is located relative to the Quarto project root.
--

local links = {}

local f = assert(
  io.open((quarto.project.directory or ".") .. "/config/links.md", "r"),
  "links.lua: cannot open config/links.md"
)
for line in f:lines() do
  local key, url = line:match("^%[([%w_-]+)%]:%s*(%S+)%s*$")
  if key then links[key] = url end
end
f:close()

function Link(el)
  local target = el.target or ""
  -- Skip Quarto's project-relative links ("@/slug/"); only resolve "@key" external links.
  if target:sub(1, 1) == "@" and target:sub(2, 2) ~= "/" then
    local key = target:sub(2)
    local url = links[key]
    if not url then
      error("links.lua: unknown link key '@" .. key .. "'")
    end
    el.target = url
    return el
  end
end
