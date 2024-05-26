# Tutorial information
slug = "sdxpy"
title = "Software Design by Example"
subtitle = "a tool-based introduction with Python"
repo = f"https://github.com/gvwilson/{slug}"
author = {
    "name": "Greg Wilson",
    "email": "gvwilson@third-bit.com",
    "site": "https://third-bit.com/",
}
lang = "en"
highlight = "tango.css"
plausible = "third-bit.com"
archive = f"{slug}-examples.zip"
isbn = "978-1032725253"
hardcopy = "https://www.routledge.com/Software-Design-by-Example-A-Tool-Based-Introduction-with-Python/Wilson/p/book/9781032725215"
cover = f"{slug}-cover.png"
timing = False

# Chapters.
chapters = [
    "intro",
    "oop",
    "dup",
    "glob",
    "parse",
    "test",
    "interp",
    "func",
    "protocols",
    "archive",
    "check",
    "template",
    "lint",
    "layout",
    "perf",
    "persist",
    "binary",
    "db",
    "build",
    "pack",
    "ftp",
    "http",
    "viewer",
    "undo",
    "vm",
    "debugger",
    "des",
    "finale",
]

# Appendices.
appendices = [
    "bib",
    "bonus",
    "syllabus",
    "license",
    "conduct",
    "contrib",
    "glossary",
    "colophon",
    "contents",
]

# Files to copy verbatim.
copy = [
    "*.as",
    "*.jpg",
    "*.js",
    "*.json",
    "*.mx",
    "*.out",
    "*.png",
    "*.py",
    "*.sh",
    "*.svg",
    "*.tll",
    "*.tll",
    "*.txt",
    "*.webp",
    "*.xml",
    "*.yml",
]

# Exclusions (don't process).
exclude = {
    "*.dot",
    "*.xml",
}

# Files known to be unincluded.
unincluded = {
    "src/archive/sample_dir.sh",
    "src/archive/sample_dir/a.txt",
    "src/archive/sample_dir/b.txt",
    "src/archive/sample_dir/sub_dir/c.txt",
    "src/binary/bird.txt",
    "src/binary/dynamic_format.out",
    "src/binary/dynamic_format.py",
    "src/binary/hex_notation.out",
    "src/binary/hex_notation.py",
    "src/binary/pack_unicode.out",
    "src/binary/pack_unicode.py",
    "src/bonus/attribute.out",
    "src/bonus/inheritance_example.out",
    "src/bonus/inheritance_example.sh",
    "src/build/concept_map.pdf",
    "src/build/dependencies.pdf",
    "src/build/double_linear_dep.sh",
    "src/build/topo_sort.pdf",
    "src/check/catalog.out",
    "src/check/catalog.sh",
    "src/check/check.sh",
    "src/check/contains.sh",
    "src/db/test_db.py",
    "src/db/test_records.py",
    "src/debugger/assembler.py",
    "src/debugger/fill_array.as",
    "src/debugger/fill_array.mx",
    "src/debugger/halt.as",
    "src/debugger/halt.mx",
    "src/debugger/print_num.as",
    "src/debugger/print_num.mx",
    "src/dup/dracula.txt",
    "src/dup/dup.out",
    "src/dup/grouped.sh",
    "src/dup/naive_dracula.pdf",
    "src/dup/naive_dracula.py",
    "src/dup/naive_dracula_unique.pdf",
    "src/dup/tests/a1.txt",
    "src/dup/tests/a2.txt",
    "src/dup/tests/a3.txt",
    "src/dup/tests/b1.txt",
    "src/dup/tests/b2.txt",
    "src/dup/tests/c1.txt",
    "src/finale/derosa.jpg",
    "src/func/adder.out",
    "src/func/adder.py",
    "src/func/dynamic.out",
    "src/func/dynamic.sh",
    "src/func/dynamic.tll",
    "src/func/func.sh",
    "src/glob/concept_map.pdf",
    "src/glob/fowler-refactoring.webp",
    "src/glob/gamma-design-patterns.webp",
    "src/glob/kerievsky-refactoring-to-patterns.webp",
    "src/glob/simpler_match.py",
    "src/glob/test_glob_null.py",
    "src/glob/test_simpler_match.py",
    "src/interp/concept_map.pdf",
    "src/interp/doubling.sh",
    "src/interp/recursive_evaluation.pdf",
    "src/interp/repeat_zero.out",
    "src/interp/repeat_zero.sh",
    "src/interp/stmt.py",
    "src/interp/vars.sh",
    "src/intro/.gitignore",
    "src/intro/comprehension.pdf",
    "src/layout/test_easy_mode.out",
    "src/layout/test_placed.out",
    "src/layout/test_wrapped.out",
    "src/lint/double.py",
    "src/lint/find_duplicate_keys.sh",
    "src/lint/find_unused_variables.sh",
    "src/oop/inherit_class.pdf",
    "src/oop/shapes_class.out",
    "src/oop/shapes_class.pdf",
    "src/oop/shapes_dict.out",
    "src/oop/shapes_dict.pdf",
    "src/pack/exhaustive.sh",
    "src/pack/manual.sh",
    "src/parse/concept_map.pdf",
    "src/parse/test_better_parser.py",
    "src/perf/analysis.pdf",
    "src/perf/analysis.py",
    "src/perf/make.out",
    "src/perf/make.py",
    "src/perf/timing.csv",
    "src/perf/timing.sh",
    "src/persist/concept_map.pdf",
    "src/persist/shared.pdf",
    "src/persist/shared.py",
    "src/persist/test_aliasing.out",
    "src/persist/test_aliasing.py",
    "src/persist/test_aliasing_wrong.out",
    "src/persist/test_builtin.out",
    "src/protocols/mock_object.out",
    "src/protocols/test_better_iterator.py",
    "src/protocols/util.py",
    "src/protocols/wrap_infinite.out",
    "src/protocols/wrap_infinite.sh",
    "src/template/conditional.sh",
    "src/template/loop.sh",
    "src/template/multiple_variables.sh",
    "src/template/single_constant.sh",
    "src/template/single_variable.sh",
    "src/template/static_text.sh",
    "src/test/concept_map.pdf",
    "src/test/locals.out",
    "src/undo/app.py",
    "src/undo/buffer.py",
    "src/undo/test_action.py",
    "src/undo/test_history.py",
    "src/undo/util.py",
    "src/undo/window.py",
    "src/viewer/.gitignore",
    "src/viewer/make_lines.py",
    "src/vm/count_up_assemble.sh",
    "src/vm/count_up_run.sh",
    "src/vm/fill_array.mx",
    "src/vm/fill_array_assemble.sh",
    "src/vm/fill_array_run.sh",
    "src/vm/halt.as",
    "src/vm/halt.mx",
    "src/vm/halt.out",
    "src/vm/halt_assemble.sh",
    "src/vm/halt_run.sh",
    "src/vm/print_r1.out",
    "src/vm/print_r1_assemble.sh",
    "src/vm/print_r1_run.sh",
}

# Theme information.
theme = "mccole"
src_dir = "src"
out_dir = "docs"
extension = "/"

# Enable various Markdown extensions.
markdown_settings = {
    "extensions": [
        "markdown.extensions.extra",
        "markdown.extensions.smarty",
        "pymdownx.superfences",
    ]
}

# Show theme.
if __name__ == "__main__":
    print(theme)
