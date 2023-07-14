#!/usr/bin/env python

"""Turn single-page HTML into LaTeX."""

import argparse
import sys

from bs4 import BeautifulSoup, NavigableString, Tag

from . import util

CROSSREFS = {"Appendix": "appref", "Chapter": "chapref", "Section": "secref"}

GL_PREFIX = "gl:"

PRINT_INDEX = r"""
\cleardoublepage
\makeatletter
\renewcommand{\tocetcmark}[1]{%
  \@mkboth{{#1}}{{#1}}}
  \makeatother
\printindex
"""

LATEX_FIG_SMALL = 0.6
LATEX_FIG_REGULAR = 0.8


def main():
    """Convert HTML to LateX."""
    options = parse_args()
    glossary = read_glossary(options.glossary)
    text = sys.stdin.read()
    text = text.replace(r"\(", "<math>").replace(r"\)", "</math>")
    soup = BeautifulSoup(text, "html.parser")
    state = {
        "appendix": False,
        "seen": {},
        "unknown": set(),
        "glossary": glossary,
        "language": options.language,
    }
    accum = []
    for child in soup.find_all("section", class_="new-chapter"):
        accum = handle(child, state, accum, True)
    result = "".join(accum)

    with open(options.head, "r") as reader:
        print(reader.read())
    print(result)
    with open(options.foot, "r") as reader:
        print(reader.read())

    if options.debug:
        if state["unknown"]:
            print("Unknown:", file=sys.stderr)
            for key in sorted(state["unknown"]):
                print(key, file=sys.stderr)
        print("Seen", file=sys.stderr)
        for key in sorted(state["seen"]):
            print(key, file=sys.stderr)
            for value in sorted(state["seen"][key]):
                print(f"- {', '.join(value)}", file=sys.stderr)


def children(node, state, accum, doEscape):
    """Convert children of node."""
    for child in node:
        handle(child, state, accum, doEscape)
    return accum


def citation(node, state, accum, doEscape):
    """Handle bibliographic citation."""
    cites = node.find_all("a")
    assert all(has_class(child, "bib-ref") for child in cites)
    keys = ",".join([c["href"].split("#")[1] for c in cites])
    accum.append(rf"\cite{{{keys}}}")


def escape(text, doEscape):
    """Escape special characters if asked to."""
    if not doEscape:
        return text
    return (
        text.replace("{", "ACTUAL-LEFT-CURLY-BRACE")
        .replace("}", "ACTUAL-RIGHT-CURLY-BRACE")
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
        .replace("~", r"{\textapprox}")  # see https://tex.stackexchange.com/a/377
        .replace("©", r"{\textcopyright}")
        .replace("μ", r"{\textmu}")
        .replace("…", "...")
        .replace("ACTUAL-LEFT-CURLY-BRACE", r"\{")
        .replace("ACTUAL-RIGHT-CURLY-BRACE", r"\}")
    )


def figure(node, state, accum, doEscape):
    """Convert a figure."""
    assert node.name == "figure", "Not a figure"
    label = node["id"]

    if node.has_attr("class") and "figure-here" in node["class"]:
        command = "figpdfhere"
    else:
        command = "figpdf"

    if node.has_attr("class") and "latex-small" in node["class"]:
        scale = LATEX_FIG_SMALL
    else:
        scale = LATEX_FIG_REGULAR

    path = node.img["src"].replace(".svg", ".pdf")
    caption = "".join(children(node.figcaption, state, [], True))
    caption = caption.split(":", 1)[1].strip()
    accum.append(f"\\{command}{{{label}}}{{{path}}}{{{caption}}}{{{scale}}}\n")


def handle(node, state, accum, doEscape):
    """Handle nodes by type."""
    record_seen(node, state)

    # Pure text
    if isinstance(node, NavigableString):
        accum.append(escape(node.string, doEscape))

    # Not a tag
    elif not isinstance(node, Tag):
        pass

    # <a class="figref"> => figure cross-reference
    elif node_match(node, "a", "fig-ref"):
        key = href_key(node)
        accum.append(rf"\figref{{{key}}}")

    # <a class="gl-ref"> => glossary cross-reference
    elif node_match(node, "a", "gl-ref"):
        accum.append(r"\glossref{")
        children(node, state, accum, doEscape)
        accum.append("}")
        key = href_key(node)
        if key.startswith(GL_PREFIX):
            key = key[len(GL_PREFIX) :]
        term = state["glossary"][key][state["language"]]["term"]
        accum.append(rf"\index{{{escape(term, True)}}}")

    # <a class="link-ref"> => just show the link
    elif node_match(node, "a", "link-ref"):
        children(node, state, accum, doEscape)

    # <a class="tbl-ref"> => table cross-reference
    elif node_match(node, "a", "tbl-ref"):
        key = href_key(node)
        accum.append(rf"\tblref{{{key}}}")

    # <a class="x-ref"> => section cross-reference
    elif node_match(node, "a", "x-ref"):
        key = node["href"].lstrip("#")
        kind = node.text.split(" ")[0]
        assert kind in CROSSREFS
        accum.append(rf"\{CROSSREFS[kind]}{{{key}}}")

    # <a> without class
    elif node_match(node, "a"):
        # pure internal link in glossary
        if node["href"].startswith("#"):
            accum.append(r"\glosskey{")
            children(node, state, accum, doEscape)
            accum.append("}")

        # explicitly suppress footnote URL
        elif has_class(node, "no-footnote"):
            children(node, state, accum, doEscape)

        # external link
        else:
            accum.append(r"\hreffoot{")
            children(node, state, accum, doEscape)
            accum.append("}{")
            accum.append(escape(node["href"], True))
            accum.append("}")

    # <blockquote> => quotation
    elif node_match(node, "blockquote"):
        accum.append("\\begin{quotation}\n")
        children(node, state, accum, doEscape)
        accum.append("\\end{quotation}\n")

    # <br> => newline
    elif node_match(node, "br"):
        accum.append("\\\\\n")

    # <code> => inline typewriter text
    elif node_match(node, "code"):
        temp = "".join(children(node, state, [], True))
        temp = temp.replace("'", r"{\textquotesingle}")
        accum.append(rf"\texttt{{{temp}}}")

    # <dd> => body of labeled itemize
    elif node_match(node, "dd"):
        children(node, state, accum, doEscape)
        accum.append("\n\n")

    # <div class="notex"> => skip
    elif node_match(node, "div", "notex"):
        pass

    # <div class="callout"> => create a callout
    elif node_match(node, "div", "callout"):
        accum.append("\\begin{callout}\n")
        children(node, state, accum, doEscape)
        accum.append("\\end{callout}\n")

    # <div class="center"> => center a block of text
    elif node_match(node, "div", "center"):
        accum.append("\\begin{center}\n")
        children(node, state, accum, doEscape)
        accum.append("\\end{center}\n")

    # <div class="code-sample"> => pass through
    elif node_match(node, "div", "code-sample"):
        children(node, state, accum, doEscape)

    # <div class="glossary"> => pass through
    elif node_match(node, "div", "glossary"):
        children(node, state, accum, doEscape)

    # <div class="highlight"> => code
    elif node_match(node, "div", "highlight"):
        children(node, state, accum, doEscape)

    # <div class="pagebreak"> => force a LaTeX page break
    elif node_match(node, "div", "pagebreak"):
        accum.append("\n\\newpage\n")

    # <div class="table"> => pass through
    elif node_match(node, "div", "table"):
        children(node, state, accum, doEscape)

    # <dl class="bib-list"> => placeholder for bibliography
    elif node_match(node, "dl", "bib-list"):
        accum.append("\\printbibliography[heading=none]\n")

    # <dl> => itemize list
    elif node_match(node, "dl"):
        children(node, state, accum, doEscape)

    # <dt> => itemize key
    elif node_match(node, "dt"):
        accum.append(r"\noindent \textbf{")
        children(node, state, accum, doEscape)
        accum.append("}: ")

    # <em> => italics
    elif node_match(node, "em"):
        accum.append(r"\emph{")
        children(node, state, accum, doEscape)
        accum.append(r"}")

    # <figure> => figpdf macro
    elif node_match(node, "figure"):
        figure(node, state, accum, doEscape)

    # <h1> => chapter title
    elif node_match(node, "h1"):
        assert node.has_attr("id"), f"H1 without ID {node}"
        state["slug"] = node["id"]
        content = "".join(children(node, state, [], doEscape))
        kind, title = content.split(":", 1)
        if kind.startswith("Appendix") and not state["appendix"]:
            accum.append("\n\\appendix\n")
            state["appendix"] = True
        accum.append(r"\chapter{")
        accum.append(title.strip())
        accum.append(r"}\label{")
        accum.append(state["slug"])
        accum.append("}\n")
        if state["appendix"]:
            accum.append(
                f"\\markboth{{\\thechapter\\ {title}}}{{\\thechapter\\ {title}}}"
            )

    # <h2> => section title (with or without ID)
    elif node_match(node, "h2"):
        title = "".join(children(node, state, [], doEscape))
        if ":" in title:
            title = title.split(":", 1)[1].strip()
        if node.has_attr("id"):
            accum.append(r"\section{")
            accum.append(title)
            accum.append(r"}\label{")
            accum.append(node["id"])
            accum.append("}\n")
        else:
            accum.append(r"\section*{")
            accum.append(title)
            accum.append("}\n")

    # <h3> inside <div class="callout"> => callout title
    elif (
        (node.name == "h3")
        and (node.parent.name == "div")
        and has_class(node.parent, "callout")
    ):
        accum.append("\n")
        accum.append(r"\subsubsection*{")
        children(node, state, accum, doEscape)
        accum.append("}\n")

    # other <h3> => subsection (unnumbered)
    elif node_match(node, "h3"):
        accum.append(r"\subsection*{")
        children(node, state, accum, doEscape)
        accum.append("}\n")

    # <li> => list item
    elif node_match(node, "li"):
        accum.append(r"\item ")
        children(node, state, accum, doEscape)
        accum.append("\n")

    # <math> => math text
    elif node_match(node, "math"):
        accum.append(f"${make_math(node.text)}$")

    # <ol> => ordered list
    elif node_match(node, "ol"):
        accum.append("\\begin{enumerate}\n")
        children(node, state, accum, doEscape)
        accum.append("\\end{enumerate}\n")

    # <p> => paragraph
    elif node_match(node, "p"):
        accum.append("\n")
        if noindent(node):
            accum.append(r"\noindent ")
        children(node, state, accum, doEscape)
        accum.append("\n")

    # <pre> => preformatted text
    elif node_match(node, "pre"):
        assert 1 <= len(node.contents) <= 2, f"Bad code node {node}"

        # Direct code (not an include file, no language specified).
        if len(node.contents) == 1:
            title, body = "", node.contents[0]

        # Code inclusion with language and title.
        else:
            title, body = node.contents[0], node.contents[1]
            assert title.name == "span", "Expected span as title node of pre"

        # Are we switching display type based on language?
        background = ""
        frame = "tblr"
        if node_match(node.parent.parent, "div", "code-sample"):
            if has_class(node.parent.parent, {"lang-html", "lang-out", "lang-txt"}):
                background = r",backgroundcolor=\color{black!5}"
            if has_class(node.parent.parent, {"lang-sh"}):
                frame = "shadowbox"

        # Build code.
        assert body.name == "code", "Expected code as body of pre"
        accum.append(f"\\begin{{lstlisting}}[frame={frame}{background}]\n")
        children(body, state, accum, False)
        accum.append("\\end{lstlisting}\n")

    # <section> => chapter (recurse only)
    elif node_match(node, "section"):
        if node.h1["id"] == "contents":
            accum.append(PRINT_INDEX)
        else:
            children(node, state, accum, doEscape)

    # <span class="bib-ref"> => citations
    elif node_match(node, "span", "bib-ref"):
        citation(node, state, accum, doEscape)

    # <span class="gl-key"> => format glossary key
    elif node_match(node, "span", "gl-key"):
        accum.append(r"{\newline}\glosskey{")
        children(node, state, accum, doEscape)
        accum.append(r"}")

    # <span class="indexentry"> => add an index entry
    elif node_match(node, "span", "ix-entry"):
        children(node, state, accum, doEscape)
        index_entry(node, state, accum, doEscape)

    # <span> => ignore
    elif node_match(node, "span"):
        children(node, state, accum, doEscape)

    # <strong> => bold text
    elif node_match(node, "strong"):
        accum.append(r"\textbf{")
        children(node, state, accum, doEscape)
        accum.append(r"}")

    # <table> => a table
    elif node_match(node, "table"):
        table(node, state, accum, doEscape)

    # <td> => pass through
    elif node_match(node, "td"):
        children(node, state, accum, doEscape)

    # <th> => pass through
    elif node_match(node, "th"):
        children(node, state, accum, doEscape)

    # <ul> => unordered list
    elif node_match(node, "ul"):
        accum.append("\\begin{itemize}\n")
        children(node, state, accum, doEscape)
        accum.append("\\end{itemize}\n")

    # anything else => report
    else:
        state["unknown"].add(str(node))

    # Report back.
    return accum


def has_class(node, cls):
    """Check if node has one of the specified classes."""
    if not node.has_attr("class"):
        return False
    if isinstance(cls, str):
        return cls in node["class"]
    assert isinstance(cls, set)
    return any(c in node["class"] for c in cls)


def href_key(node):
    """Get key from href attribute if available."""
    if "#" in node["href"]:
        return node["href"].split("#")[1]
    return node["href"]


def index_entry(node, state, accum, doEscape):
    """Construct index entries."""
    assert (node.name == "span") and node.has_attr("ix-key")
    for key in [k.strip() for k in node["ix-key"].split(";")]:
        accum.append(rf"\index{{{escape(key, doEscape)}}}")


def make_math(text):
    """Convert text to math symbols."""
    return text.replace("×", r"{\times}")


def node_match(node, name, cls=None):
    """Does this node match requirements?"""
    if node.name != name:
        return False
    if cls is None:
        return True
    return has_class(node, cls)


def noindent(node):
    """Is this an unindented paragraph?"""
    return node_match(node, "p", {"continue", "definitions"})


def parse_args():
    """Handle command-line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--debug", action="store_true", help="show debugging")
    parser.add_argument("--foot", required=True, help="LaTeX foot")
    parser.add_argument("--glossary", required=True, help="glossary file")
    parser.add_argument("--head", required=True, help="LaTeX head")
    parser.add_argument("--language", required=True, help="language code")
    return parser.parse_args()


def read_glossary(filename):
    """Read glossary and convert to dictionary."""
    glossary = util.read_yaml(filename)
    return {entry["key"]: entry for entry in glossary}


def record_seen(node, state):
    """Record which node types have been seen."""
    if not isinstance(node, Tag):
        return
    seen = state["seen"]
    if node.name not in seen:
        seen[node.name] = set()
    if node.has_attr("class"):
        seen[node.name].add(tuple(sorted(node["class"])))
    else:
        seen[node.name].add(("None",))


def table(node, state, accum, doEscape):
    """Convert a table."""
    assert node.name == "table", "Node is not a table"
    label = node["id"] if node.has_attr("id") else None
    position = node["class"] if node.has_attr("class") else None
    position = "[h]" if position is not None else ""

    assert node.tbody, f"Table node does not have body {node}"
    rows = [table_row(row, state, doEscape, "td") for row in node.tbody.find_all("tr")]
    width = len(node.tbody.find("tr").find_all("td"))
    spec = "l" * width

    thead = node.thead
    if thead:
        row = thead.tr
        assert row, f"Table head does not have row {node}"
        headers = node.thead.tr.find_all("th")
        assert headers, f"Table node does not have headers {node}"
        head = table_row(node.thead.tr, state, doEscape, "th")
        rows = [head, *rows]

    if label:
        caption = "".join(children(node.caption, state, [], True))
        caption = caption.split(":")[1].strip()
        accum.append(f"\\begin{{table}}{position}\n")
    else:
        accum.append("\n\\vspace{\\baselineskip}\n")

    accum.append(f"\\begin{{tabular}}{{{spec}}}\n")
    accum.append("\n".join(rows))
    accum.append("\n\\end{tabular}\n")
    if label:
        accum.append(f"\\caption{{{caption}}}\n")
        accum.append(f"\\label{{{label}}}\n")
        accum.append("\\end{table}\n")
    else:
        accum.append("\n\\vspace{\\baselineskip}\n")


def table_row(row, state, doEscape, tag):
    """Convert a single row of a table to a string."""
    cells = row.find_all(tag)
    result = []
    for cell in cells:
        temp = handle(cell, state, [], True)
        temp = "".join(temp)
        if tag == "th":
            temp = rf"\textbf{{\underline{{{temp}}}}}"
        result.append(temp)
    return " & ".join(result) + r" \\"


if __name__ == "__main__":
    main()
