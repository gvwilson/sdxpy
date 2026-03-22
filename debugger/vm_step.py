import sys

from architecture import OPS, VMState
from vm_base import VirtualMachineBase

# mccole:lookup
OPS_LOOKUP = {value["code"]: key for key, value in OPS.items()}
# mccole:/lookup

# mccole:derive
class VirtualMachineStep(VirtualMachineBase):
# mccole:/derive
    # mccole:init
    def __init__(self, reader=input, writer=sys.stdout):
        super().__init__(writer)
        self.reader = reader
    # mccole:/init

    # mccole:run
    def run(self):
        self.state = VMState.STEPPING
        while True:
            if self.state == VMState.STEPPING:
                self.interact(self.ip)
            if self.state == VMState.FINISHED:
                break
            instruction = self.ram[self.ip]
            self.ip += 1
            op, arg0, arg1 = self.decode(instruction)
            self.execute(op, arg0, arg1)
    # mccole:/run

    # mccole:interact
    def interact(self, addr):
        while self.state == VMState.STEPPING:
            try:
                command = self.read(f"{addr:06x} [dmqrs]> ")
                if not command:
                    continue
                elif command in {"d", "dis"}:
                    self.write(self.disassemble(addr, self.ram[addr]))
                elif command in {"m", "memory"}:
                    self.show()
                elif command in {"q", "quit"}:
                    self.state = VMState.FINISHED
                    break
                elif command in {"r", "run"}:
                    self.state = VMState.RUNNING
                    break
                elif command in {"s", "step"}:
                    break
                else:
                    self.write(f"Unknown command '{command}'")
            except EOFError:
                self.state = VMState.FINISHED
    # mccole:/interact

    # mccole:disassemble
    def disassemble(self, addr, instruction):
        op, arg0, arg1 = self.decode(instruction)
        assert op in OPS_LOOKUP, f"Unknown op code {op} at {addr}"
        return f"{OPS_LOOKUP[op]} | {arg0} | {arg1}"
    # mccole:/disassemble

    # mccole:read
    def read(self, prompt):
        return self.reader(prompt).strip()
    # mccole:/read

if __name__ == "__main__":
    VirtualMachineStep.main()
