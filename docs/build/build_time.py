import json
import sys

from build_better import BuildBetter


# [class]
class BuildTime(BuildBetter):
    def _check_keys(self, name, details):
        super()._check_keys(name, details)
        self._must("time" in details, f"No time for {name}")

    def _refresh(self, config, node, actions):
        assert node in config, f"Unknown node {node}"
        if self._needs_update(config, node):
            actions.append(config[node]["rule"])

    def _needs_update(self, config, node):
        return any(
            config[node]["time"] < config[d]["time"]
            for d in config[node]["depends"]
        )
# [/class]


if __name__ == "__main__":
    with open(sys.argv[1], "r") as reader:
        config = json.load(reader)
    builder = BuildBetter()
    actions = builder.build(config)
    for a in actions:
        print(a)
