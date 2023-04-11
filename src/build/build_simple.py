import json
import sys


# [main]
class BuildBase:
    def build(self, config_file):
        config = self._configure(config_file)
        ordered = self._topo_sort(config)
        for node in ordered:
            self._refresh(config, node)

    def _refresh(self, config, node):
        assert node in config, f"Unknown node {node}"
        print(config[node]["rule"])
# [/main]

    # [config]
    def _configure(self, config_file):
        with open(config_file, "r") as reader:
            config = json.load(reader)
            known = set(config.keys())
            return {
                n: self._check(n, d, known)
                for n, d in config.items()
            }
    # [/config]

    # [check]
    def _check(self, name, details, known):
        assert "rule" in details, f"Missing rule for {name}"
        assert "depends" in details, f"Missing depends for {name}"
        depends = set(details["depends"])
        assert depends.issubset(known), \
            f"Unknown depends for {name}"
        return {"rule": details["rule"], "depends": depends}
    # [/check]

    # [sort]
    def _topo_sort(self, config):
        graph = {n: config[n]["depends"] for n in config}
        result = []
        while graph:
            available = {n for n in graph if not graph[n]}
            assert available, f"Circular graph {graphs.keys()}"
            result.extend(available)
            graph = {
                n: graph[n] - available
                for n in graph
                if n not in available
            }
        return result
    # [/sort]


if __name__ == "__main__":
    builder = BuildBase()
    builder.build(sys.argv[1])
