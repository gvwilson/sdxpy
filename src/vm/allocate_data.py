import assert from 'assert'

import { RAM_LEN } from './architecture.js'
import Assembler from './assembler.js'

const DIVIDER = '.data'

class DataAllocator extends Assembler {
  // [assemble]
  assemble (lines) {
    lines = this.cleanLines(lines)
    const [toCompile, toAllocate] = this.splitAllocations(lines)
    const labels = this.findLabels(lines)
    const instructions = toCompile.filter(line => !this.isLabel(line))
    const baseOfData = instructions.length
    this.addAllocations(baseOfData, labels, toAllocate)
    const compiled = instructions.map(instr => this.compile(instr, labels))
    const program = this.instructionsToText(compiled)
    return program
  }
  // [/assemble]

  // [split-allocations]
  splitAllocations (lines) {
    const split = lines.indexOf(DIVIDER)
    if (split === -1) {
      return [lines, []]
    } else {
      return [lines.slice(0, split), lines.slice(split + 1)]
    }
  }
  // [/split-allocations]

  // [add-allocations]
  addAllocations (baseOfData, labels, toAllocate) {
    toAllocate.forEach(alloc => {
      const fields = alloc.split(':').map(a => a.trim())
      assert(fields.length === 2,
        `Invalid allocation directive "${alloc}"`)
      const [label, numWordsText] = fields
      assert(!(label in labels),
        `Duplicate label "${label}" in data allocation`)
      const numWords = parseInt(numWordsText)
      assert((baseOfData + numWords) < RAM_LEN,
        `Allocation "${label}" requires too much memory`)
      labels[label] = baseOfData
      baseOfData += numWords
    })
  }
  // [/add-allocations]
}

export default DataAllocator
