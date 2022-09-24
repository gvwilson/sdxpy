"""Build a list of reviewers."""

import ivy
import shortcodes
import util
import yaml


@shortcodes.register("reviewers")
def reviewers_list(pargs, kwargs, node):
    """Create a list of reviewers."""

    def _format(entry):
        if "url" in entry:
            return f'<li><a href="{entry["url"]}">{entry["name"]}</a></li>'
        return f'<li>{entry["name"]}</li>'

    util.require("reviewers" in ivy.site.config, "No reviewers specified")
    with open(ivy.site.config["reviewers"], "r") as reader:
        reviewers = yaml.safe_load(reader)
    reviewers = [_format(r) for r in reviewers]
    return "<ul>\n" + "\n".join(reviewers) + "\n</ul>"
