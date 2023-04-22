import sys
from architecture import NUM_REG, OP_SHIFT, OPS

# [class]
class Assembler:
    def assemble(self, lines):
        lines = self._get_lines(lines)
        labels = self._find_labels(lines)
        instructions = [ln for ln in lines if not self._is_label(ln)]
        compiled = [self._compile(instr, labels) for instr in instructions]
        program = self._to_text(compiled)
        return program
# [/class]

    # [labels]
    def _find_labels(self, lines):
        result = {}
        loc = 0
        for ln in lines:
            if self._is_label(ln):
                label = ln[:-1].strip()
                assert label not in result, f"Duplicate label {label}"
                result[label] = loc
            else:
                loc += 1
        return result

    def _is_label(self, line):
        return line.endswith(":")
    # [/labels]

    # [compile]
    def _compile(self, instruction, labels):
        tokens = instruction.split()
        op, args = tokens[0], tokens[1:]
        assert op in OPS, f"Unknown operation {op}"
        fmt = OPS[op]["fmt"]

        if fmt == "--":
            return self._combine(OPS[op]["code"])

        elif fmt == "r-":
            return self._combine(self._reg(args[0]), OPS[op]["code"])

        elif fmt == "rr":
            return self._combine(
                self._reg(args[1]), self._reg(args[0]), OPS[op]["code"]
            )

        elif fmt == "rv":
            return self._combine(
                self._value(args[1], labels), self._reg(args[0]), OPS[op]["code"]
            )
    # [/compile]

    # [value]
    def _value(self, token, labels):
        if token[0] != "@":
            return int(token)
        lbl = token[1:]
        assert lbl in labels, f"Unknown label '{token}'"
        return labels[lbl]
    # [/value]

    # [combine]
    def _combine(self, *args):
        assert len(args) > 0, "Cannot combine no arguments"
        result = 0
        for a in args:
            result <<= OP_SHIFT
            result |= a
        return result
    # [/combine]

    def _to_text(self, program):
        return [f"{op:06x}" for op in program]

    def _get_lines(self, lines):
        lines = [ln.strip() for ln in lines]
        lines = [ln for ln in lines if len(ln) > 0]
        lines = [ln for ln in lines if not self._is_comment(ln)]
        return lines

    def _is_comment(self, line):
        return line.startswith("#")

    def _reg(self, token):
        assert token[0] == "R", f"Register '{token}' does not start with 'R'"
        r = int(token[1:])
        assert 0 <= r < NUM_REG, f"Illegal register {token}"
        return r

def main(assembler_cls):
    assert len(sys.argv) == 3, f"Usage: {sys.argv[0]} input|- output|-"
    reader = open(sys.argv[1], "r") if (sys.argv[1] != "-") else sys.stdin
    writer = open(sys.argv[2], "w") if (sys.argv[2] != "-") else sys.stdout
    lines = reader.readlines()
    assembler = assembler_cls()
    program = assembler.assemble(lines)
    for instruction in program:
        print(instruction, file=writer)

if __name__ == "__main__":
    main(Assembler)
