import cProfile
import sys

import ivy  # noqa: F401

sys.argv = ["ivy", "build"]
cProfile.run("ivy.main()", sort="tottime")
