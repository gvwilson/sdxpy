def gen_sequences(left, right, all_seq,  current_seq):
    if (not left) and (not right):
        all_seq.append(current_seq)
    elif not left:
        all_seq.append([*current_seq, *right])
    elif not right:
        all_seq.append([*current_seq, *left])
    else:
        gen_sequences(left[1:], right, all_seq, current_seq + [left[0]])
        gen_sequences(left, right[1:], all_seq, current_seq + [right[0]])
    return all_seq

if __name__ == "__main__":
    all_sequences = gen_sequences("ab", "cd", [], [])
    printable = "\n".join('-'.join(x) for x in all_sequences)
    print(f"combination of 'ab' and 'cd'\n{printable}")
