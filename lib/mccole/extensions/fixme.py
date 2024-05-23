"""Handle notes to self."""

import shortcodes
import util


@shortcodes.register("fixme")
@util.timing
def fixme(pargs, kwargs, node):
    """Leave a note to self."""
    util.require(
        (len(pargs) == 1) and (not kwargs),
        f"Bad 'fixme' in {node.path}: '{pargs}' and '{kwargs}'",
    )
    return f'<p class="fixme">FIXME: {util.markdownify(pargs[0])}</p>'
