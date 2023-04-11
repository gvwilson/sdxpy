def show_args(title, *args, **kwargs):
    print(f"{title} args '{args}' and kwargs '{kwargs}'")

show_args("nothing")
show_args("one unnamed argument", 1)
show_args("one named argument", second="2")
show_args("one of each", 3, fourth="4")

a_list = [7, 8]
a_dict = {"nine": 9, "ten": 10}
show_args("direct", a_list, a_dict)
show_args("spreading", *a_list, **a_dict)
