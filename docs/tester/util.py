def run_tests(available, prefix):
    """Run all the functions whose names start with the given prefix."""
    for name in [n for n in available if n.startswith(prefix)]:
        try:
            available[name]()
            print(f"pass: {name}")
        except AssertionError as e:
            print(f"fail: {name} {str(e)}")
        except Exception as e:
            print(f"error: {name} {str(e)}")
