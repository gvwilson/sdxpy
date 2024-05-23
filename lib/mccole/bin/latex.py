"""Convert HTML pages to LaTeX for printing."""

import argparse
from bs4 import BeautifulSoup, NavigableString, Tag
import importlib.util
from pathlib import Path
import sys


LATEX_FIG_SCALE = 0.8


class ConversionException(Exception):
    pass


def main():
    """Main driver."""
    options = parse_args()
    config = load_config(options.config)
    pages = load_pages(options.htmldir, config)
    accum = []
    do_latex_header(options, config, accum)
    appendix_marked = False
    for info in pages.values():
        appendix_marked = do_start_appendix(info, accum, appendix_marked)
        recurse(info, info["doc"], accum)
    do_latex_footer(options, config, accum)
    print("".join(accum))


def at_a(info, node, accum, begin):
    """Handle <a href="something">text</a>."""
    cls = node.attrs.get("class", [])

    if "cross-ref" in cls:
        key = node.attrs["href"].rstrip("/").split("/")[-1]
        command = "chapref" if key in info["chapters"] else "appref"
        accum.append(rf"\{command}{{{key}}}")
        return False

    elif "fig-ref" in cls:
        key = node.attrs["href"].split("#")[-1]
        accum.append(rf"\figref{{{key}}}")
        return False

    elif "gl-ref" in cls:
        if begin:
            accum.append(r"\glossref{")
        else:
            accum.append("}")
        return True

    elif "tbl-ref" in cls:
        key = node.attrs["href"].split("#")[-1]
        accum.append(rf"\tblref{{{key}}}")
        return False

    elif (info["slug"] == "glossary") and node.attrs["href"].startswith("#"):
        return True

    else:
        if begin:
            accum.append(r"\hreffoot{")
        else:
            accum.extend(["}{", node["href"], "}"])
        return True


def at_blockquote(info, node, accum, begin):
    """Handle <blockquote>…</blockquote>."""
    if begin:
        accum.append("\\begin{quotation}\n")
    else:
        accum.append("\n\\\begin{quotation}\n")
    return True


def at_caption(info, node, accum, begin):
    """Handle <caption>…</caption>."""
    return True


def at_code(info, node, accum, begin):
    """Handle <code>…</code>."""
    if begin:
        accum.append(r"\texttt{")
    else:
        accum.append("}")
    return True


def at_dd(info, node, accum, begin):
    """Handle <dd>…</dd>."""
    if not begin:
        accum.append("\n")
    return True


def at_dl(info, node, accum, begin):
    """Handle <dl>…</dl>."""
    if begin:
        accum.append("\\begin{description}\n")
    else:
        accum.append("\\end{description}\n")
    return True


def at_div(info, node, accum, begin):
    """Handle <div>…</div>."""
    if any(cls.startswith("language-") for cls in node.attrs["class"]):
        do_codeblock(info, node, accum)
        return False

    elif "table" in node.attrs["class"]:
        do_table_div(info, node, accum)
        return False

    elif "center" in node.attrs.get("class"):
        if begin:
            accum.append("\\begin{center}\n")
        else:
            accum.append("\\begin{center}\n")
        return True

    else:
        warn(info, node)
        return False


def at_dt(info, node, accum, begin):
    """Handle <dt>…</dt>."""
    if begin:
        accum.append(r"\item[")
    else:
        accum.append("] ")
    return True


def at_em(info, node, accum, begin):
    """Handle <em>…</em>."""
    if begin:
        accum.append(r"\emph{")
    else:
        accum.append("}")
    return True


def at_figcaption(info, node, accum, begin):
    """Handle figure caption."""
    return True


def at_figure(info, node, accum, begin):
    """Handle <figure>…</figure>."""
    label = node["id"]
    command = "figpdfhere" if "here" in node.attrs.get("class", []) else "figpdf"
    scale = LATEX_FIG_SCALE
    if node.img.has_attr("width"):
        scale = float(node.img["width"].rstrip("%"))/100
    path = f"{info['slug']}/{node.img['src'].replace('.svg', '.pdf')}"
    caption = do_caption(info, node.figcaption, "figure")
    accum.extend([f"\\{command}", "{", label, "}{", path, "}{", caption, "}{", str(scale), "}"])
    return False

def at_h1(info, node, accum, begin):
    """Handle <h1>…</h1>."""
    if begin:
        accum.append(rf"\chapter{{")
    else:
        accum.extend([rf"}}\label{{{info["slug"]}}}", "\n"])
    return True


def at_h2(info, node, accum, begin):
    """Handle <h2>…</h2>."""
    if begin:
        accum.append(r"\section{")
    else:
        accum.append("}")
    return True


def at_li(info, node, accum, begin):
    """Handle <li>…</li>."""
    if begin:
        accum.append(r"\item ")
    else:
        accum.append("\n")
    return True


def at_main(info, node, accum, begin):
    """Handle <main>…</main>."""
    return True


def at_ol(info, node, accum, begin):
    """Handle <ol>…</ol>."""
    if begin:
        accum.append(r"\begin{enumerate}")
    else:
        accum.append(r"\end{enumerate}")
    return True


def at_p(info, node, accum, begin):
    """Handle <p>…</p>."""
    if begin:
        accum.append("\n")
    else:
        accum.append("\n")
    return True


def at_span(info, node, accum, begin):
    """Handle <span>…</span>."""
    if "bib-ref" in node.attrs["class"]:
        keys = [child.attrs["href"].split("#")[-1] for child in node.find_all("a")]
        accum.extend([r"\cite{", ",".join(keys), "}"])
        return False

    elif "bibtex-protected" in node.attrs["class"]:
        return True

    elif "ix-entry" in node.attrs["class"]:
        if not begin:
            accum.extend([r"\index{", node.attrs["ix-key"], "}"])
        return True

    else:
        warn(info, node)
        return False


def at_strong(info, node, accum, begin):
    """Handle <strong>…</strong>."""
    if begin:
        accum.append(r"\textbf{")
    else:
        accum.append("}")
    return True


def at_table(info, node, accum, begin):
    """Handle <table>…</table>."""
    width = len(node.tbody.find("tr").find_all("td"))
    spec = "l" * width
    rows = [do_table_row(info, row, "td") for row in node.tbody.find_all("tr")]

    if node.thead:
        headers = node.thead.tr.find_all("th")
        head = do_table_row(info, node.thead.tr, "th")
        rows = [head, *rows]

    accum.extend([
        "\n\\vspace{\\baselineskip}\n",
        f"\\begin{{tabular}}{{{spec}}}\n",
        "\n".join(rows),
        "\n\\end{tabular}\n",
        "\n\\vspace{\\baselineskip}\n",
    ])

    return False


def at_td(info, node, accum, begin):
    """Handle <td>…</td>."""
    return True


def at_th(info, node, accum, begin):
    """Handle <th>…</th>."""
    return True


def at_ul(info, node, accum, begin):
    """Handle <ul>…</ul>."""
    if begin:
        accum.append(r"\begin{itemize}")
    else:
        accum.append(r"\end{itemize}")
    return True


def do_caption(info, node, kind):
    """Create a caption."""
    text = "".join(recurse(info, node, []))
    return text.split(":", 1)[1].strip()


def do_codeblock(info, node, accum):
    """Handle highlighted block of code."""
    background = ""
    frame = "tblr"
    rulesepcolor=""
    cls = [c for c in node.attrs["class"] if c.startswith("language-")][0]
    if cls in {"language-html", "language-out", "language-text"}:
        background = r",backgroundcolor=\color{black!5}"
    elif cls in {"lang-sh"}:
        frame = "shadowbox"
        rulesepcolor = r",rulesepcolor=\color{black!50}"
    accum.append(f"\\begin{{lstlisting}}[frame={frame}{rulesepcolor}{background}]\n")
    accum.append(node.pre.code.get_text())
    accum.append("\\end{lstlisting}\n")


def do_latex_footer(options, config, accum):
    """Add footer."""
    filepath = Path(options.root, "lib", config.theme, "latex", "footer.tex")
    footer = filepath.read_text()
    accum.append(footer)


def do_latex_header(options, config, accum):
    """Add header."""
    filepath = Path(options.root, "lib", config.theme, "latex", "header.tex")
    header = filepath.read_text()
    for old, new in (("==TITLE==", config.title), ("==AUTHOR==", config.author["name"])):
        header = header.replace(old, new)
    accum.append(header)


def do_literal_text(node, accum):
    """Handle literal text string."""
    result = (
        node.text.replace("{", "\x02")
        .replace("}", "\x03")
        .replace("\\", r"{\textbackslash}")
        .replace("$", r"\$")
        .replace("%", r"\%")
        .replace("_", r"\_")
        .replace("^", r"{\textasciicircum}")
        .replace("#", r"\#")
        .replace("&", r"\&")
        .replace("<<<", r"<\null<\null<")
        .replace(">>>", r">\null>\null>")
        .replace("<<", r"<\null<")
        .replace(">>", r">\null>")
        .replace("~", r"$\sim$")
        .replace("©", r"{\textcopyright}")
        .replace("μ", r"{\textmu}")
        .replace("…", "...")
        .replace("\x03", r"\}")
        .replace("\x02", r"\{")
    )
    accum.append(result)


def do_nothing(info, node, accum, begin):
    """Do nothing with this node."""
    msg = f"{info['slug']}: unhandled {node.name} {node.attrs} ({node.sourceline})"
    raise ConversionException(msg)


def do_start_appendix(info, accum, marked):
    """Insert start-of-appendices marker?"""
    if marked:
        return marked
    if info["slug"] in info["appendices"]:
        accum.append("\n\\appendix\n")
        return True
    return False


def do_table_div(info, node, accum):
    """Handle table wrapped in div."""
    label = node.attrs.get("id", None)
    latex_pos = "[h]" if any("here" in c for c in node.attrs.get("class", [])) else ""
    table = recurse(info, node.table, [])
    caption = do_caption(info, node.caption, "table")
    accum.extend([
        f"\\begin{{table}}{latex_pos}\n",
        "\\centering\n",
        *table[1:-1], # to remove \baselineskip
        f"\\caption{{{caption}}}\n",
        f"\\label{{{label}}}\n",
        "\\end{table}\n",
    ])
    return False


def do_table_row(info, row, tag):
    """Convert a single row of a table to a string."""
    cells = row.find_all(tag)
    accum = []
    for cell in cells:
        temp = "".join(recurse(info, cell, []))
        if tag == "th":
            temp = rf"\textbf{{\underline{{{temp}}}}}"
        accum.append(temp)
    return " & ".join(accum) + r" \\"


def get_title(doc):
    """Extract title from document."""
    return doc.find("h1").string


def load_config(filename):
    """Load configuration file as module."""
    spec = importlib.util.spec_from_file_location("config", filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_pages(htmldir, config):
    """Load and sanitifze pages."""
    ordered = config.chapters + config.appendices
    # Let LaTeX make the index
    if "contents" in ordered:
        ordered.remove("contents")
    pages = {
        slug: {
            "doc": read_html(Path(htmldir, slug, "index.html")),
            "slug": slug,
        }
        for slug in ordered
    }
    chapters = set(config.chapters)
    appendices = set(config.appendices)
    for slug, info in pages.items():
        info["title"] = get_title(info["doc"])
        info["doc"] = sanitize(info["doc"])
        info["chapters"] = chapters
        info["appendices"] = appendices
    return pages


def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True, help="Root directory")
    options = parser.parse_args()
    options.config = Path(options.root, "config.py")
    options.htmldir = Path(options.root, "docs")
    return options


def read_html(filepath):
    """Read and tidy up an HTML page."""
    text = filepath.read_text()
    doc = BeautifulSoup(text, "html.parser")
    return doc


def recurse(info, node, accum):
    """Recurse at node."""
    if isinstance(node, Tag):
        handler = globals().get(f"at_{node.name}", do_nothing)
        if handler(info, node, accum, True):
            for child in node:
                recurse(info, child, accum)
            handler(info, node, accum, False)
    elif isinstance(node, NavigableString):
        do_literal_text(node, accum)
    return accum


def sanitize(doc):
    """Remove things that aren't translated."""
    title = doc.find("h1").extract()
    keep = doc.find("main")
    keep.insert(0, title)
    for node in keep.find_all(attrs={"class": "notex"}):
        node.decompose()
    return keep


def warn(info, node):
    """Display warning message."""
    print(f"UNKOWNN {info['slug']}: {node.name} {node.attrs} {node.sourceline}", file=sys.stderr)


if __name__ == "__main__":
    main()
