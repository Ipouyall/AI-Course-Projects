import random
from time import time
from .equation import Equation


def _make_random_chromosome(length: int, operands: list, operators: list):
    return tuple(random.choice(operands) if i % 2 == 0 else random.choice(operators) for i in range(length))


def generate_population(length: int, operands: list, operators: list, size: int):
    return [_make_random_chromosome(length, operands, operators) for _ in range(size)]


def _calculate_fitness(chromosome: list, target: int):
    return -1 * abs(target - eval(''.join(chromosome)))


def _crossover(first_chromosome: tuple, second_chromosome: tuple, target: int):
    crossover_points = set(
        random.sample(range(1, len(first_chromosome) - 1), random.randint(1, len(first_chromosome) // 2))
    )
    first_child, second_child = list(first_chromosome), list(second_chromosome)
    for i in crossover_points:
        first_child[i], second_child[i] = second_child[i], first_child[i]

    return tuple(
        first_child if
        _calculate_fitness(first_child, target) > _calculate_fitness(second_child, target)
        else second_child)


def _make_mating_pool(population_size: int, population: list, fitnesses: list, max_sample: int = 10):
    mating_pool = []
    min_val = abs(min(fitnesses) - 1)
    coefficient = (max_sample - 1) / (max(fitnesses) - min(fitnesses))

    for candidate, fitness in zip(population, fitnesses):
        mating_pool.extend([candidate] * int(1 + (fitness + min_val) * coefficient))

    return random.sample(mating_pool, k=min(population_size, len(mating_pool)))


class EquationBuilder:
    __config = {
        "crossover_probability": 0.8,
        "carry_percentage": 0.25,
        "population_size": 800,
        "generate_new_population_rate": 0.1,
        "fitness_termination_threshold": 60,
    }
    __setattr = [
        "cross_over_probability",
        "carry_percentage",
        "population_size",
        "generate_new_population_rate",
        "fitness_termination_threshold",
    ]
    
    def __init__(self, _equation: Equation):
        if _equation.length % 2 == 0:
            raise ValueError("Equation length must be odd")
        self.equation_length = _equation.length
        self.operands = list(map(str, _equation.operands))
        self.operators = _equation.operators
        self.target = _equation.result

        self.population = generate_population(
            self.equation_length,
            self.operands,
            self.operators,
            self.get_config("population_size")
        )
        self.timeout = lambda: False
    
    def find_equation(self):
        """Create a new generation of chromosomes, and make it better in every iteration"""
        iteration_num = 0
        fr_threshold = self.get_config("fitness_termination_threshold")
        fitness_history = {}
        while not self.timeout():
            iteration_num += 1
            tended, chromosome = self._next_iteration()
            if tended is True:
                return chromosome, iteration_num

            if tended in fitness_history:
                fitness_history[tended] += 1
            else:
                fitness_history[tended] = 1

            if fitness_history[tended] > fr_threshold:
                break

        print(f"Timeout after {iteration_num} iterations")
        print(f"- Best chromosome: {chromosome}")
        print(f"- Fitness: {tended}")
        return None, iteration_num

    def _next_iteration(self):
        self.population.extend(
            generate_population(
                self.equation_length,
                self.operands,
                self.operators,
                int(self.get_config("population_size") * self.get_config("generate_new_population_rate"))
            ))

        random.shuffle(self.population)
        fitnesses = [self._calculate_fitness(chromosome) for chromosome in self.population]
        straight_to_next_gen_count = int(self.get_config("population_size") * self.get_config("carry_percentage"))
        straight_chromosomes = sorted(
            zip(fitnesses, self.population), reverse=True, key=lambda x: x[0]
        )[:straight_to_next_gen_count]
        
        best_fitness = straight_chromosomes[0][0]
        best_chromosome = straight_chromosomes[0][1]
        if best_fitness == 0:
            return True, best_chromosome
        carried_chromosomes = [chromosome for _, chromosome in straight_chromosomes]

        mating_pool = _make_mating_pool(
            self.get_config("population_size") - straight_to_next_gen_count,
            self.population,
            fitnesses,
        )
        crossover_pool = self._create_crossover_pool(mating_pool)

        self.population.clear()
        self.population = [self._mutate(chromosome) for chromosome in crossover_pool]
        self.population.extend(carried_chromosomes)

        return best_fitness, best_chromosome
    
    def _create_crossover_pool(self, mating_pool: list[tuple]) -> list:
        crossover_pool = []
        for obj in mating_pool:
            if random.random() < self.get_config("crossover_probability"):
                crossover_pool.append(obj)
            else:
                crossover_pool.append(
                    _crossover(obj, random.choice(mating_pool), self.target)
                )
        return crossover_pool
    
    def _mutate(self, chromosome, ratio=0.4):
        """mutate the chromosome and return it"""
        mutation_number = random.sample(range(0, len(chromosome)), random.randint(0, int(len(chromosome)*ratio) + 1))
        next_chromosome = list(chromosome)
        for i in set(mutation_number):
            if i % 2 == 0:
                next_chromosome[i] = random.choice(self.operands)
            else:
                next_chromosome[i] = random.choice(self.operators)
        return tuple(next_chromosome)

    def _calculate_fitness(self, chromosome) -> int:
        return _calculate_fitness(chromosome, self.target)

    def set_timeout_by_seconds(self, seconds: float):
        start = None

        def timeout():
            nonlocal start
            if start is None:
                start = time()
            return time() - start > seconds

        self.timeout = timeout

    def set_timeout_by_iterations(self, iterations: int):
        iteration = 0

        def timeout():
            nonlocal iteration
            iteration += 1
            return iteration > iterations

        self.timeout = timeout

    @staticmethod
    def set_config(**kwargs):
        for key, value in kwargs.items():
            if key in EquationBuilder.__setattr:
                EquationBuilder.__config[key] = value
            else:
                raise ValueError(f"Invalid key {key}")

    @staticmethod
    def get_config(name=None):
        if name is None:
            return EquationBuilder.__config
        else:
            return EquationBuilder.__config[name]
