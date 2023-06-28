import pydot
import sys

from cat import Cat
from head import Head
from tail import Tail

class Flow:
    def __init__(self):
        pass

    def run(self, filename, source, data, sink):
        nodes, edges = self._make_graph(filename)
        self._construct(nodes)
        self._connect(nodes, edges)
        self._run(nodes, source, data)
        return nodes[sink]["obj"].result()

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

    def _construct(self, nodes):
        for (name, props) in nodes.items():
            props["obj"] = eval(props["label"])

    def _connect(self, nodes, edges):
        for edge in edges:
            if edge["label"] is None:
                label = "input"
            else:
                label = edge["label"]
            src = nodes[edge["src"]]["obj"]
            dst = nodes[edge["dst"]]["obj"]
            src.tell(dst, label)

    def _run(self, nodes, start, data):
        nodes[start]["obj"].notify("input", data)

    def _clean_label(self, label):
        return None if (label is None) else label.strip('"')

if __name__ == "__main__":
    filename, source, sink = sys.argv[1:]
    data = ["a", "b", "c", "d", "e"]
    flow = Flow()
    result = flow.run(filename, source, data, sink)
    print(result)
