import sys

from architecture import OPS
from vm import VirtualMachine


class VirtualMachineBreak(VirtualMachine):
    def run(self):
        self.set_break(0)
        running = True
        while running:
            addr, op, arg0, arg1 = self.fetch()
            if op == OPS["brk"]["code"]:
                running = self.at_break(addr)
            else:
                running = self.execute(op, arg0, arg1)

    def at_break(self, addr):
        pass

    def clear_break(self, addr):
        pass

    def set_break(self, addr):
        pass

    def show_memory(self):
        self.show_memory(sys.stdout)

    def single_step(self):
        pass
