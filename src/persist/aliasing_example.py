import sys

from aliasing import SaveAlias

word = "word"
child = [word, word]
parent = []
parent.append(parent)
parent.append(child)

saver = SaveAlias(sys.stdout)
saver.save(parent)
