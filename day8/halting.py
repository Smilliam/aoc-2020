import copy
import logging

logging.basicConfig()
logger = logging.getLogger('halting')
logger.setLevel('INFO')

class Computer():
    def __init__(self, program):
        self.program = program
        self.reset() # this is silly but we need to reset the instruction exec count
        self.pc = 0
        self.accumulator = 0

    def reset(self):
        self.pc = 0
        self.accumulator = 0
        for ins in self.program:
            ins.reset()

    def run(self):
        cur_instruction = self.program[self.pc]
        while not cur_instruction.times_executed():
            self.pc, self.accumulator = cur_instruction.execute(self.pc, self.accumulator)
            if self.pc >= len(program):
                return True
            cur_instruction = self.program[self.pc]

        return False

class Instruction():
    def __init__(self, line):
        split = line.split()
        self.kind = split[0]
        self.val  = int(split[1])
        self._times_executed = 0

    def execute(self, pc, accumulator):
        self._times_executed += 1
        if self.kind == 'acc':
            return pc + 1, accumulator + self.val
        elif self.kind == 'jmp':
            return pc + self.val, accumulator
        else: # nop
            return pc + 1, accumulator

    def times_executed(self):
        return self._times_executed

    def reset(self):
        self._times_executed = 0

    def __repr__(self):
        return f'[{self.kind}, {self.val}]'

def edit_program(program, num_to_skip):
    count = 0
    for ins in program:
        count += 1
        if ins.kind == 'acc':
            continue

        if num_to_skip > 0:
            num_to_skip -= 1
            continue
        if ins.kind == 'jmp':
            logger.debug(f'changing jmp to nop at {count-1}')
            ins.kind = 'nop'
            break
        elif ins.kind == 'nop':
            logger.debug(f'changing nop to jmp at {count-1}')
            ins.kind = 'jmp'
            break

    return program, count-1

def parse_args():
    import argparse
    parser = argparse.ArgumentParser()

    parser.add_argument('in_file', type=str)

    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()

    program = []
    with open(args.in_file, 'r') as ff:
        for line in ff:
            program.append(Instruction(line))

    computer = Computer(program)
    computer.run()
    print(computer.accumulator)

    computer.reset()
    skips = 0
    while not computer.run():
        logger.debug(f'making next computer. Skipping {skips}')
        if skips > len(program):
            break

        next_program, idx = edit_program(copy.deepcopy(program), skips)
        logger.debug(next_program)
        logger.debug(f'{next_program[idx].kind}')
        skips += 1
        computer = Computer(next_program)

    print(computer.accumulator)
