from dataclasses import dataclass


@dataclass
class Equation:
    length: int
    operators: list
    operands: list
    result: int

    def is_satisfied(self, chromosome: tuple) -> bool:
        if chromosome is None:
            return False
        return \
            self.result == eval(''.join(chromosome)) and \
            len(chromosome) == self.length and \
            all([int(operand) in self.operands for operand in chromosome[::2]]) and \
            all([operator in self.operators for operator in chromosome[1::2]])

