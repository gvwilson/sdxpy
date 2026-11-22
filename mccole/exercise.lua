-- Exercise inclusion shortcode.
--
-- Usage: {{< exercise KIND FILENAME TIME >}}
--   KIND     either "book" or "slides"
--   FILENAME path to a Markdown file (relative to the file containing the
--            shortcode) whose first line is an H1 heading with the title
--   TIME     duration in minutes (only used when KIND is "book")
--
-- The H1 heading in the included file is stripped and replaced with an H3
-- (book) or H2 (slides) heading; for book output the time is appended to the
-- title.

return {
  ["exercise"] = function(args, kwargs, meta)
    local rel = pandoc.utils.stringify(args[1])

    -- Resolve the included file relative to the file containing the shortcode.
    local input = quarto.doc.input_file or "."
    local dir = pandoc.path.directory(input)
    local path = pandoc.path.join({dir, rel})

    local f = assert(io.open(path, "r"), "exercise: cannot open " .. rel)
    local content = f:read("*all")
    f:close()

    -- The first line must be an H1 heading; capture its text and remove it.
    local title
    content = content:gsub("^%s*##%s+([^\r\n]*)\r?\n?", function(text)
      title = text:gsub("%s+$", "")
      return ""
    end, 1)

    -- Drop blank lines left between the removed heading and the body.
    content = content:gsub("^[\r\n]+", "")

    local heading
    heading = "### " .. title .. "\n\n"

    return pandoc.read(heading .. content, "markdown").blocks
  end
}
