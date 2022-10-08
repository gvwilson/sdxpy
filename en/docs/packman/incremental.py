import importlib
import sys


# [main]
def main():
    versions = importlib.import_module(sys.argv[1]).versions
    packages = list(versions.keys())
    if len(sys.argv) > 2:
        packages.reverse()

    allowed = []
    examined = find(versions, packages, allowed, {}, 0)
    print(f"examined {examined}")
    for a in allowed:
        print(a)
# [/main]


# [find]
def find(constraints, remaining, allowed, current, so_far):
    so_far += 1
    if not remaining:
        allowed.append(current)

    else:
        package, rest = remaining[0], remaining[1:]
        for version in constraints[package]:
            candidate = current | {package: version}
            if compatible(constraints, candidate):
                so_far = find(constraints, rest, allowed, candidate, so_far)

    return so_far
# [/find]


def compatible(constraints, candidate):
    for package_i, version_i in candidate.items():
        lookup_i = constraints[package_i][version_i]
        for package_j, version_j in candidate.items():
            if package_i == package_j:
                continue
            if package_j not in lookup_i:
                continue
            if version_j not in lookup_i[package_j]:
                return False
    return True


if __name__ == "__main__":
    main()
