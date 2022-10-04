import sys

from architecture import OPS
from vm_interact import VMState, VirtualMachineInteract


class VirtualMachineBreak(VirtualMachineInteract):
    def __init__(self):
        super().__init__()
        self.breaks = {}
        self.handlers |= {
            "b": self._do_add_breakpoint,
            "break": self._do_add_breakpoint,
            "c": self._do_clear_breakpoint,
            "clear": self._do_clear_breakpoint,
        }

    def show(self, writer):
        super().show(writer)
        if self.breaks:
            print("-" * 6)
            for key, instruction in self.breaks.items():
                print(f"{key:06x}: {self.disassemble(instruction)}")

    def run(self):
        self.state = VMState.STEPPING
        while self.state != VMState.FINISHED:
            instruction = self.ram[self.ip]
            op, arg0, arg1 = self.decode(instruction)

            if op == OPS["brk"]["code"]:
                original = self.breaks[self.ip]
                self.interact()
                op, arg0, arg1 = self.decode(original)
                self.ip += 1
                self.execute(op, arg0, arg1)

            else:
                if self.state == VMState.STEPPING:
                    self.interact()
                self.ip += 1
                self.execute(op, arg0, arg1)

    def _do_add_breakpoint(self, addr):
        if self.ram[addr] == OPS["brk"]["code"]:
            return
        assert addr not in self.breaks, f"Inconsistent breakpoint state for {addr}"
        self.breaks[addr] = self.ram[addr]
        self.ram[addr] = OPS["brk"]["code"]
        return True

    def _do_clear_breakpoint(self, addr):
        if self.ram[addr] != OPS["brk"]["code"]:
            return
        assert addr in self.breaks, f"Inconsistent breakpoint state for {addr}"
        self.ram[addr] = self.breaks[addr]
        del self.breaks[addr]
        return True


if __name__ == "__main__":
    VirtualMachineBreak.main()
