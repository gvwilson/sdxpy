-- Glossary reference shortcode.
--
-- Usage: {{< g key "display text" >}}
-- Renders a link to the glossary entry with id `key` on the glossary page.
-- The relative path "../glossary/index.html" is correct because every lesson
-- lives one directory below the project root, as does the glossary chapter.
--
-- If the display text is omitted the key itself is used.

return {
  ["g"] = function(args, kwargs, meta)
    local key = pandoc.utils.stringify(args[1])
    local text = args[2] or args[1]
    return pandoc.Link(text, "../glossary/index.html#" .. key)
  end
}
