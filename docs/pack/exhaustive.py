import itertools
import json
import sys

# [main]
def main():
    manifest = json.load(sys.stdin)
    possible = make_possibilities(manifest)
    print(f"{len(possible)} possibilities")
    allowed = [p for p in possible if compatible(manifest, p)]
    print(f"{len(allowed)} allowed")
    for a in allowed:
        print(a)
# [/main]

# [possible]
def make_possibilities(manifest):
    available = []
    for package, versions in manifest.items():
        available.append([(package, v) for v in versions])
    return list(itertools.product(*available))
# [/possible]

# [compatible]
def compatible(manifest, combination):
    for package_i, version_i in combination:
        lookup_i = manifest[package_i][version_i]
        for package_j, version_j in combination:
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
