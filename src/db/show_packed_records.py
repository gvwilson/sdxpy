from record import Experiment

ex = Experiment("abcdef", 12345, [6, 7])
print(Experiment.pack(ex).replace('\0', '.'))
