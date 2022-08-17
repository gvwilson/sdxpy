OPS = {
  "hlt": { "code":  1, "fmt": "--" }, # Halt program
  "ldc": { "code":  2, "fmt": "rv" }, # Load immediate
  "ldr": { "code":  3, "fmt": "rr" }, # Load register
  "cpy": { "code":  4, "fmt": "rr" }, # Copy register
  "str": { "code":  5, "fmt": "rr" }, # Store register
  "add": { "code":  6, "fmt": "rr" }, # Add
  "sub": { "code":  7, "fmt": "rr" }, # Subtract
  "beq": { "code":  8, "fmt": "rv" }, # Branch if equal
  "bne": { "code":  9, "fmt": "rv" }, # Branch if not equal
  "prr": { "code": 10, "fmt": "r-" }, # Print register
  "prm": { "code": 11, "fmt": "r-" }  # Print memory
}

OP_MASK = 0xFF # select a single byte
OP_SHIFT = 8   # shift up by one byte
OP_WIDTH = 6   # op width in characters when printing

NUM_REG = 4    # number of registers
RAM_LEN = 256  # number of words in RAM
