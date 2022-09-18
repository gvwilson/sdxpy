"""Handle figures and figure references."""

from textwrap import dedent

import shortcodes

import util


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
        slug in figures, f"Unknown figure reference {slug} ({node.filepath})"
    )
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
