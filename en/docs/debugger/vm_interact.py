import sys

from architecture import VMState
from vm_step import VirtualMachineStep


class VirtualMachineInteract(VirtualMachineStep):
    def __init__(self):
        super().__init__()
        self.handlers = {
            "d": self._do_disassemble,
            "dis": self._do_disassemble,
            "m": self._do_memory,
            "memory": self._do_memory,
            "n": self._do_next,
            "next": self._do_next,
            "q": self._do_quit,
            "quit": self._do_quit,
            "r": self._do_run,
            "run": self._do_run,
        }

    def run(self):
        self.state = VMState.STEPPING
        while self.state != VMState.FINISHED:
            if self.state == VMState.STEPPING:
                self.interact()
            instruction = self.ram[self.ip]
            self.ip += 1
            op, arg0, arg1 = self.decode(instruction)
            self.execute(op, arg0, arg1)

    def interact(self):
        prompt = "".join(sorted({key[0] for key in self.handlers}))
        interacting = True
        while interacting:
            try:
                command = input(f"{self.ip:06x} [{prompt}]> ").strip()
                if not command:
                    continue
                elif command not in self.handlers:
                    print(f"Unknown command {command}")
                else:
                    interacting = self.handlers[command](self.ip)
            except EOFError:
                self.state = VMState.FINISHED
                interacting = False

    def _do_disassemble(self, addr):
        print(self.disassemble(addr))
        return True

    def _do_memory(self, addr):
        self.show(sys.stdout)
        return True

    def _do_next(self, addr):
        self.state = VMState.STEPPING
        return False

    def _do_quit(self, addr):
        self.state = VMState.FINISHED
        return False

    def _do_run(self, addr):
        self.state = VMState.RUNNING
        return False


if __name__ == "__main__":
    VirtualMachineInteract.main()
