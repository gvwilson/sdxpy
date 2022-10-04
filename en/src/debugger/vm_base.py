import sys

from architecture import NUM_REG, OP_MASK, OP_SHIFT, OPS, RAM_LEN, VMState

COLUMNS = 4
DIGITS = 8


class VirtualMachineBase:
    @classmethod
    def main(cls):
        assert len(sys.argv) == 3, f"Usage: {sys.argv[0]} input|- output|-"
        reader = open(sys.argv[1], "r") if (sys.argv[1] != "-") else sys.stdin
        writer = open(sys.argv[2], "w") if (sys.argv[2] != "-") else sys.stdout

        lines = [ln.strip() for ln in reader.readlines()]
        program = [int(ln, 16) for ln in lines if ln]

        vm = cls()
        vm.initialize(program)
        vm.run()
        vm.show(writer)
        
    def __init__(self):
        self.initialize([])
        self.prompt = ">>"

    def initialize(self, program):
        assert len(program) <= RAM_LEN, "Program is too long for memory"
        self.ram = [program[i] if (i < len(program)) else 0 for i in range(RAM_LEN)]
        self.ip = 0
        self.reg = [0] * NUM_REG

    def run(self):
        self.state = VMState.RUNNING
        while self.state != VMState.FINISHED:
            addr, op, arg0, arg1 = self.fetch()
            self.execute(op, arg0, arg1)

    def fetch(self):
        assert (
            0 <= self.ip < len(self.ram)
        ), f"Program counter {self.ip:06x} out of range 0..{len(self.ram):06x}"
        old_ip = self.ip
        instruction = self.ram[self.ip]
        self.ip += 1
        return (old_ip, *self.decode(instruction))

    def decode(self, instruction):
        op = instruction & OP_MASK
        instruction >>= OP_SHIFT
        arg0 = instruction & OP_MASK
        instruction >>= OP_SHIFT
        arg1 = instruction & OP_MASK
        return op, arg0, arg1

    def execute(self, op, arg0, arg1):
        if op == OPS["hlt"]["code"]:
            self.state = VMState.FINISHED

        elif op == OPS["ldc"]["code"]:
            self.assert_is_register(arg0)
            self.reg[arg0] = arg1

        elif op == OPS["ldr"]["code"]:
            self.assert_is_register(arg0)
            self.assert_is_register(arg1)
            self.reg[arg0] = self.ram[self.reg[arg1]]

        elif op == OPS["cpy"]["code"]:
            self.assert_is_register(arg0)
            self.assert_is_register(arg1)
            self.reg[arg0] = self.reg[arg1]

        elif op == OPS["str"]["code"]:
            self.assert_is_register(arg0)
            self.assert_is_register(arg1)
            self.assert_is_address(self.reg[arg1])
            self.ram[self.reg[arg1]] = self.reg[arg0]

        elif op == OPS["add"]["code"]:
            self.assert_is_register(arg0)
            self.assert_is_register(arg1)
            self.reg[arg0] += self.reg[arg1]

        elif op == OPS["sub"]["code"]:
            self.assert_is_register(arg0)
            self.assert_is_register(arg1)
            self.reg[arg0] -= self.reg[arg1]

        elif op == OPS["beq"]["code"]:
            self.assert_is_register(arg0)
            self.assert_is_address(arg1)
            if self.reg[arg0] == 0:
                self.ip = arg1

        elif op == OPS["bne"]["code"]:
            self.assert_is_register(arg0)
            self.assert_is_address(arg1)
            if self.reg[arg0] != 0:
                self.ip = arg1

        elif op == OPS["prr"]["code"]:
            self.assert_is_register(arg0)
            print(self.prompt, self.reg[arg0])

        elif op == OPS["prm"]["code"]:
            self.assert_is_register(arg0)
            self.assert_is_address(self.reg[arg0])
            print(self.prompt, self.ram[self.reg[arg0]])

        else:
            assert False, f"Unknown op {op:06x}"

    def show(self, writer):
        # Show IP and registers
        print(f"IP{' ' * 6}= {self.ip:06x}")
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

    def assert_is_register(self, reg):
        assert 0 <= reg < len(self.reg), f"Invalid register {reg:06x}"

    def assert_is_address(self, addr):
        assert 0 <= addr < len(self.ram), f"Invalid register {addr:06x}"


if __name__ == "__main__":
    VirtualMachineBase.main()
