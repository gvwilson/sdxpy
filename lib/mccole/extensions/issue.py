"""Shortcode for linking to GitHub issue."""

import ark
import shortcodes
import util


@shortcodes.register("issue")
@util.timing
def issue(pargs, kwargs, node):
    """Insert link to GitHub issue."""
    util.require(
        (len(pargs) == 1) and (not kwargs),
        f"Bad 'issue' in {node.path}: '{pargs}' and '{kwargs}'",
    )
    try:
        number = int(pargs[0])
    except ValueError:
        util.fail(f"Bad 'issue' in {node.path}: {pargs[0]} is not a number")
    try:
        repo = ark.site.config["repo"]
    except KeyError:
        util.fail(f"While processing 'issue' in {node.path}: 'repo' not in config")
    url = f"{repo}/issues/{number}"
    return f'<a href="{url}" class="issue">Issue {number}</a>'
