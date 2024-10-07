# Abacus machine
# (c) 2024 Kimberly Wilber

from dataclasses import dataclass, field
from collections import defaultdict
from functools import wraps, partial
import re

# An Abacus Machine is a machine with infinite numeric registers
# and a program counter.
@dataclass
class AbacusMachine:
    pc: str = "start"
    regs: defaultdict = field(default_factory=lambda: defaultdict(lambda: 0))
    def __repr__(self):
        return rf"AbacusMachine(pc={self.pc!r:10}  regs={dict(self.regs)!r})"
    def op_inc(self, reg, next_line):
        self.regs[reg] += 1
        self.pc = next_line
    def op_ifzdec(self, cmpreg, lineTrue, decreg, lineFalse):
        if self.regs[cmpreg] == 0:
            self.pc = lineTrue
        else:
            self.regs[decreg] -= 1
            self.pc = lineFalse
    def step1(self, program, verbose=True):
        "Evaluate one step"
        pc = self.pc
        if pc not in program:
            raise StopIteration("Halted")
        opcode, *argv = program[pc]
        getattr(self, "op_"+opcode)(*argv)
        if verbose:
            print(f"{' '.join(program[pc]):30} => {self}")

def parse_program(program):
    """
    Parse a program, returning {"line_num": callable()}
    """
    parsed_program = {}
    line_regex = re.compile(r"\s*(\w+):\s*(\w+)\s*(.*)(#.*)?")
    for line_str in program.split("\n"):
        if (line := line_regex.fullmatch(line_str)):
            line_num, opcode, argv, comment = line.groups()
            argv = re.split(r"\s+", argv)
            parsed_program[line_num] = (opcode, *argv)
    return parsed_program

prog = parse_program(r"""
# Testing
start: inc 1 3
3:     inc 1 zz
zz:    inc 1 start
""")
print(prog)
# => {'start': ('inc', '1', '3'),
#     '3':     ('inc', '1', 'zz'),
#     'zz': ('inc', '1', 'start')}

abacus = AbacusMachine()
for _ in range(10):
    abacus.step1(prog, verbose=True)
# Output:
#   inc 1 3                        => AbacusMachine(pc='3'         regs={'1': 1})
#   inc 1 zz                       => AbacusMachine(pc='zz'        regs={'1': 2})
#   inc 1 start                    => AbacusMachine(pc='start'     regs={'1': 3})
#   inc 1 3                        => AbacusMachine(pc='3'         regs={'1': 4})
#   inc 1 zz                       => AbacusMachine(pc='zz'        regs={'1': 5})
#   inc 1 start                    => AbacusMachine(pc='start'     regs={'1': 6})
#   inc 1 3                        => AbacusMachine(pc='3'         regs={'1': 7})
#   inc 1 zz                       => AbacusMachine(pc='zz'        regs={'1': 8})
#   inc 1 start                    => AbacusMachine(pc='start'     regs={'1': 9})
#   inc 1 3                        => AbacusMachine(pc='3'         regs={'1': 10})