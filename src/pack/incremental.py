import importlib
import json
import sys

# [main]
def main():
    manifest = json.load(sys.stdin)
    packages = list(manifest.keys())
    if len(sys.argv) > 1:
        packages.reverse()

    accum = []
    count = find(manifest, packages, accum, [], 0)

    print(f"count {count}")
    for a in accum:
        print(a)
# [/main]

# [find]
def find(manifest, remaining, accum, current, count):
    count += 1
    if not remaining:
        accum.append(current)
    else:
        head, tail = remaining[0], remaining[1:]
        for version in manifest[head]:
            candidate = current + [(head, version)]
            if compatible(manifest, candidate):
                count = find(
                    manifest, tail, accum, candidate, count
                )
    return count
# [/find]

def compatible(manifest, candidate):
    for package_i, version_i in candidate:
        lookup_i = manifest[package_i][version_i]
        for package_j, version_j in candidate:
            if package_i == package_j:
                continue
            if package_j not in lookup_i:
                continue
            if version_j not in lookup_i[package_j]:
                return False
    return True

if __name__ == "__main__":
    main()
