# Copyright © 2023 Giovanni Squillero <giovanni.squillero@polito.it>
# https://github.com/squillero/computational-intelligence
# Free for personal or classroom use; see 'LICENSE.md' for details.

from abc import abstractmethod


class AbstractProblem:
    def __init__(self):
        self._calls = 0

    @property
    @abstractmethod
    def x(self):
        pass

    @property
    def calls(self):
        return self._calls

    @staticmethod
    def onemax(genome):
        return sum(bool(g) for g in genome)

    def __call__(self, genome):

        # 1. Update the number of calls to the fitness function.
        self._calls += 1

        # 2. Calculate fitness values for different sub-genomes of the input genome and then sorts them in descending order.
            # The number of sub-genomes depends on the value of x (i.e., the instance of the problem).
        fitnesses = sorted((AbstractProblem.onemax(genome[s :: self.x]) for s in range(self.x)), reverse=True)
        
        # 3. Calculate the fitness value of the input genome.
            # This is done aggregating fitness values from different sub-genomes of the input genome, 
            # giving more weight to sub-genomes with higher fitness values
        val = sum(f for f in fitnesses if f == fitnesses[0]) - sum(
            f * (0.1 ** (k + 1)) for k, f in enumerate(f for f in fitnesses if f < fitnesses[0])
        )
        return val / len(genome)


def make_problem(a):
    class Problem(AbstractProblem):
        @property
        @abstractmethod
        def x(self):
            return a

    return Problem()