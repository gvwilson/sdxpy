"""Generate list of thanks."""

import shortcodes
import util


@shortcodes.register("thanks")
def thanks(pargs, kwargs, node):
    """Handle [% thanks %] shortcode."""
    util.require(
        (not pargs) and (not kwargs),
        f"Bad 'thanks' shortcode with {pargs} and {kwargs}",
    )
    details = util.read_thanks()
    if not details:
        return ""
    details = [_format_name(d) for d in details]
    if len(details) == 1:
        return details[0]
    elif len(details) == 2:
        return f"{details[0]} and {details[1]}"
    else:
        details[-1] = f"and {details[-1]}"
        return ", ".join(details)


def _format_name(detail):
    """Handle family-personal and personal-family naming."""
    order = detail.get("order", None)
    if order == "pf":
        return f"{detail['personal']} {detail['family']}"
    elif order == "fp":
        return f"{detail['family']} {detail['personal']}"
    util.fail(f"Unknown order {order} in {detail}")
