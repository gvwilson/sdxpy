import json

# [body]
import networkx as nx
from config_loader import ConfigLoader
from networkx.readwrite import json_graph

class GraphCreator(ConfigLoader):
    def build(self):
        self.load_config()
        self.build_graph()
        self.check_cycles()
    # [/body]

    # [build]
    def build_graph(self):
        self.graph = nx.DiGraph()

        for rule in self.rules:
            self.graph.add_node(rule["target"], recipes=rule["recipes"])

        for rule in self.rules:
            for d in rule["depends"]:
                self.graph.add_edge(d, rule["target"])
    # [/build]

    # [check]
    def check_cycles(self):
        cycles = list(nx.algorithms.simple_cycles(self.graph))
        assert len(cycles) == 0, f"Dependency graph contains cycles {cycles}"
    # [/check]

    # [str]
    def __str__(self):
        temp = json_graph.node_link_data(self.graph)
        temp = {k: v for (k, v) in temp.items() if k in {"nodes", "links"}}
        return json.dumps(temp, indent=2)
    # [/str]


# [main]
if __name__ == "__main__":
    import sys
    assert len(sys.argv) == 2, f"Expect config file not {sys.argv}"
    builder = GraphCreator(sys.argv[1])
    builder.build()
    print(builder)
# [/main]
