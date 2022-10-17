import networkx as nx
import yaml

from graph_creator import GraphCreator

# [body]
class AddTimestamps(GraphCreator):
    def __init__(self, rules_file, times_file):
        super().__init__(rules_file)
        self.times_file = times_file

    def build(self):
        self.load_config()
        self.build_graph()
        self.add_timestamps()
        self.check_cycles()
    # [/body]

    # [timestamps]
    def add_timestamps(self):
        with open(self.times_file, "r") as reader:
            times = yaml.load(reader, Loader=yaml.FullLoader)
        missing = {n for n in self.graph.nodes} - {n for n in times.keys()}
        assert not missing, f"Name(s) missing from times: {', '.join(missing)}"
        nx.set_node_attributes(self.graph, times, "timestamp")
    # [/timestamps]

# [main]
if __name__ == "__main__":
    import sys
    assert len(sys.argv) == 3, f"Expect config and timestamp file not {sys.argv}"
    builder = AddTimestamps(sys.argv[1], sys.argv[2])
    builder.build()
    print(builder)
# [/main]
