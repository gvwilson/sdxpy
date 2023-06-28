"""Handle figures and figure references."""

from dataclasses import dataclass
from textwrap import dedent

import ark
import shortcodes
import util

# ----------------------------------------------------------------------


@dataclass
class Figure:
    """Keep track of information about a figure."""

    node: ark.nodes.Node = None
    fileslug: str = ""
    cls: str = ""
    slug: str = ""
    img: str = ""
    alt: str = ""
    caption: str = ""
    number: tuple = ()
    width: str = ""


@ark.events.register(ark.events.Event.INIT)
def collect():
    """Collect information from pages."""
    # Gather data.
    major = util.make_major()
    collected = {}
    ark.nodes.root().walk(lambda node: _collect(node, major, collected))
    _cleanup(major, collected)


def _collect(node, major, collected):
    """Pull data from a single node."""
    parser = shortcodes.Parser(inherit_globals=False, ignore_unknown=True)
    parser.register(_parse, "figure")
    collected[node.slug] = []
    try:
        parser.parse(node.text, {"node": node, "values": collected[node.slug]})
    except shortcodes.ShortcodeSyntaxError as exc:
        util.fail(f"%figure shortcode parsing error in {node.filepath}: {exc}")


def _cleanup(major, collected):
    """Convert collected figures information to flat lookup table."""
    figures = util.make_config("figures")
    for fileslug in collected:
        if fileslug in major:
            for i, entry in enumerate(collected[fileslug]):
                entry.fileslug = fileslug
                entry.number = (str(major[fileslug]), str(i + 1))
                figures[entry.slug] = entry


def _parse(pargs, kwargs, data):
    """Collect information from a single figure shortcode."""
    data["values"].append(Figure(data["node"], **kwargs))
    return ""


# ----------------------------------------------------------------------


@shortcodes.register("f")
def figure_ref(pargs, kwargs, node):
    """Handle [% f slug %] figure reference shortcodes."""
    util.require((len(pargs) == 1) and (not kwargs), "Bad 'f' shortcode")

    # Haven't collected information yet.
    if (figures := util.get_config("figures")) is None:
        return ""

    # Create cross-reference.
    slug = pargs[0]
    util.require(slug in figures, f"Unknown figure reference {slug} ({node.filepath})")
    figure = figures[slug]
    label = util.make_label("figure", figure.number)
    cls = 'class="fig-ref"'
    url = f"@root/{figure.fileslug}/#{slug}"
    return f'<a {cls} href="{url}">{label}</a>'


@shortcodes.register("figure")
def figure_def(pargs, kwargs, node):
    """Handle figure definition."""
    allowed = {"cls", "slug", "img", "alt", "caption"}
    util.require(
        (not pargs) and allowed.issuperset(kwargs.keys()),
        f"Bad 'figure' shortcode {pargs} and {kwargs}",
    )
    cls = kwargs.get("cls", None)
    cls = f' class="{cls}"' if cls is not None else ""
    slug = kwargs["slug"]
    img = kwargs["img"]
    alt = util.markdownify(kwargs["alt"])
    caption = util.markdownify(kwargs["caption"])

    util.require_file(node, img, "figure")

    if util.is_slides(node):
        return dedent(
            f"""\
            <figure{cls}>
            <img src="../{img}" alt="{alt}"/>
            </figure>
            """
        )

    figure = util.get_config("figures")[slug]
    label = util.make_label("figure", figure.number)
    return dedent(
        f"""\
        <figure id="{slug}"{cls}>
        <img src="./{img}" alt="{alt}"/>
        <figcaption markdown="1">{label}: {caption}</figcaption>
        </figure>
        """
    )


@shortcodes.register("figure_list")
def figure_list(pargs, kwargs, node):
    """Display all figures."""
    util.require(not pargs and not kwargs, "figure_list takes no arguments")

    # Haven't collected information yet.
    if (figures := util.get_config("figures")) is None:
        return ""

    chapters = util.get_config("titles")["chapters"]
    result = []
    for entry in chapters:
        result.append(f"## {entry.title}")
        for i, fig in enumerate(figures.values()):
            if fig.fileslug != entry.slug:
                continue
            alt = util.markdownify(fig.alt)
            label = util.make_label("figure", fig.number)
            caption = util.markdownify(fig.caption)
            result.extend(
                [
                    f'<figure id="fig-{i:04}">',
                    f"<img src='@root/{entry.slug}/{fig.img}' alt='{alt}'>",
                    f'<figcaption markdown="1">{label}: {caption}</figcaption>',
                    "</figure>",
                ]
            )
    return "\n\n".join(result)
