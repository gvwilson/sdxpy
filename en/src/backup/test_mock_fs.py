from pathlib import Path

def test_simple_example(fs):
    sentence = "This file contains one sentence."
    fs.create_file("alpha.txt", contents=sentence)
    assert Path("alpha.txt").exists()
    with open("alpha.txt", "r") as reader:
        assert reader.read() == sentence
