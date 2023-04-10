import importlib
import sys
from pathlib import Path

EXPORT = "export"

def load(dirs, name):
    result = None
    for d in dirs:
        assert Path(d).is_dir()
        filename = Path(d, f"{name}.py")
        if filename.exists():
            sys.path.insert(0, d)
            module = importlib.import_module(name)
            sys.path.pop(0)
            if hasattr(module, EXPORT):
                result = getattr(module, EXPORT)
                break
    assert result is not None
    return result
