from architecture import NUM_REG, OP_MASK, OP_SHIFT, RAM_LEN

COLUMNS = 4
DIGITS = 8


class VirtualMachineBase:
    def __init__(self):
        self.initialize([])
        self.prompt = ">>"

    # [skip]
    # [initialize]
    def initialize(self, program):
        assert len(program) <= RAM_LEN, "Program is too long for memory"
        self.ram = [program[i] if (i < len(program)) else 0 for i in range(RAM_LEN)]
        self.ip = 0
        self.reg = [0] * NUM_REG
    # [/initialize]

    # [fetch]
    def fetch(self):
        assert (
            0 <= self.ip < len(self.ram)
        ), f"Program counter {self.ip:06x} out of range 0..{len(self.ram):06x}"
        instruction = self.ram[self.ip]
        self.ip += 1
        op = instruction & OP_MASK
        instruction >>= OP_SHIFT
        arg0 = instruction & OP_MASK
        instruction >>= OP_SHIFT
        arg1 = instruction & OP_MASK
        return [op, arg0, arg1]
    # [/fetch]

    def show(self, writer):
        # Show registers
        for (i, r) in enumerate(self.reg):
            print(f"R{i:06x} = {r:06x}", file=writer)

        # How much memory to show
        top = max(i for (i, m) in enumerate(self.ram) if m != 0)

        # Show memory
        base = 0
        while base <= top:
            output = f"{base:06x}: "
            for i in range(COLUMNS):
                output += f"  {self.ram[base + i]:06x}"
            print(output, file=writer)
            base += COLUMNS

    @classmethod
    def main(cls):
        import sys

        assert len(sys.argv) == 3, f"Usage: {sys.argv[0]} input|- output|-"
        reader = open(sys.argv[1], "r") if (sys.argv[1] != "-") else sys.stdin
        writer = open(sys.argv[2], "w") if (sys.argv[2] != "-") else sys.stdout

        lines = [ln.strip() for ln in reader.readlines()]
        program = [int(ln, 16) for ln in lines if ln]
        vm = cls()
        vm.initialize(program)
        vm.run()
        vm.show(writer)
    # [/skip]


# [main]
if __name__ == "__main__":
    VirtualMachineBase.main()
# [/main]
