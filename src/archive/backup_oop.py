import csv
import shutil
import sys
import time
from pathlib import Path

from hash_all import hash_all

# [base]
class Archive:
    def __init__(self, source_dir):
        self._source_dir = source_dir

    def backup(self):
        manifest = hash_all(self._source_dir)
        self._write_manifest(manifest)
        self._copy_files(manifest)
        return manifest
# [/base]


class ArchiveLocal(Archive)
    def __init__(self, source_dir, backup_dir):
        super().__init__()
        self._backup_dir = backup_dir

    def _copy_files(self, manifest):
        for (filename, hash_code) in manifest:
            source_path = Path(self._source_dir, filename)
            backup_path = Path(self._backup_dir, f"{hash_code}.bck")
            if not backup_path.exists():
                shutil.copy(source_path, backup_path)

    def _write_manifest(self, manifest):
        t = self._timestamp()
        backup_dir = Path(self._backup_dir)
        if not backup_dir.exists():
            backup_dir.mkdir()
        manifest_file = Path(backup_dir, f"{timestamp}.csv")
        with open(manifest_file, "w") as raw:
            writer = csv.writer(raw)
            writer.writerow(["filename", "hash"])
            writer.writerows(manifest)

    def _timestamp(self):
        return f"{time.time()}".split(".")[0]

# [use]
def analyze_and_save(options, archiver):
    data = read_data(options)
    results = analyze_data(data)
    save_everything(result)
    archiver.backup()
# [/use]

if __name__ == "__main__":
    assert len(sys.argv) == 3, "Usage: backup.py source_dir backup_dir"
    source_dir = sys.argv[1]
    backup_dir = sys.argv[2]
    # [create]
    archiver = ArchiveLocal(source_dir, backup_dir)
    # [/create]
    analyze_and_save({}, archiver)
