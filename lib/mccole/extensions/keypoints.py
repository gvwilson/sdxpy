"""Display key points of chapter."""

import ark
import ibis

from filters import is_chapter
import util


@ibis.filters.register("keypoints")
@util.timing
def keypoints(node):
    """Construct key points listing for chapter."""
    if not is_chapter(node):
        return ""

    metadata = ark.site.config["_meta_"]
    util.require(
        node.slug in metadata,
        f"Slug {node.slug} not in metadata",
    )
    if "syllabus" not in metadata[node.slug]:
        return ""

    points = [util.markdownify(p) for p in metadata[node.slug]["syllabus"]]
    points = "\n".join([f"<li>{p}</li>" for p in points])
    return f'<ul class="keypoints">\n{points}\n</ul>'
