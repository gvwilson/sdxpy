// Construct table of contents for page.
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
        const link = document.createElement("a")
        link.innerHTML = heading.innerHTML.replace(/Section.+:/g, "")
        link.href = `#${heading.id}`
        item.appendChild(link)
        list.appendChild(item)
    }

    if (! document.querySelector("meta[name='has_slides']")) {
        return
    }
    const slides = document.createElement("li")
    slides.classList.add("no-number")
    list.appendChild(slides)
    slides.innerHTML = '<a href="./slides/">slides</a>'
}

// Insert links to code/output samples.
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

// Get metadata from top of page.
const getMetadata = () => {
    let repo = undefined, major = undefined, slides = undefined, build_date = undefined

    const repo_meta = document.querySelector("meta[name='repo']")
    const major_meta = document.querySelector("meta[name='major']")
    const template_meta = document.querySelector("meta[name='template']")
    const build_date_meta = document.querySelector("meta[name='build_date']")

    if (repo_meta && major_meta && template_meta && build_date_meta) {
	repo = repo_meta.getAttribute("content")
	major = major_meta.getAttribute("content")
	slides = (template_meta && template_meta.getAttribute("content") == "slides") ? " slides" : ""
	build_date = build_date_meta.getAttribute('content')
    }

    return {repo, major, slides, build_date}
}

// Convert section headings to links for filing GitHub issues.
const enableFeedback = () => {
    const {repo, major, slides, build_date} = getMetadata()
    if (!repo) {
	return
    }
    const issues_url = `${repo}/issues/new`
    for (const heading of [...document.querySelectorAll("h2")]) {
        const title_text = `/${major}${slides} - ${heading.textContent} (${build_date})`
        const url = `${issues_url}?title=${encodeURI(title_text)}`
        link = document.createElement("a")
        link.setAttribute("href", url)
        heading.parentElement.replaceChild(link, heading)
        link.appendChild(heading)
    }
}

// Load all images referenced in page.
const loadImages = async (imageArray) => {
    const promiseArray = []
    for (let img of imageArray) {
        promiseArray.push(new Promise(resolve => {
            img.onload = () => resolve()
            if (img.complete) {
                resolve()
            }
        }))
    }
    await Promise.all(promiseArray)
}

// Conditionally report size of slide.
const reportSlideSize = (slide, content) => {
    console.log(
        `[1] ` +
        `${slide.offsetWidth} x ${slide.offsetHeight} ` +
        `| ${content.offsetWidth} x ${content.offsetHeight}`
    )
}

// Get initial elements for reporting slides sizes.
const startSlideOverflow = () => {
    const allNodes = [...document.querySelectorAll("div.remark-slide-container")]
    const node0 = allNodes[0]
    const elSlide0 = node0.querySelector("div.remark-slide")
    const slide0 = {
        offsetWidth: elSlide0.offsetWidth,
        offsetHeight: elSlide0.offsetHeight
    }
    const elContent0 = elSlide0.querySelector("div.remark-slide-content")
    const content0 = {
        offsetWidth: elContent0.offsetWidth,
        offsetHeight: elContent0.offsetHeight
    }
    return {allNodes, node0, slide0, content0}
}

// Find and report slides that are too large.
const findAndReportSlideOverflow = (reportSizes, allNodes, slide0, content0) => {
    for (const i in allNodes) {
        const node = allNodes[i]
        node.style.display = "block";
        loadImages([...node.querySelectorAll("img")]).then(() => {
            const slide = node.querySelector("div.remark-slide")
            const content = slide.querySelector("div.remark-slide-content")
            const scaler = node.querySelector("div.remark-slide-scaler")
            if ((content.offsetHeight) > scaler.offsetHeight ||
                (content.offsetWidth) > scaler.offsetWidth) {
                console.warn(`Slide ${parseInt(i) + 1} too large`)
            }
            if ((slide.offsetWidth !== slide0.offsetWidth) ||
                (slide.offsetHeight !== slide0.offsetHeight) ||
                (content.offsetWidth !== content0.offsetWidth) ||
                (content.offsetHeight !== content0.offsetHeight)) {
                    if (reportSizes) {
                        reportSlideSize(slide, content)
		    }
            }
            node.style.display = ""
        })
    }
}

// Report sizes of slides.
const checkSlideOverflow = (reportSizes) => {
    const {allNodes, node0, slide0, content0} = startSlideOverflow()
    const problems = findAndReportSlideOverflow(reportSizes, allNodes, slide0, content0)
    node0.classList.add("remark-visible")
}

const mccole = () => {
    constructTableOfContents()
    insertCodeSampleTitles()
    enableFeedback()
    checkSlideOverflow(false)
}

mccole()
