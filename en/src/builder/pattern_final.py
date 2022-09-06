import networkx as nx

from expand_variables import ExpandVariables

class PatternFinal(ExpandVariables):

    def build(self):
        self.load_config()
        self.build_graph()
        self.expand_rules()
        self.expand_variables()
        self.add_timestamps()
        self.check_cycles()
        self.run()

    # [build]
    def build_graph(self):
        self.patterns = {
            r["target"]:r for r in self.rules
            if "%" in r["target"]
        }
        self.rules = [r for r in self.rules if "%" not in r["target"]]
        super().build_graph()
    # [/build]

    # [expand]
    def expand_rules(self):
        for target in self.graph.nodes:
            if (rule := self.find_rule(target)):
                self.fill_in(target, rule)
    # [/expand]

    # [find]
    def find_rule(self, target):
        if "." not in target:
            return None
        suffix = target.split(".")[-1]
        key = f"%.{suffix}"
        return self.patterns.get(key, None)
    # [/find]

    # [fill]
    def fill_in(self, target, rule):
        stem = target.split(".")[0]
        self.graph.nodes[target]["recipes"] = rule["recipes"]
        depends = [d.replace("%", stem) for d in rule["depends"]]
        for d in depends:
            self.graph.add_edge(d, target)
    # [/fill]

# [main]
if __name__ == "__main__":
    import sys
    assert len(sys.argv) == 3, f"Expect config and timestamp file not {sys.argv}"
    builder = PatternFinal(sys.argv[1], sys.argv[2])
    builder.build()
# [/main]
