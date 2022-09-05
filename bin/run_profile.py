import cProfile
import sys
import ivy

sys.argv = ["ivy", "build"]
cProfile.run("ivy.main()", sort="tottime")
