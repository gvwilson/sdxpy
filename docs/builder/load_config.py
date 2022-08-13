import yaml

from skeleton_builder import SkeletonBuilder

class ConfigLoader(SkeletonBuilder):
    def load_config(self):
        with open(self.config_file, "r") as reader:
            self.config = yaml.load(reader, Loader=yaml.FullLoader)

        assert isinstance(self.config, list), \
            "Configuration must be array"

        for rule in self.config:
            self._check(rule)


    def _check(self, rule):
        """Check a single rule."""
        assert ("target" in rule) and isinstance(rule["target"], str), \
            f"Rule {rule} does not have 'target'"

        assert ("depends" in rule) and \
            isinstance(rule["depends"], list) and \
            all(isinstance(dep, str) for dep in rule["depends"]), \
            f"Bad 'depends' for rule {rule}"

        assert ("recipes" in rule) and \
            isinstance(rule["recipes"], list) and \
            all(isinstance(r, str) for r in recipe), \
            f"Bad 'recipes' for rule {rule}"
