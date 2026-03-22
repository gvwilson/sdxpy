data = {"names": ["Johnson", "Vaughan", "Jackson"]}

dom = read_html("template.html")
expander = Expander(dom, data)
expander.walk()
print(expander.result)
