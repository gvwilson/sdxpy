g = {k:str(v) for (k, v) in globals().items()}

import json
import sys
json.dump(g, sys.stdout, indent=2)
