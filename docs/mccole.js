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

    if (!document.querySelector("meta[name='has_slides']")) {
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

const loadImages = async (imageArray) => {
    const promiseArray = []; // create an array for promises

    for (let img of imageArray) {
        promiseArray.push(new Promise(resolve => {
            img.onload = () =>
                resolve();
            if (img.complete)
                resolve();
        }));
    }

    await Promise.all(promiseArray); // wait for all the images to be loaded
}

const showSlideSizes = () => {
    const allNodes = [...document.querySelectorAll("div.remark-slide-container")]
    const firstNode = allNodes[0]
    const elFirstSlide = firstNode.querySelector("div.remark-slide")
    const firstSlide = {
        offsetWidth: elFirstSlide.offsetWidth,
        offsetHeight: elFirstSlide.offsetHeight
    }
    const elFirstContent = elFirstSlide.querySelector("div.remark-slide-content")
    const firstContent = {
        offsetWidth: elFirstContent.offsetWidth,
        offsetHeight: elFirstContent.offsetHeight
    }
    console.log(`[1] ${firstSlide.offsetWidth} x ${firstSlide.offsetHeight} | ${firstContent.offsetWidth} x ${firstContent.offsetHeight}`)
    for (const i in allNodes) {
        const node = allNodes[i]
        node.style.display = "block";
        loadImages([...node.querySelectorAll("img")]).then(() => {
            const slide = node.querySelector("div.remark-slide")
            const content = slide.querySelector("div.remark-slide-content")
            const scaler = node.querySelector("div.remark-slide-scaler")
            if ((content.offsetHeight) > scaler.offsetHeight ||
                (content.offsetWidth) > scaler.offsetWidth) {
                console.warn(`Content of slide ${parseInt(i) + 1} is too big for the slide!`)
            }
            if ((slide.offsetWidth !== firstSlide.offsetWidth) ||
                (slide.offsetHeight !== firstSlide.offsetHeight) ||
                (content.offsetWidth !== firstContent.offsetWidth) ||
                (content.offsetHeight !== firstContent.offsetHeight)) {
                console.log(`(${parseInt(i) + 1}) ${slide.offsetWidth} x ${slide.offsetHeight} | ${content.offsetWidth} x ${content.offsetHeight}`)
            }
            node.style.display = ""
        })
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
