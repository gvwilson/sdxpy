class SkeletonBuilder:

    def __init__(self, config_file):
        self.config_file = config_file

    def build(self):
        self.load_config()
        self.build_graph()
        self.check_cycles()
        self.run()

    def load_config(self):
        """Load configuration."""
        raise NotImplementedError("load_config")

    def build_graph(self):
        """Construct dependency graph."""
        raise NotImplementedError("build_graph")

    def check_cycles(self):
        """Ensure dependency graph is acyclic."""
        raise NotImplementedError("check_cycles")

    def run(self):
        """Build whatever needs building."""
        raise NotImplementedError("run")
