def show_spread(left, middle, right):
    print(f"left {left} middle {middle} right {right}")

all_in_list = [1, 2, 3]
show_spread(*all_in_list)

all_in_dict = {"right": 30, "left": 10, "middle": 20}
show_spread(**all_in_dict)
