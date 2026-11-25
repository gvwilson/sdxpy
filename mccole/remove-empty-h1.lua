--
-- drop the empty H1 that `# {.unnumbered}` produces on the home page.
--

function Header(el)
  if el.level == 1 and #el.content == 0 and el.classes:includes("unnumbered") then
    return {}
  end
end
