class BasicExperiment:
    MAX_NAME_LEN = 6
    TIMESTAMP_LEN = 10
    MAX_READING = 10
    MAX_READING_LEN = 2
    MAX_READINGS_NUM = 2

    @staticmethod
    def key(record):
        assert isinstance(record, BasicExperiment)
        return record._name

    def __init__(self, name, timestamp, readings):
        assert 0 < len(name) <= self.MAX_NAME_LEN
        assert 0 <= len(readings) <= self.MAX_READINGS_NUM
        assert all((0 <= r <= self.MAX_READING) for r in readings)
        self._name = name
        self._timestamp = timestamp
        self._readings = readings

    # [omit]
    def __str__(self):
        joined = ', '.join(str(r) for r in self._readings)
        return f"{self._name}({self._timestamp})[{joined}]"

    def __eq__(self, other):
        return isinstance(other, self.__class__) and \
            (self._name == other._name) and \
            (self._timestamp == other._timestamp) and \
            (self._readings == other._readings)
    # [/omit]
