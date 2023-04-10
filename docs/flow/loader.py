import importlib
import sys
from pathlib import Path

EXPORT = "export"

def load(dirs):
    result = {}
    for d in dirs:
        sys.path.insert(0, d)
        for filename in Path(d).iterdir():
            if filename.suffix != ".py":
                continue
            name = filename.stem
            module = importlib.import_module(name)
            if hasattr(module, EXPORT):
                cls = getattr(module, EXPORT)
                result[cls.__name__] = cls
        sys.path.pop(0)
    return result
