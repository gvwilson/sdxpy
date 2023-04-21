from pathlib import Path

from interface import Database

# [class]
class Blocked(Database):
    RECORDS_PER_BLOCK = 2

    @staticmethod
    def size():
        return Blocked.RECORDS_PER_BLOCK

    def __init__(self, record_cls):
        super().__init__(record_cls)
        self._next = 0
        self._index = {}
        self._blocks = []

    def num_blocks(self):
        return len(self._blocks)

    def num_records(self):
        return len(self._index)
# [/class]

    # [add]
    def add(self, record):
        key = self._record_cls.key(record)
        seq_id = self._next_seq_id()
        self._index[key] = seq_id
        block_id = self._get_block_id(seq_id)
        block = self._get_block(block_id)
        block[seq_id] = record
    # [/add]

    # [get]
    def get(self, key):
        if key not in self._index:
            return None
        seq_id = self._index[key]
        block_id = self._get_block_id(seq_id)
        block = self._get_block(block_id)
        return block[seq_id]
    # [/get]

    # [helper]
    def _next_seq_id(self):
        seq_id = self._next
        self._next += 1
        return seq_id

    def _get_block_id(self, seq_id):
        return seq_id // Blocked.RECORDS_PER_BLOCK

    def _get_block(self, block_id):
        while block_id >= len(self._blocks):
            self._blocks.append({})
        return self._blocks[block_id]
    # [/helper]
