// Construct table of contents for page.
// - Find <div class="page-toc">. (Do not build ToC if this element is not present.)
// - Find all <h2>.
// - Create list of links, removing the word "Section" from titles.
// - If page has <meta name="has_slides">, add unnumbered link to slides.
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

// Insert links to code/output samples.
// - Find all <div class="code-sample"> with "title" attribute.
// - Append <p class="code-sample-title"> with value of div's "title" attribute.
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

// Convert section headings to links for filing GitHub issues.
// - Find <meta> attributes for repo, major heading, page template, and build date.
// - If all are present, find all <h2> and wrap with link to GitHub repo issue submission.
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
        const title_text = `/${major}${slides} - ${heading.textContent} (${build_date})`
        const url = `${issues_url}?title=${encodeURI(title_text)}`
        link = document.createElement("a")
        link.setAttribute("href", url)
        heading.parentElement.replaceChild(link, heading)
        link.appendChild(heading)
    }
}

// Load all images referenced in page.
// - Construct array of promises for loading images.
// - Wait for all promises to resolve.
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

// Report sizes of slides.
// - Get dimensions of first (title) slide.
// - For each other slide:
//   - Wait until images have loaded.
//   - Compare size to that of first slide and report differences.
//   - Report if slide overflows.
const reportSlideOverflow = (reportSizes) => {
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
    if (reportSizes) {
	console.log(
	    `[1] ` + \
	    `${slide0.offsetWidth} x ${slide0.offsetHeight} ` + \
	    `| ${content0.offsetWidth} x ${content0.offsetHeight}`
	)
    }
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
	    if (reportSizes) {
		if ((slide.offsetWidth !== slide0.offsetWidth) ||
                    (slide.offsetHeight !== slide0.offsetHeight) ||
                    (content.offsetWidth !== content0.offsetWidth) ||
                    (content.offsetHeight !== content0.offsetHeight)) {
                    console.log(
			`(${parseInt(i) + 1}) ` + \
			`${slide.offsetWidth} x ${slide.offsetHeight} ` + \
			`| ${content.offsetWidth} x ${content.offsetHeight}`
		    )
		}
            }
            node.style.display = ""
        })
    }
    node0.classList.add("remark-visible")
}

const mccole = () => {
    constructTableOfContents()
    insertCodeSampleTitles()
    enableFeedback()
    reportSlideOverflow(true)
}

mccole()
