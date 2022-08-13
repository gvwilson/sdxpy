import importlib
import sys


def main():
    """Main driver."""
    assert len(sys.argv) > 1, "Missing module name"
    module = importlib.import_module(sys.argv[1])
    try:
        builder = module.make_builder(sys.argv[2:])
        builder.build()
    except Exception as exc:
        print(str(exc), file=sys.stderr)


if __name__ == "__main__":
    main()
