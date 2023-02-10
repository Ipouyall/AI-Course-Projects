import unittest
from genetic import Equation, EquationBuilder


class TestEquationBuilder(unittest.TestCase):
    def setUp(self):
        self.equation = Equation(
            operands=[1, 2, 3, 4, 5, 6, 7, 8],
            operators=['+', '-', '*'],
            length=21,
            result=18019
        )
        equation_builder = EquationBuilder(self.equation)
        self.built_equation, self.iteration = equation_builder.find_equation()

    def test_correctness(self):
        eq = ' '.join(self.built_equation)
        print(f"test correctness")
        print("- Equation: ", eq)
        print("- Iteration: ", self.iteration)
        self.assertTrue(eval(eq) == self.equation.result)
        print()

    def test_satisfaction(self):
        eq = ' '.join(self.built_equation)
        print(f"test satisfaction")
        print("- Equation: ", eq)
        print("- Iteration: ", self.iteration)
        self.assertTrue(self.equation.is_satisfied(self.built_equation))
    print()


class TestEquationBuilder2(unittest.TestCase):
    def setUp(self):
        self.equation = Equation(
            operands=[1, 2, 3, 4, 5, 6, 7, 8, 11, 23, 89],
            operators=['+', '-', '%', '/'],
            length=11,
            result=1000000,
        )

    def test_auto_termination(self):
        equation_builder = EquationBuilder(self.equation)
        equation_builder.set_config(fitness_termination_threshold=50)
        built_equation, iteration = equation_builder.find_equation()
        self.assertTrue(built_equation is None)

    def test_iteration_termination(self):
        equation_builder = EquationBuilder(self.equation)
        equation_builder.set_config(fitness_termination_threshold=500)
        equation_builder.set_timeout_by_iterations(100)
        built_equation, iteration = equation_builder.find_equation()
        self.assertTrue(iteration == 100)
        self.assertTrue(built_equation is None)


if __name__ == '__main__':
    unittest.main()
