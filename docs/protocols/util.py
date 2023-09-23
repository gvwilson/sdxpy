def run_tests(whence, prefix):
    results = {"pass": 0, "fail": 0, "error": 0}
    for (name, test) in whence.items():
        if not name.startswith(prefix):
            continue
        try:
            test()
            results["pass"] += 1
        except AssertionError:
            results["fail"] += 1
        except Exception:
            results["error"] += 1
    print(f"pass {results['pass']}")
    print(f"fail {results['fail']}")
    print(f"error {results['error']}")
