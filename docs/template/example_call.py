variables = {"names": ["Johnson", "Vaughan", "Jackson"]}

dom = read_html("template.html")
expander = Expander(dom, variables)
expander.walk()
print(expander.result)
