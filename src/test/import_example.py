import importlib.util
import sys

path = sys.argv[1]
variable = sys.argv[2]

spec = importlib.util.spec_from_file_location("", path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
value = getattr(module, variable)
print(f"After all that, the value is '{value}'")
