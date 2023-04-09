class Pipeline:
    def __init__(self):
        pass

    def run(self):
        for stage in self._stages:
            stage.run()

