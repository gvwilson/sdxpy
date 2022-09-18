# [body]
import yaml


class ConfigLoader:
    def __init__(self, rules_file):
        self.rules_file = rules_file

    def build(self):
        self.load_config()

    def load_config(self):
        with open(self.rules_file, "r") as reader:
            self.rules = yaml.load(reader, Loader=yaml.FullLoader)

        assert isinstance(self.rules, list), "Configuration must be array"

        for rule in self.rules:
            self._check(rule)

    # [/body]

    # [check]
    def _check(self, rule):
        """Check a single rule."""
        assert ("target" in rule) and isinstance(
            rule["target"], str
        ), f"Rule {rule} does not have 'target'"

        assert (
            ("depends" in rule)
            and isinstance(rule["depends"], list)
            and all(isinstance(dep, str) for dep in rule["depends"])
        ), f"Bad 'depends' for rule {rule}"

        assert (
            ("recipes" in rule)
            and isinstance(rule["recipes"], list)
            and all(isinstance(r, str) for r in rule["recipes"])
        ), f"Bad 'recipes' for rule {rule}"

    # [/check]


# [main]
if __name__ == "__main__":
    import sys

    assert len(sys.argv) == 2, f"Expect config file not {sys.argv}"
    builder = ConfigLoader(sys.argv[1])
    builder.build()
# [/main]
