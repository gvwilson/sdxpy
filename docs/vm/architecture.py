const OPS = {
  hlt: { code:  1, fmt: '--' }, // Halt program
  ldc: { code:  2, fmt: 'rv' }, // Load immediate
  ldr: { code:  3, fmt: 'rr' }, // Load register
  cpy: { code:  4, fmt: 'rr' }, // Copy register
  str: { code:  5, fmt: 'rr' }, // Store register
  add: { code:  6, fmt: 'rr' }, // Add
  sub: { code:  7, fmt: 'rr' }, // Subtract
  beq: { code:  8, fmt: 'rv' }, // Branch if equal
  bne: { code:  9, fmt: 'rv' }, // Branch if not equal
  prr: { code: 10, fmt: 'r-' }, // Print register
  prm: { code: 11, fmt: 'r-' }  // Print memory
}

const OP_MASK = 0xFF // select a single byte
const OP_SHIFT = 8   // shift up by one byte
const OP_WIDTH = 6   // op width in characters when printing

const NUM_REG = 4    // number of registers
const RAM_LEN = 256  // number of words in RAM

export {
  OPS,
  OP_MASK,
  OP_SHIFT,
  OP_WIDTH,
  NUM_REG,
  RAM_LEN
}
