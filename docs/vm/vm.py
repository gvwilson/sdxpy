import assert from 'assert'

import {
  OPS
} from './architecture.js'

import VirtualMachineBase from './vm-base.js'

class VirtualMachine extends VirtualMachineBase {
  run () {
    let running = true
    while (running) {
      const [op, arg0, arg1] = this.fetch()
      switch (op) {
        case OPS.hlt.code:
          running = false
          break

        case OPS.ldc.code:
          this.assertIsRegister(arg0, op)
          this.reg[arg0] = arg1
          break

        // [skip]
        case OPS.ldr.code:
          this.assertIsRegister(arg0, op)
          this.assertIsRegister(arg1, op)
          this.reg[arg0] = this.ram[this.reg[arg1]]
          break

        case OPS.cpy.code:
          this.assertIsRegister(arg0, op)
          this.assertIsRegister(arg1, op)
          this.reg[arg0] = this.reg[arg1]
          break

        // [op_str]
        case OPS.str.code:
          this.assertIsRegister(arg0, op)
          this.assertIsRegister(arg1, op)
          this.assertIsAddress(this.reg[arg1], op)
          this.ram[this.reg[arg1]] = this.reg[arg0]
          break
        // [/op_str]

        // [op_add]
        case OPS.add.code:
          this.assertIsRegister(arg0, op)
          this.assertIsRegister(arg1, op)
          this.reg[arg0] += this.reg[arg1]
          break
        // [/op_add]

        case OPS.sub.code:
          this.assertIsRegister(arg0, op)
          this.assertIsRegister(arg1, op)
          this.reg[arg0] -= this.reg[arg1]
          break

        // [op_beq]
        case OPS.beq.code:
          this.assertIsRegister(arg0, op)
          this.assertIsAddress(arg1, op)
          if (this.reg[arg0] === 0) {
            this.ip = arg1
          }
          break
        // [/op_beq]

        case OPS.bne.code:
          this.assertIsRegister(arg0, op)
          this.assertIsAddress(arg1, op)
          if (this.reg[arg0] !== 0) {
            this.ip = arg1
          }
          break

        case OPS.prr.code:
          this.assertIsRegister(arg0)
          console.log(this.prompt, this.reg[arg0])
          break

        case OPS.prm.code:
          this.assertIsRegister(arg0)
          this.assertIsAddress(this.reg[arg0])
          console.log(this.prompt, this.ram[this.reg[arg0]])
          break
        // [/skip]

        default:
          assert(false, `Unknown op ${op}`)
          break
      }
    }
  }

  assertIsRegister (reg) {
    assert((0 <= reg) && (reg < this.reg.length),
      `Invalid register ${reg}`)
  }

  assertIsAddress (addr) {
    assert((0 <= addr) && (addr < this.ram.length),
      `Invalid register ${addr}`)
  }
}

export default VirtualMachine
