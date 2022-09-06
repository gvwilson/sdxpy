from architecture import RAM_LEN
from assembler import Assembler

DIVIDER = '.data'

class DataAllocator(Assembler):

    # [assemble]
    def assemble(self, lines):
        lines = self.clean_lines(lines)
        to_compile, to_allocate = self.split_allocations(lines)
        labels = self.find_labels(lines)
        instructions = [ln for ln in to_compile if not self.is_label(ln)]
        base_of_data = len(instructions)
        self.add_allocations(base_of_data, labels, to_allocate)
        compiled = [self.compile(instr, labels) for instr in instructions]
        program = self.instructions_to_text(compiled)
        return program
    # [/assemble]

    # [split-allocations]
    def split_allocations(self, lines):
        try:
            split = lines.index(DIVIDER)
            return lines[0:split], lines[split+1:]
        except ValueError:
            return lines, []
    # [/split-allocations]

    # [add-allocations]
    def add_allocations(self, base_of_data, labels, to_allocate):
        for alloc in to_allocate:
            fields = [a.strip() for a in alloc.split(":")]
            assert len(fields) == 2, \
                f"Invalid allocation directive '{alloc}'"
            lbl, num_words_text = fields
            assert lbl not in labels, \
                f"Duplicate label '{label}' in data allocation"
            num_words = int(num_words_text)
            assert (base_of_data + num_words) < RAM_LEN, \
                f"Allocation '{label}' requires too much memory"
            labels[lbl] = base_of_data
            base_of_data += num_words
    # [/add-allocations]

# [main]
if __name__ == "__main__":
    DataAllocator.main()
# [/main]
