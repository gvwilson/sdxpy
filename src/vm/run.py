import assert from 'assert'
import fs from 'fs'

import VirtualMachine from './vm.js'

const main = () => {
  assert(process.argv.length >= 3,
    'Usage: as.js input [show]')
  const program = readProgram(process.argv[2])
  const vm = new VirtualMachine()
  vm.initialize(program)
  vm.run()
  if ((process.argv.length > 3) && (process.argv[3] === 'show')) {
    vm.show()
  }
}

const readProgram = (filename) => {
  return fs.readFileSync(filename, 'utf-8')
    .trim()
    .split('\n')
    .map(instr => parseInt(instr, 16))
}

main()
