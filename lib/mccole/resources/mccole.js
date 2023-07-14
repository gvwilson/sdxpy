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

    if (! document.querySelector("meta[name='has_slides']")) {
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

const enableFeedback = () => {
    const repo_meta = document.querySelector("meta[name='repo']")
    const major_meta = document.querySelector("meta[name='major']")
    const template_meta = document.querySelector("meta[name='template']")
    const build_date_meta = document.querySelector("meta[name='build_date']")
    if (!(repo_meta && major_meta && template_meta && build_date_meta)) {
        return
    }

    const repo = repo_meta.getAttribute("content")
    const major = major_meta.getAttribute("content")
    const slides = (template_meta && template_meta.getAttribute("content") == "slides") ? " slides" : ""
    const build_date = build_date_meta.getAttribute('content')

    const issues_url = `${repo}/issues/new`

    for (const heading of [...document.querySelectorAll("h2")]) {
        const title_text = `${major}${slides}/${heading.textContent} (${build_date})`
        const url = `${issues_url}?title=${encodeURI(title_text)}`
        link = document.createElement("a")
        link.setAttribute("href", url)
        heading.parentElement.replaceChild(link, heading)
        link.appendChild(heading)
    }
}

const showSlideSizes = () => {
    const allNodes = [...document.querySelectorAll("div.remark-slide-container")]
    let firstNode = null, firstSlide = null, firstContent = null
    for (const i in allNodes) {
        const node = allNodes[i]
        node.classList.add("remark-visible")
        const slide = node.querySelector("div.remark-slide")
        const content = slide.querySelector("div.remark-slide-content")
        if (firstNode === null) {
            firstNode = node
            firstSlide = {offsetWidth: slide.offsetWidth, offsetHeight: slide.offsetHeight}
            firstContent = {offsetWidth: content.offsetWidth, offsetHeight: content.offsetHeight}
            console.log(`[${parseInt(i)+1}] ${firstSlide.offsetWidth} x ${firstSlide.offsetHeight} | ${firstContent.offsetWidth} x ${firstContent.offsetHeight}`)
        }
        else if ((slide.offsetWidth != firstSlide.offsetWidth) ||
                 (slide.offsetHeight != firstSlide.offsetHeight) ||
                 (content.offsetWidth != firstContent.offsetWidth) ||
                 (content.offsetHeight != firstContent.offsetHeight)) {
            console.log(`(${parseInt(i)+1}) ${slide.offsetWidth} x ${slide.offsetHeight} | ${content.offsetWidth} x ${content.offsetHeight}`)
        }
        node.classList.remove("remark-visible")
    }
    firstNode.classList.add("remark-visible")
}

const mccole = () => {
    constructTableOfContents()
    insertCodeSampleTitles()
    enableFeedback()
    showSlideSizes()
}

mccole()
