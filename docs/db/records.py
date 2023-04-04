class Experiment:
    MAX_NAME_LEN = 6
    TIMESTAMP_LEN = 10
    MAX_READING = 10
    MAX_READING_LEN = 2
    MAX_READINGS_NUM = 2
    RECORD_LEN = MAX_NAME_LEN + 1 \
        + TIMESTAMP_LEN + 1 \
        + (MAX_READING_LEN * 3 * MAX_READINGS_NUM)

    @staticmethod
    def size():
        return Experiment.RECORD_LEN

    @staticmethod
    def key(record):
        assert isinstance(record, Experiment)
        return record._name

    @staticmethod
    def pack(record):
        assert isinstance(record, Experiment)
        readings = "\0".join(str(r) for r in record._readings)
        result = f"{record._name}\0{record._timestamp}\0{readings}"
        if len(result) < Experiment.RECORD_LEN:
            result += "\0" * (Experiment.RECORD_LEN - len(result))
        return result

    @staticmethod
    def unpack(raw):
        assert isinstance(raw, str)
        parts = raw.split("\0")
        name = parts[0]
        timestamp = int(parts[1])
        readings = [int(r) for r in parts[2:] if len(r)]
        return Experiment(name, timestamp, readings)

    @staticmethod
    def pack_multi(records):
        return ''.join([Experiment.pack(r) for r in records])

    @staticmethod
    def unpack_multi(raw):
        size = Experiment.size()
        split = [raw[i:i+size] for i in range(0, len(raw), size)]
        return [Experiment.unpack(s) for s in split]

    def __init__(self, name, timestamp, readings):
        assert 0 < len(name) <= self.MAX_NAME_LEN
        assert 0 <= len(readings) <= self.MAX_READINGS_NUM
        assert all((0 <= r <= self.MAX_READING) for r in readings)
        self._name = name
        self._timestamp = timestamp
        self._readings = readings

    def __str__(self):
        joined = ', '.join(str(r) for r in self._readings)
        return f"{self._name}({self._timestamp})[{joined}]"

    def __eq__(self, other):
        return isinstance(other, Experiment) and \
            (self._name == other._name) and \
            (self._timestamp == other._timestamp) and \
            (self._readings == other._readings)
