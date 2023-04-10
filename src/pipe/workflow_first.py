import pydot
import sys

from cat import Cat
from head import Head
from tail import Tail

def make_graph(filename):
    graph = pydot.graph_from_dot_file(filename)[0]
    nodes = {
        n.get_name(): {"label": clean_label(n.get_label())}
        for n in graph.get_nodes()
    }
    edges = [
        {
            "src": e.get_source(),
            "dst": e.get_destination(),
            "label": clean_label(e.get_label())
        }
        for e in graph.get_edges()
    ]
    return nodes, edges

def clean_label(label):
    return None if (label is None) else label.strip('"')

def construct(nodes):
    for (name, props) in nodes.items():
        props["obj"] = eval(props["label"])

def connect(nodes, edges):
    for edge in edges:
        label = edge["label"] if edge["label"] is not None else "input"
        src = nodes[edge["src"]]["obj"]
        dst = nodes[edge["dst"]]["obj"]
        src.tell(dst, label)

def run(nodes, start, data):
    nodes[start]["obj"].notify("input", data)

def show(nodes):
    for (name, props) in nodes.items():
        print(name, props["obj"].result())

def main(filename, start):
    nodes, edges = make_graph(filename)
    construct(nodes)
    connect(nodes, edges)
    run(nodes, start, ["a", "b", "c", "d", "e"])
    show(nodes)

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
