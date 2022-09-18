import networkx as nx
from add_timestamps import AddTimestamps


# [body]
class UpdateTimestamps(AddTimestamps):
    def build(self):
        self.load_config()
        self.build_graph()
        self.add_timestamps()
        self.check_cycles()
        self.run()

    # [/body]

    # [run]
    def run(self):
        times = nx.get_node_attributes(self.graph, "timestamp")
        current_time = 1 + max(times.values())
        print(f"{current_time}: START")
        for name in reversed(list(nx.topological_sort(self.graph))):
            if self.is_stale(name):
                self.update(name, current_time)
                self.graph.nodes[name]["timestamp"] = current_time
                current_time += 1
        print(f"{current_time}: END")

    # [/run]

    # [stale]
    def is_stale(self, name):
        return any(
            self.graph.nodes[p]["timestamp"] >= self.graph.nodes[name]["timestamp"]
            for p in self.graph.predecessors(name)
        )

    # [/stale]

    # [update]
    def update(self, name, time):
        print(f"- {name} ({time}):")
        for r in self.graph.nodes[name]["recipes"]:
            print(f"  - {r}")

    # [/update]


# [main]
if __name__ == "__main__":
    import sys

    assert len(sys.argv) == 3, f"Expect config and timestamp file not {sys.argv}"
    builder = UpdateTimestamps(sys.argv[1], sys.argv[2])
    builder.build()
# [/main]
