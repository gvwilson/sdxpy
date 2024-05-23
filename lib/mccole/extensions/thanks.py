"""Handle thanks."""

import ark
from pathlib import Path
import shortcodes
import yaml

import util


@shortcodes.register("thanks")
@util.timing
def thanks(pargs, kwargs, node):
    """Handle [% thanks %] shortcode."""
    util.require(
        (not pargs) and (not kwargs),
        f"Bad 'thanks' in {node.path}: '{pargs}' and '{kwargs}'",
    )
    filepath = Path(ark.site.home(), "info", "thanks.yml")
    names = yaml.safe_load(filepath.read_text()) or []
    names = [_format_name(name) for name in names]
    if len(names) == 1:
        return names[0]
    elif len(names) == 2:
        return f"{names[0]} and {names[1]}"
    else:
        names[-1] = f"and {names[-1]}"
        return ", ".join(names)


def _format_name(details):
    """Handle family-personal and personal-family naming."""
    order = details.get("order", None)
    if order == "pf":
        return f"{details['personal']} {details['family']}"
    elif order == "pmf":
        return f"{details['personal']} {details['middle']} {details['family']}"
    elif order == "fp":
        return f"{details['family']} {details['personal']}"
    util.fail(f"Unknown order {order} in {details}")
