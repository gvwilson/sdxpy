"""Handle figures references and figures."""

import ark
import shortcodes

import util


@shortcodes.register("f")
@util.timing
def figure_ref(pargs, kwargs, node):
    """Handle [%f slug %] figure reference shortcode."""
    util.require(
        (len(pargs) == 1) and (not kwargs),
        f"Bad 'f' in {node.path}: '{pargs}' and '{kwargs}'",
    )
    slug = pargs[0]
    known = ark.site.config["_figures_"]
    util.require(slug in known, f"Unknown figure slug {slug} in {node.path}")
    number = known[slug]["slug"]
    file_slug = known[slug]["node"]
    caption = f"{util.kind('figure')}&nbsp;{number}"
    return f'<a class="fig-ref" href="@root/{file_slug}/#{slug}">{caption}</a>'


@shortcodes.register("figure")
@util.timing
def figure_def(pargs, kwargs, node):
    """Handle figure definition."""
    allowed = {"cls", "scale", "slug", "img", "alt", "caption"}
    util.require(
        (not pargs) and util.allowed(kwargs, allowed),
        f"Bad 'figure' in {node.path}: '{pargs}' and '{kwargs}'",
    )

    cls = kwargs.get("cls", None)
    cls = f' class="{cls}"' if cls is not None else ""

    scale = kwargs.get("scale", None)
    scale = f' width="{scale}"' if scale is not None else ""

    slug = kwargs["slug"]
    img = kwargs["img"]
    alt = util.markdownify(kwargs["alt"])
    caption = util.markdownify(kwargs["caption"])

    util.require_file(node, img, "figure")
    known = ark.site.config["_figures_"]

    if util.is_index_file(node):
        label = f"{util.kind('figure')}&nbsp;{known[slug]['slug']}: "
        relpath = "."
    elif util.is_slide_file(node):
        label = ""
        relpath = ".."
    else:
        util.fail(f"Unknown node type for figure {node}")
    body = f'<img src="{relpath}/{img}" alt="{alt}"{scale}/>'
    caption = f'<figcaption>{label}{caption}</figcaption>'
    return f'<figure id="{slug}"{cls}>\n{body}\n{caption}\n</figure>'
