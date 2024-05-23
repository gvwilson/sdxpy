// Inspired by https://yihui.org/en/2023/09/snap-slides/

(function(doc) {
    let page = doc.body;  // <body> is container of slides

    // Is this a plain <hr> separator?
    function isSep(el) {
        return (el.tagName === 'HR') && (el.attributes.length === 0);
    }

    // Set attribute on element by create a div and copy the attribute over.
    function setAttr(el, attr) {
        const m = newElement('div');
        m.innerHTML = `<div ${attr}></div>`;
        const attrs = m.firstElementChild.attributes;
        for (let i = 0; i < attrs.length; i++) {
            let a = attrs[i];
            el.setAttribute(a.name, a.value);
        }
        m.remove();
    }

    // Create new element with given class.
    function newElement(tag, cls) {
        const el = doc.createElement(tag);
        if (cls) {
            el.className = cls;
        }
        return el;
    }

    // Create a new slide.
    function newSlide(s) {
        return (s?.innerText === '') ? s : newElement('div', 'slide');
    }

    // Create slides from content.
    function createSlides() {
        let el = page.firstElementChild;
        // no slides
        if (!el) {
            return false;
        }
        // insert first slide
        let s = newSlide();
        el.before(s);
        while (true) {
            // look at next element in page
            let el = s.nextSibling;
            // if no next element, we're done
            if (!el) {
                break;
            }
            // if this is a slide separator, remove it and start a new slide
            if (isSep(el)) {
                s = newSlide(s);
                el.before(s);
                el.remove();
            }
            // if this is explicitly a new slide, add it
            else if (el.classList?.contains('slide')) {
                s = newSlide(s);
                el.after(s);
            }
            // otherwise, append content to current slide
            else {
                s.append(el);
            }
        }
        return true; // slides were found
    }

    // Add slide number as ID.
    function addSlideId(slide, i) {
	slide.setAttribute('id', `slide-${i}`);
    }

    // Update URL to reflect current slide.
    function addSlideObserver(slide) {
	function report(entries, observer) {
	    if (entries[0].isIntersecting) {
		window.location.hash = slide.getAttribute('id');
	    }
	}
	const observer = new IntersectionObserver(report, {threshold: 0.5});
	observer.observe(slide);
    }

    // Add page number to bottom right.
    function addPageNumber(slide, i, numSlides) {
        const pageNum = newElement('span', 'page-number');
        pageNum.innerText = `${i + 1}/${numSlides}`;
        pageNum.onclick = e => location.hash = i + 1; // ???
        slide.append(pageNum);
    }

    // Apply slide attributes in <!--# --> comments.
    function applyDirectives(slide) {
        const pattern = /[\s\n]class="([^"]+)"/;
        for (let node of slide.childNodes) {
            if (node.nodeType !== Node.COMMENT_NODE) {
                continue;
            }
            let directive = node.textContent;
            if (!/^#/.test(directive)) {
                continue;
            }
            directive = directive.replace(/^#/, '');
            const m = directive.match(pattern);
            if (m) {
                directive = directive.replace(pattern, '').trim();
                slide.className += ' ' + m[1];
            }
            if (directive) {
                setAttr(slide, directive);
            }
            break;
        }
    }

    // add page numbers and directives to slides
    function decorateSlides() {
        const slides = doc.querySelectorAll('div.slide');
        const numSlides = slides.length;
        slides.forEach((s, i) => {
	    addSlideId(s, i);
	    addSlideObserver(s);
            addPageNumber(s, i, numSlides);
            applyDirectives(s);
        });
    }

    // set up and run
    function main(doc) {
        page.classList.add('slide-container');
        if (!createSlides()) {
            return;
        }
        decorateSlides();
        
        // press 'f' for fullscreen mode and 'o' for overview
        doc.addEventListener('keyup', (e) => {
            if (e.target !== doc.body) {
                return;
            }
            if (e.key === 'f') {
                doc.documentElement.requestFullscreen();
            }
            else if (e.key === 'o') {
                doc.body.classList.toggle('overview');
            }
            sessionStorage.setItem('body-class', doc.body.className);
        });
        
        // restore previously saved body class
        const bc = sessionStorage.getItem('body-class');
        if (bc) {
            doc.body.className += ' ' + bc;
        }
    }

    // run
    main(doc);
})(document);
