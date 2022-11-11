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
  insertCodeSampleTitles()
}

mccole()
