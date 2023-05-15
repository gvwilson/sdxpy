import pydot
import sys

from loader import load

class Flow:
    def __init__(self):
        pass

    def run(self, filename, dirs):
        nodes, edges = self._make_graph(filename)
        available = load(dirs)
        self._construct(available, nodes)
        self._connect(nodes, edges)
        self._start(nodes)

    def _make_graph(self, filename):
        graph = pydot.graph_from_dot_file(filename)[0]
        nodes = {
            n.get_name(): {"label": self._clean_label(n.get_label())}
            for n in graph.get_nodes()
        }
        edges = [
            {
                "src": e.get_source(),
                "dst": e.get_destination(),
                "label": self._clean_label(e.get_label())
            }
            for e in graph.get_edges()
        ]
        return nodes, edges

    def _construct(self, available, nodes):
        for (name, props) in nodes.items():
            props["obj"] = eval(props["label"], globals(), available)

    def _connect(self, nodes, edges):
        for edge in edges:
            if edge["label"] is None:
                label = "input"
            else:
                label = edge["label"]
            src = nodes[edge["src"]]["obj"]
            dst = nodes[edge["dst"]]["obj"]
            src.tell(dst, label)

    def _start(self, nodes):
        for props in nodes.values():
            if props["obj"].kind() == "source":
                props["obj"].run()

    def _clean_label(self, label):
        return None if (label is None) else label.strip('"')

if __name__ == "__main__":
    flow = Flow()
    flow.run(sys.argv[1], sys.argv[2:])
