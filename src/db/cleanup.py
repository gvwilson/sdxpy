from pathlib import Path

from blocked_file import BlockedFile

class Cleanup(BlockedFile):
    def add(self, record):
        super().add(record)
        self._cleanup()

    # [cleanup]
    def _cleanup(self):
        new_seq = {
            o: i for i, o in enumerate(self._index.values())
        }
        keep = {self._get_block_id(o) for o in new_seq}

        renaming = {o: i for i, o in enumerate(list(sorted(keep)))}
        garbage_ids = {
            i for i in range(len(self._blocks))
            if i not in renaming
        }

        self._delete_blocks(garbage_ids)
        self._rename_blocks(renaming)

        new_index = {
            k: new_seq[self._index[k]] for k in self._index
        }
        self._index = new_index
        self._next = len(self._index)
    # [/cleanup]

    def _delete_blocks(self, garbage_ids):
        for i in garbage_ids:
            filename = self._get_filename(i)
            print("...deleting", filename)
            Path(filename).unlink()

    def _rename_blocks(self, renaming):
        for old_id, new_id in sorted(renaming.items()):
            old_filename = self._get_filename(old_id)
            new_filename = self._get_filename(new_id)
            if old_filename != new_filename:
                print("...moving", old_filename, new_filename)
                Path(old_filename).rename(new_filename)
