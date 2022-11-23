import sys

from architecture import OPS, VMState
from vm_base import VirtualMachineBase

# [lookup]
OPS_LOOKUP = {value["code"]: key for key, value in OPS.items()}
# [/lookup]

class VirtualMachineStep(VirtualMachineBase):
    # [run]
    def run(self):
        self.state = VMState.STEPPING
        while self.state != VMState.FINISHED:
            self.interact(self.ip)
            if self.state == VMState.STEPPING:
                instruction = self.ram[self.ip]
                self.ip += 1
                op, arg0, arg1 = self.decode(instruction)
                self.execute(op, arg0, arg1)
    # [/run]

    # [interact]
    def interact(self, addr):
        while self.state == VMState.STEPPING:
            try:
                command = input(f"{addr:06x} [dmn]> ").strip()
                if not command:
                    continue
                elif command in {"d", "dis"}:
                    print(self.disassemble(self.ram[addr]))
                elif command in {"m", "memory"}:
                    self.show(sys.stdout)
                elif command in {"n", "next"}:
                    break
                elif command in {"q", "quit"}:
                    self.state = VMState.FINISHED
                    break
                else:
                    print(f"Unknown command '{command}'")
            except EOFError:
                self.state = VMState.FINISHED
    # [/interact]

    # [disassemble]
    def disassemble(self, instruction):
        op, arg0, arg1 = self.decode(instruction)
        assert op in OPS_LOOKUP, f"Unknown op code {op} at {addr}"
        return f"{OPS_LOOKUP[op]} | {arg0} | {arg1}"
    # [/disassemble]
        

if __name__ == "__main__":
    VirtualMachineStep.main()
