"""Handle figures and figure references."""

from dataclasses import dataclass
from textwrap import dedent

import ivy
import shortcodes
import util


@dataclass
class Figure:
    """Keep track of information about a figure."""

    node: ivy.nodes.Node = None
    fileslug: str = ""
    slug: str = ""
    img: str = ""
    alt: str = ""
    caption: str = ""
    number: tuple = ()
    width: str = ""


@shortcodes.register("f")
def figure_ref(pargs, kwargs, node):
    """Handle [% f slug %] figure reference shortcodes."""
    util.require((len(pargs) == 1) and (not kwargs), "Bad 'f' shortcode")

    # Haven't collected information yet.
    if (figures := util.get_config("figures")) is None:
        return ""

    # Create cross-reference.
    slug = pargs[0]
    util.require(
        slug in figures, f"Unknown figure cross-reference {slug} ({node.filepath})"
    )
    figure = figures[slug]
    label = util.make_label("figure", figure.number)
    cls = 'class="fig-ref"'
    url = f"@root/{figure.fileslug}/#{slug}"
    return f'<a {cls} href="{url}">{label}</a>'


@shortcodes.register("figure")
def figure_def(pargs, kwargs, node):
    """Handle [% figure slug=slug img=img alt=alt caption=cap %] figure definition."""
    util.require(
        (not pargs) and {"slug", "img", "alt", "caption"}.issuperset(kwargs.keys()),
        "Bad 'figure' shortcode",
    )
    slug = kwargs["slug"]
    img = kwargs["img"]
    alt = kwargs["alt"]
    caption = kwargs["caption"]

    figure = util.get_config("figures")[slug]
    label = util.make_label("figure", figure.number)

    return dedent(
        f"""\
    <figure id="{slug}">
      <img src="./{img}" alt="{alt}"/>
      <figcaption markdown="1">{label}: {caption}</figcaption>
    </figure>
    """
    )


@ivy.events.register(ivy.events.Event.INIT)
def figures_collect():
    """Collect information by parsing shortcodes."""
    parser = shortcodes.Parser(inherit_globals=False, ignore_unknown=True)
    parser.register(_parse_figure, "figure")
    figures = {}
    ivy.nodes.root().walk(lambda node: _parse_shortcodes(node, parser, figures))
    _flatten_figures(figures)


def _parse_shortcodes(node, parser, figures):
    """Collect information from node."""
    extra = {"node": node, "seen": []}
    parser.parse(node.text, extra)
    figures[node.slug] = extra["seen"]


def _parse_figure(pargs, kwargs, extra):
    """Collect information from a single figure shortcode."""
    extra["seen"].append(Figure(extra["node"], **kwargs))
    return ""


def _flatten_figures(collected):
    """Convert collected figures information to flat lookup table."""
    major = util.make_major()
    figures = util.make_config("figures")
    for fileslug in collected:
        if fileslug in major:
            for (i, entry) in enumerate(collected[fileslug]):
                entry.fileslug = fileslug
                entry.number = (str(major[fileslug]), str(i + 1))
                figures[entry.slug] = entry
