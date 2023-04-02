---
title: "A Database"
---

- interface_original.py: outline of key/value store
- just_dict_original.py: store records in a dictionary in memory (for developing tests)
- test_db_original.py: test save and load
- interface.py: refactor to use static methods of record class
- just_dict_refactored.py: showing cleaner interface
- records.py: store experimental records in "packed" fixed-width format
  - doesn't handle Unicode
- test_db.py: showing how to parameterize tests
- file_backed.py: read and write every time
- blocked.py: store records in blocks (but no I/O)
  - add some custom tests in test_db.py
- blocked_file.py: save and load blocks as needed
  - have to rebuild the index when we restart
- cleanup.py: delete unused blocks
  - it's not atomic
