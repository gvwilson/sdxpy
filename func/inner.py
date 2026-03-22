def outer(value):
    def inner(current):
        print(f"inner sum is {current + value}")
    
    print(f"outer value is {value}")
    for i in range(3):
        inner(i)

outer(10)
