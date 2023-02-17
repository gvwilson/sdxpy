from glob import glob
from importlib.machinery import SourceFileLoader

test_files = glob("**/test_*.py", root_dir=".", recursive=True)
for (i, name) in enumerate(test_files):
    m = SourceFileLoader(f"m{i}", name).load_module()
    for name in dir(m):
        if not name.startswith("test_"):
            continue
        func = getattr(m, name)
        try:
            func()
            print(f"{name} pass")
        except AssertionError:
            print(f"{name} fail")
        except Exception:
            print(f"{name} error")
