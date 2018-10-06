"""Evaluates chromosomes based on a provided fitness function.

@since 0.1.0
"""

from typing import Callable, List

from .types import Chromosome, Eval


def evaluate(population: List[Chromosome], evaluation_fn: Callable) -> List[Eval]:
    """Evaluates the given population using the given evaluation function.

    Params:
    - population (List[Chromosome]): The population of chromosomes to evaluate
    - evaluation_fn (Callable): The evaluation function to use

    Returns:
    - evaluated_population (List[Eval]): The evaluated chromosomes with their scores
    """
    evaluated_population = [(chromosome, evaluation_fn(chromosome)) for chromosome in population]
    return evaluated_population
# End of evaluate()
