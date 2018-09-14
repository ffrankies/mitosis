"""Generates "DNA" sequences - the "genotype" of a population.

@since 0.1.0
"""

import random


def generate(searchspace_size: int, population_size: int, random_seed: int = 0.12345) -> list:
    """Generates the initial population of size population_size using the size of the searchspace.
    
    Params:
    - searchspace_size (int): The size of the searchspace
    - population_size (int): The size of the population to generate

    Returns:
    - population (list<str>): The generated population
    """
    random.seed(random_seed)
    population = random.choices(['0','1'], k=112)
    population = [''.join(genotype) for genotype in population]
    return population
# End of generate()
