import assert from 'assert'

import {
  OPS,
  OP_SHIFT,
  OP_WIDTH,
  NUM_REG
} from './architecture.js'

class Assembler {
  // [assemble]
  assemble (lines) {
    lines = this.cleanLines(lines)
    const labels = this.findLabels(lines)
    const instructions = lines.filter(line => !this.isLabel(line))
    const compiled = instructions.map(instr => this.compile(instr, labels))
    const program = this.instructionsToText(compiled)
    return program
  }

  cleanLines (lines) {
    return lines
      .map(line => line.trim())
      .filter(line => line.length > 0)
      .filter(line => !this.isComment(line))
  }

  isComment (line) {
    return line.startsWith('#')
  }
  // [/assemble]

  // [find-labels]
  findLabels (lines) {
    const result = {}
    let index = 0
    lines.forEach(line => {
      if (this.isLabel(line)) {
        const label = line.slice(0, -1)
        assert(!(label in result),
          `Duplicate label ${label}`)
        result[label] = index
      } else {
        index += 1
      }
    })
    return result
  }

  isLabel (line) {
    return line.endsWith(':')
  }
  // [/find-labels]

  // [compile]
  compile (instruction, labels) {
    const [op, ...args] = instruction.split(/\s+/)
    assert(op in OPS,
      `Unknown operation "${op}"`)
    let result = 0
    switch (OPS[op].fmt) {
      case '--':
        result = this.combine(
          OPS[op].code
        )
        break
      case 'r-':
        result = this.combine(
          this.register(args[0]),
          OPS[op].code
        )
        break
      case 'rr':
        result = this.combine(
          this.register(args[1]),
          this.register(args[0]),
          OPS[op].code
        )
        break
      case 'rv':
        result = this.combine(
          this.value(args[1], labels),
          this.register(args[0]),
          OPS[op].code
        )
        break
      default:
        assert(false,
          `Unknown instruction format ${OPS[op].fmt}`)
    }
    return result
  }
  // [/compile]

  // [combine]
  combine (...args) {
    assert(args.length > 0,
      'Cannot combine no arguments')
    let result = 0
    for (const a of args) {
      result <<= OP_SHIFT
      result |= a
    }
    return result
  }
  // [/combine]

  // [utilities]
  instructionsToText (program) {
    return program.map(op => op.toString(16).padStart(OP_WIDTH, '0'))
  }

  register (token) {
    assert(token[0] === 'R',
      `Register "${token}" does not start with 'R'`)
    const r = parseInt(token.slice(1))
    assert((0 <= r) && (r < NUM_REG),
      `Illegal register ${token}`)
    return r
  }

  value (token, labels) {
    if (token[0] !== '@') {
      return parseInt(token)
    }
    const labelName = token.slice(1)
    assert(labelName in labels,
      `Unknown label "${token}"`)
    return labels[labelName]
  }
  // [/utilities]
}

export default Assembler
