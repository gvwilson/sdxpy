const constructTableOfContents = () => {
    const toc = document.querySelector("div.page-toc")
    if (!toc) {
        return
    }

    const list = document.createElement("ol")
    list.classList.add("page-toc")
    toc.appendChild(list)
    for (const heading of [...document.querySelectorAll("h2")]) {
        const item = document.createElement("li")
        item.innerHTML = heading.innerHTML.replace(/Section.+:/g, "")
        const link = document.createElement("a")
        link.href = `#${heading.id}`
        link.appendChild(item)
        list.appendChild(link)
    }

    if (! document.querySelector("meta[name='slides']")) {
	return
    }
    const slides = document.createElement("li")
    slides.classList.add("no-number")
    list.appendChild(slides)
    slides.innerHTML = '<a href="./slides/">slides</a>'
}

const insertCodeSampleTitles = () => {
  for (const node of [...document.querySelectorAll("div.code-sample")]) {
    if (node.hasAttribute("title")) {
      const filename = node.getAttribute('title')
      const newChild = document.createElement("p")
      newChild.innerHTML = `<a href="${filename}">${filename}</a>`
      newChild.classList.add("code-sample-title")
      node.after(newChild)
    }
  }
}

const mccole = () => {
  constructTableOfContents()
  insertCodeSampleTitles()
}

mccole()
