"""Generate link to GitHub issue."""

import ark
import shortcodes
import util


@shortcodes.register("issue")
def issue_ref(pargs, kwargs, node):
    """Handle [% issue number %] issue reference shortcodes."""
    util.require(
        (len(pargs) == 1) and (not kwargs),
        f"Bad 'issue' shortcode with {pargs} and {kwargs} in {node}",
    )
    try:
        number = int(pargs[0])
    except ValueError:
        util.fail(f"Bad issue number {pargs[0]} in issue shortcode in {node}")
    repo = ark.site.config["repo"]
    url = f"{repo}/issues/{number}"
    title = util.TRANSLATIONS[ark.site.config["lang"]]["issue"]
    return f'{title} <a href="{url}">#{number}</a>'
