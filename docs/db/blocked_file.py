from pathlib import Path

from blocked import Blocked

# [class]
class BlockedFile(Blocked):
    def __init__(self, record_cls, db_dir):
        super().__init__(record_cls)
        self._db_dir = Path(db_dir)
        self._build_index()

    def add(self, record):
        super().add(record)
        self._save(record)

    def get(self, key):
        if key not in self._index:
            return None
        self._load(key)
        return super().get(key)
# [/class]

    # [save]
    def _save(self, record):
        key = self._record_cls.key(record)
        seq_id = self._index[key]
        block_id = self._get_block_id(seq_id)

        block = self._get_block(block_id)
        packed = self._record_cls.pack_multi(block.values())

        filename = self._get_filename(block_id)
        with open(filename, "w") as writer:
            writer.write(''.join(packed))
    # [/save]

    # [load]
    def _load(self, key):
        seq_id = self._index[key]
        block_id = self._get_block_id(seq_id)
        filename = self._get_filename(block_id)
        self._load_block(block_id, filename)

    def _load_block(self, block_id, filename):
        with open(filename, "r") as reader:
            raw = reader.read()

        records = self._record_cls.unpack_multi(raw)
        base = self.size() * block_id
        block = self._get_block(block_id)
        for i, r in enumerate(records):
            block[base + i] = r
    # [/load]

    def _get_filename(self, block_id):
        return self._db_dir.joinpath(f"{block_id:04}.db")

    # [index]
    def _build_index(self):
        seq_id = 0
        for (block_id, filename) in enumerate(
                sorted(self._db_dir.iterdir())
        ):
            self._load_block(block_id, filename)
            for record in self._get_block(block_id).values():
                key = self._record_cls.key(record)
                self._index[key] = seq_id
                seq_id += 1
    # [/index]
