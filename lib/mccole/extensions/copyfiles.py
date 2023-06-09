"""Copy files verbatim from source directory to destination."""

from glob import iglob
from pathlib import Path
from shutil import copyfile

import ark


@ark.events.register(ark.events.Event.INIT)
def copy_files():
    """Copy files."""
    patterns = ark.site.config.get("copy", None)

    # Nothing to copy.
    if patterns is None:
        return

    # Copy everything that matches.
    for pat in patterns:
        src_dir = ark.site.src()
        out_dir = ark.site.out()
        pat = Path(src_dir, "**", pat)
        for src_file in iglob(str(pat), recursive=True):
            out_file = src_file.replace(src_dir, out_dir)
            Path(out_file).parent.mkdir(exist_ok=True, parents=True)
            copyfile(src_file, out_file)
