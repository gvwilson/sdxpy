# [setup]
from pathlib import Path
import pytest
from unittest.mock import patch
from backup import backup

FILES = {
    "a.txt": "aaa",
    "b.txt": "bbb",
    "subdir/c.txt": "ccc"
}

@pytest.fixture
def our_fs(fs):
    for name, contents in FILES.items():
        fs.create_file(name, contents=contents)
# [/setup]

# [test]
def test_nested_example(our_fs):
    with patch("backup.current_time", return_value=1234):
        manifest = backup(".", "/backup")
    for filename, hash_code in manifest:
        assert Path("/backup", f"{hash_code}.bck").exists()
        assert Path("/backup", "1234.csv").exists()
# [/test]
