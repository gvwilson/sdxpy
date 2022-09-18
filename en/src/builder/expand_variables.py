from update_timestamps import UpdateTimestamps


class ExpandVariables(UpdateTimestamps):
    def build(self):
        self.load_config()
        self.build_graph()
        self.expand_variables()
        self.add_timestamps()
        self.check_cycles()
        self.run()

    # [expand]
    def expand_variables(self):
        for target in self.graph.nodes:
            self.expand_one(target)

    def expand_one(self, target):
        dependencies = list(self.graph.predecessors(target))
        recipes = self.graph.nodes[target]["recipes"]
        for (ir, recipe) in enumerate(recipes):
            result = recipe.replace("@TARGET", target).replace(
                "@DEPENDENCIES", " ".join(dependencies)
            )
            for (id, d) in enumerate(dependencies):
                result = result.replace(f"@DEP[{id+1}]", d)
            self.graph.nodes[target]["recipes"][ir] = result

    # [/expand]


# [main]
if __name__ == "__main__":
    import sys

    assert len(sys.argv) == 3, f"Expect config and timestamp file not {sys.argv}"
    builder = ExpandVariables(sys.argv[1], sys.argv[2])
    builder.build()
# [/main]
