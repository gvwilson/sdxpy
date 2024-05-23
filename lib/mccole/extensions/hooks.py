"""Various hooks for processing files."""

import ark
import util

EXCLUSIONS = {
    "__pycache__",
}


@ark.filters.register(ark.filters.Filter.LOAD_NODE_DIR)
@util.timing
def keep_dir(value, path):
    """Do not process directories excluded by parent."""
    if path.name in EXCLUSIONS:
        return False
    path = str(path).replace(ark.site.src(), "").lstrip("/")
    return not any(path.startswith(x) for x in ark.site.config["exclude"])


@ark.filters.register(ark.filters.Filter.LOAD_NODE_FILE)
@util.timing
def keep_file(value, path):
    """Only process .md Markdown files."""
    if path.suffix != ".md":
        return False
    path = str(path).replace(ark.site.src(), "").lstrip("/")
    return path not in ark.site.config["exclude"]
