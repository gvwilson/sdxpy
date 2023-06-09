import cProfile
import sys

import ark  # noqa: F401

sys.argv = ["ark", "build"]
cProfile.run("ark.main()", sort="tottime")
