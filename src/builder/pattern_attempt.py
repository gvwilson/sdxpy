from expand_variables import ExpandVariables

# [body]
class PatternAttempt(ExpandVariables):

    def build(self):
        self.load_config()
        self.build_graph()
        self.extract_rules()
        self.expand_rules()
        self.expand_variables()
        self.add_timestamps()
        self.check_cycles()
        self.run()

    def extract_rules(self):
        self.rules = {}
        for target in self.graph.nodes:
            if "%" in target:
                self.rules[target] = self.graph.nodes[target]["recipes"]
        for name in self.rules:
            self.graph.remove_node(name)
# [/body]

    def expand_rules(self):
        pass # placeholder

# [main]
if __name__ == "__main__":
    import sys
    assert len(sys.argv) == 3, f"Expect config and timestamp file not {sys.argv}"
    builder = PatternAttempt(sys.argv[1], sys.argv[2])
    builder.build()
# [/main]
