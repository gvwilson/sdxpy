"""Handle file exclusions."""

from fnmatch import fnmatch
from pathlib import Path

import ark
from util import read_directives


@ark.filters.register(ark.filters.Filter.LOAD_NODE_FILE)
def keep_file(value, filepath):
    """Only process the right kinds of files."""
    return not _ignore(Path(filepath).parent, filepath)


@ark.filters.register(ark.filters.Filter.LOAD_NODE_DIR)
def keep_dir(value, dirpath):
    """Do not process directories excluded by parent."""
    return not _ignore(Path(dirpath).parent, dirpath)


def _ignore(dirpath, path):
    """Check for pattern-based exclusion."""
    directives = read_directives(dirpath, "exclude")
    configured = ark.site.config.get("exclude", [])
    combined = directives + configured
    return any(fnmatch(path.name, pat) for pat in combined)
