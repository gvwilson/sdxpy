import importlib
import sys


# [main]
def main():
    versions = importlib.import_module(sys.argv[1]).versions
    possible = make_possibilities(versions)
    print(f"{len(possible)} possibilities")
    actual = [p for p in possible if compatible(versions, p)]
    for a in actual:
        print(a)
# [/main]


# [possible]
def make_possibilities(versions):
    available = [(k, set(versions[k].keys())) for k in versions]
    allowed = []
    _make_possible(available, allowed, {})
    return allowed


def _make_possible(available, allowed, current):
    if not available:
        allowed.append(current)
        return

    (package, versions), remainder = available[0], available[1:]
    for v in versions:
        _make_possible(remainder, allowed, current | {package: v})
# [/possible]


# [compatible]
def compatible(constraints, combination):
    for package_i, version_i in combination.items():
        lookup_i = constraints[package_i][version_i]
        for package_j, version_j in combination.items():
            if package_i == package_j:
                continue
            if package_j not in lookup_i:
                continue
            if version_j not in lookup_i[package_j]:
                return False
    return True
# [/compatible]


if __name__ == "__main__":
    main()
