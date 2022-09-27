from pathlib import Path

def cache_open(cache, filename, mode):
    if not filename.endswith(cache.CACHE_SUFFIX):
        filename = f"{filename}.{CACHE_SUFFIX}"
    filename = Path(filename)
    if not filename.exists():
        raise FileNotFoundError(f"No local cache file {filename}")
    with open(filename, "r") as reader:
        identifier = reader.read().strip()
        cache_path = cache.get_cache_path(identifier)
        return open(cache_path, mode)

def cache_save(cache, filename):
    identifier = cache.add(filename)
    identifier_file = Path(f"{filename}.{CACHE_SUFFIX}")
    with open(identifier_file, "w") as writer:
        writer.write(identifier)
