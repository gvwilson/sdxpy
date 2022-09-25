from collections import Counter

from gen_sequences import gen_sequences

def read_counter(global_state, local_state):
    local_state["tmp_counter"] = global_state["counter"]

def inc_counter(global_state, local_state):
    local_state["tmp_counter"] = local_state["tmp_counter"] + 1
    
def write_counter(global_state, local_state):
    global_state["counter"] = local_state["tmp_counter"]

threads = [
    [("left", read_counter), ("left", inc_counter), ("left", write_counter)],
    [("right", read_counter), ("right", inc_counter), ("right", write_counter)]
]

sequences = gen_sequences(threads[0], threads[1], [], [])
result = Counter()
for seq in sequences:
    global_state = {"counter": 0}
    local_state = {"left": {}, "right": {}}
    for (name, func) in seq:
        func(global_state, local_state[name])
    result[global_state["counter"]] += 1

print(f"{len(sequences)} sequences")
for key in sorted(result.keys()):
    print(f"{key}: {result[key]}")
