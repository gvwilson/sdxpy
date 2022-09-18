from architecture import NUM_REG, OP_SHIFT, OP_WIDTH, OPS


class Assembler:

    # [assemble]
    def assemble(self, lines):
        lines = self.clean_lines(lines)
        labels = self.find_labels(lines)
        instructions = [ln for ln in lines if not self.is_label(ln)]
        compiled = [self.compile(instr, labels) for instr in instructions]
        program = self.instructions_to_text(compiled)
        return program

    def clean_lines(self, lines):
        lines = [ln.strip() for ln in lines]
        lines = [ln for ln in lines if len(ln) > 0]
        lines = [ln for ln in lines if not self.is_comment(ln)]
        return lines

    def is_comment(self, line):
        return line.startswith("#")

    # [/assemble]

    # [find-labels]
    def find_labels(self, lines):
        result = {}
        loc = 0
        for ln in lines:
            if self.is_label(ln):
                label = ln[:-1]
                assert label not in result, f"Duplicate label {label}"
                result[label] = loc
            else:
                loc += 1
        return result

    def is_label(self, line):
        return line.endswith(":")

    # [/find-labels]

    # [compile]
    def compile(self, instruction, labels):
        tokens = instruction.split()
        op, args = tokens[0], tokens[1:]
        assert op in OPS, f"Unknown operation {op}"

        result = 0
        if OPS[op]["fmt"] == "--":
            result = self.combine(OPS[op]["code"])

        elif OPS[op]["fmt"] == "r-":
            result = self.combine(self.register(args[0]), OPS[op]["code"])

        elif OPS[op]["fmt"] == "rr":
            result = self.combine(
                self.register(args[1]), self.register(args[0]), OPS[op]["code"]
            )

        elif OPS[op]["fmt"] == "rv":
            result = self.combine(
                self.value(args[1], labels), self.register(args[0]), OPS[op]["code"]
            )

        else:
            assert False, f"Unknown instruction format {OPS[op]['fmt']}"

        return result

    # [/compile]

    # [combine]
    def combine(self, *args):
        assert len(args) > 0, "Cannot combine no arguments"
        result = 0
        for a in args:
            result <<= OP_SHIFT
            result |= a
        return result

    # [/combine]

    # [utilities]
    def instructions_to_text(self, program):
        return [f"{op:06x}" for op in program]

    def register(self, token):
        assert token[0] == "R", f"Register '{token}' does not start with 'R'"
        r = int(token[1:])
        assert 0 <= r < NUM_REG, f"Illegal register {token}"
        return r

    def value(self, token, labels):
        if token[0] != "@":
            return int(token)

        lbl = token[1:]
        assert lbl in labels, f"Unknown label '{token}'"
        return labels[lbl]

    # [/utilities]

    # [driver]
    @classmethod
    def main(cls):
        import sys

        assert len(sys.argv) == 3, f"Usage: {sys.argv[0]} input|- output|-"
        reader = open(sys.argv[1], "r") if (sys.argv[1] != "-") else sys.stdin
        writer = open(sys.argv[2], "w") if (sys.argv[2] != "-") else sys.stdout
        lines = reader.readlines()
        assembler = cls()
        program = assembler.assemble(lines)
        for instruction in program:
            print(instruction, file=writer)

    # [/driver]


# [main]
if __name__ == "__main__":
    Assembler.main()
# [/main]
