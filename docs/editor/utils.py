from string import digits as DIGITS

def make_lines(height, width):
    lines = []
    for i in range(2 * height):
        lines.append(''.join(DIGITS[(i + j) % len(DIGITS)] for j in range(i+1)))
    return lines
