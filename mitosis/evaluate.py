"""Evaluates genotypes based on a provided fitness function.

@since 0.1.0
"""

from typing import Callable


def evaluate(population: list, evaluation_fn: Callable) -> list:
    """Evaluates the given population using the given evaluation function.

    Params:
    - population (list<str>): The population of genotypes to evaluate
    - evaluation_fn (Callable): The evaluation function to use

    Returns:
    - evaluated_population (list<tuple<str, Any>>): The evaluated genotypes with their scores
    """
    evaluated_population = [(genotype, evaluation_fn(genotype)) for genotype in population]
    return evaluated_population
# End of evaluate()
