"""Handle figures and figure references."""

from dataclasses import dataclass
from textwrap import dedent

import ivy
import shortcodes
import util

# ----------------------------------------------------------------------


@dataclass
class Figure:
    """Keep track of information about a figure."""

    node: ivy.nodes.Node = None
    slide: bool = False
    fileslug: str = ""
    cls: str = ""
    slug: str = ""
    img: str = ""
    alt: str = ""
    caption: str = ""
    number: tuple = ()
    width: str = ""


@ivy.events.register(ivy.events.Event.INIT)
def collect():
    """Collect information from pages."""
    # Gather data.
    major = util.make_major()
    collected = {}
    ivy.nodes.root().walk(lambda node: _collect(node, major, collected))
    _cleanup(major, collected)


def _collect(node, major, collected):
    """Pull data from a single node."""
    parser = shortcodes.Parser(inherit_globals=False, ignore_unknown=True)
    parser.register(_parse, "figure")
    collected[node.slug] = []
    parser.parse(node.text, {"node": node, "values": collected[node.slug]})


def _cleanup(major, collected):
    """Convert collected figures information to flat lookup table."""
    figures = util.make_config("figures")
    for fileslug in collected:
        if fileslug in major:
            for (i, entry) in enumerate(collected[fileslug]):
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
    allowed = {"slide", "cls", "slug", "img", "alt", "caption"}
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
    is_slide = kwargs.get("slide", False)

    if is_slide:
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
