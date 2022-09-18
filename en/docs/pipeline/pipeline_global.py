import csv
import sys

import yaml
from generic import EXPORTS as functions


# [func]
def pipeline(config_file, functions):
    with open(config_file, "r") as reader:
        config = yaml.safe_load(reader)
    overall = config.get("overall", {})

    data = None
    for stage in config["pipeline"]:
        func_name, params = stage["name"], stage["params"]
        func = functions[func_name]
        if data is None:
            data = func(*params, **overall)
        else:
            data = func(data, *params, **overall)

    return data


# [/func]

result = pipeline(sys.argv[1], functions)
csv.writer(sys.stdout).writerows(result)
