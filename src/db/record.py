from record_original import BasicRec

# [base]
class Experiment(BasicRec):
    RECORD_LEN = BasicRec.MAX_NAME_LEN + 1 \
        + BasicRec.TIMESTAMP_LEN + 1 \
        + (BasicRec.MAX_READING_LEN * BasicRec.MAX_READINGS_NUM) \
        + (BasicRec.MAX_READINGS_NUM - 1)

    @staticmethod
    def size():
        return Experiment.RECORD_LEN
# [/base]

    @staticmethod
    def key(record):
        assert isinstance(record, Experiment)
        return record._name

    # [pack]
    @staticmethod
    def pack(record):
        assert isinstance(record, Experiment)
        readings = "\0".join(str(r) for r in record._readings)
        result = f"{record._name}\0{record._timestamp}\0{readings}"
        if len(result) < Experiment.RECORD_LEN:
            result += "\0" * (Experiment.RECORD_LEN - len(result))
        return result
    # [/pack]

    # [unpack]
    @staticmethod
    def unpack(raw):
        assert isinstance(raw, str)
        parts = raw.split("\0")
        name = parts[0]
        timestamp = int(parts[1])
        readings = [int(r) for r in parts[2:] if len(r)]
        return Experiment(name, timestamp, readings)
    # [/unpack]

    # [multi]
    @staticmethod
    def pack_multi(records):
        return ''.join([Experiment.pack(r) for r in records])

    @staticmethod
    def unpack_multi(raw):
        size = Experiment.size()
        split = [raw[i:i + size] for i in range(0, len(raw), size)]
        return [Experiment.unpack(s) for s in split]
    # [/multi]
