"""Handle file exclusions."""

from fnmatch import fnmatch
from pathlib import Path

import ivy


@ivy.filters.register(ivy.filters.Filter.LOAD_NODE_FILE)
def keep_file(value, filepath):
    """Only process the right kinds of files."""
    return _keep(filepath)


@ivy.filters.register(ivy.filters.Filter.LOAD_NODE_DIR)
def keep_dir(value, dirpath):
    """Do not process directories with exclusion markers."""
    if Path(dirpath, ".ivyignore").exists():
        return False
    return _keep(dirpath)


def _keep(path):
    """Check for pattern-based exclusion."""
    if (patterns := ivy.site.config.get("exclude", None)) is None:
        return False
    return not any(fnmatch(path, pat) for pat in patterns)
