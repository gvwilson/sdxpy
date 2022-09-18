from architecture import OPS
from vm_base import VirtualMachineBase


class VirtualMachine(VirtualMachineBase):
    def run(self):
        running = True
        while running:
            op, arg0, arg1 = self.fetch()
            if op == OPS["hlt"]["code"]:
                running = False

            elif op == OPS["ldc"]["code"]:
                self.assert_is_register(arg0)
                self.reg[arg0] = arg1

            # [skip]
            elif op == OPS["ldr"]["code"]:
                self.assert_is_register(arg0)
                self.assert_is_register(arg1)
                self.reg[arg0] = self.ram[self.reg[arg1]]

            elif op == OPS["cpy"]["code"]:
                self.assert_is_register(arg0)
                self.assert_is_register(arg1)
                self.reg[arg0] = self.reg[arg1]

            # [op_str]
            elif op == OPS["str"]["code"]:
                self.assert_is_register(arg0)
                self.assert_is_register(arg1)
                self.assert_is_address(self.reg[arg1])
                self.ram[self.reg[arg1]] = self.reg[arg0]
            # [/op_str]

            # [op_add]
            elif op == OPS["add"]["code"]:
                self.assert_is_register(arg0)
                self.assert_is_register(arg1)
                self.reg[arg0] += self.reg[arg1]
            # [/op_add]

            elif op == OPS["sub"]["code"]:
                self.assert_is_register(arg0)
                self.assert_is_register(arg1)
                self.reg[arg0] -= self.reg[arg1]

            # [op_beq]
            elif op == OPS["beq"]["code"]:
                self.assert_is_register(arg0)
                self.assert_is_address(arg1)
                if self.reg[arg0] == 0:
                    self.ip = arg1
            # [/op_beq]

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
            # [/skip]

            else:
                assert False, f"Unknown op {op:06x}"

    def assert_is_register(self, reg):
        assert 0 <= reg < len(self.reg), f"Invalid register {reg:06x}"

    def assert_is_address(self, addr):
        assert 0 <= addr < len(self.ram), f"Invalid register {addr:06x}"


# [main]
if __name__ == "__main__":
    VirtualMachine.main()
# [/main]
