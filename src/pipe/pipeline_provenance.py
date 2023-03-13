import csv
import sys
import time
import yaml

from generic import EXPORTS as functions

# [func]
def pipeline(config_file, functions):
    with open(config_file, "r") as reader:
        config = yaml.safe_load(reader)
    overall = config.get("overall", {})

    data = None
    provenance = []
    for stage in config["pipeline"]:
        func_name, params = stage["name"], stage["params"]
        func = functions[func_name]
        data, info = run(functions, data, func_name, params, overall)
        provenance.append(info)

    return data, provenance
# [/func]

# [run]
def run(functions, data, func_name, params, overall):
    info = {"name": func_name, "params": params}
    start_time = time.time()
    func = functions[func_name]
    if data is None:
        data = func(*params, **overall)
    else:
        data = func(data, *params, **overall)
    info["time"] = time.time() - start_time
    info["size"] = data_size(data)
    return data, info

def data_size(data):
    return [0, 0] if not data else [len(data), len(data[0])]
# [/run]

result, provenance = pipeline(sys.argv[1], functions)
yaml.dump(provenance, sys.stdout)
