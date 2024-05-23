"""Show chapter tag line."""

import ark
import ibis

import util

@ibis.filters.register("tagline")
@util.timing
def tagline(node):
    """Insert chapter tagline (must exist)."""
    util.require(
        node.slug in ark.site.config["chapters"],
        f"bad tagline request: {node.path} is not a chapter",
    )
    metadata = ark.site.config["_meta_"]
    util.require(
        node.slug in metadata,
        f"no metadata for {node.path}",
    )
    tagline = metadata[node.slug].get("tagline")
    return util.markdownify(tagline) if tagline else ""
