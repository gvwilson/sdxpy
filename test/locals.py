def show_locals(low, high):
    print(f"start: {locals()}")
    for i in range(low, high):
        print(f"loop {i}: {locals()}")
    print(f"end: {locals()}")

show_locals(1, 3)
