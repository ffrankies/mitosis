"""Crosses over parent pairs to form children

@since 0.1.0
"""

import random
from typing import List, Union, Callable
from enum import Enum

from .types import Parents, Chromosome


class CrossoverMethod(Enum):
    """The selection method to be used for selection.
    """
    N_POINT = 1   # N-Point Crossover
    UNIFORM = 2   # Uniform Crossover
    CUSTOM = 3    # Custom Crossover
# End of SelectionMethod()


def crossover(parent_pairs: List[Parents], method: CrossoverMethod, random_seed: Union[int, float], num_points: int,
              custom_function: Callable, mixing_ratio: float = 0.5, *custom_args, **custom_kwargs) -> List[Chromosome]:
    """Uses one of the given methods to perform crossover on parent pairs.

    Params:
    - parent_pairs (List[Parents]): The list of parent pairs to be crossed over. Each parent pair produces one child
    - method (CrossoverMethod): The method of crossover to be used
    - random_seed (int or float): The seed for the random number generator
    - mixing_ratio (float): This refers to the probability that any gene or gene slice is selected from the first
                             parent as opposed to the second parent in the parent pair. Defaults to 0.5 (equal
                             probability that the gene is chosen from either parent)

    Method-specific params:
    - num_points (int): In n_point crossover, this refers to the number of crossover points to be used. Must be less
                        than the length of the chromosome.
    - custom_function (Callable): In custom crossover, this refers to the custom crossover function. The signature of
                                  this method must be function_name(parent_pairs, *args, **kwargs)
    - custom_args (Any): In custom crossover, this refers to the args to be passed to the custom crossover function
    - custom_kwargs (Any): In custom crossover, this refers to the keyword args to be passed to the custom crossover
                           function

    Returns:
    - children (List[Chromosome]): The children produced by crossover
    """
    if method == CrossoverMethod.N_POINT:
        children = n_point_crossover(parent_pairs, random_seed, num_points, mixing_ratio)
    elif method == CrossoverMethod.UNIFORM:
        children = uniform_crossover(parent_pairs, random_seed, mixing_ratio)
    elif method == CrossoverMethod.CUSTOM:
        children = custom_function(parent_pairs, custom_args, custom_kwargs)
    else:
        raise NotImplementedError()
    return children
# End of crossover()


def n_point_crossover(parent_pairs: List[Parents], random_seed: float, num_points: int,
                      mixing_ratio: float = 0.5) -> List[Chromosome]:
    """Uses the n-point crossover method to produce children from parent pairs. Each parent pair produces one child
    chromosome.

    Params:
    - parent_pairs (List[Parents]): The list of parent pairs to be crossed over. Each parent pair produces one child
    - random_seed (float): The seed for the random number generator
    - num_points (int): The number of crossover points to be used. Must be less than the length of the chromosome
    - mixing_ration (float): This refers to the probability that any gene slice is selected from the first parent as
                             opposed to the second parent in the parent pair. Defaults to 0.5 (equal probability that
                             the gene is chosen from either parent)

    Returns:
    - children (List[Chromosome]): The children produced by crossover
    """
    random.seed(random_seed)
    children = list()
    for parent_pair in parent_pairs:
        child = n_point_crossover(parent_pair, num_points, mixing_ratio)
        children.append(child)
    return children
# End of n_point_crossover()


def _n_point_crossover_one_pair(parent_pair: Parents, num_points: int, mixing_ratio: float = 0.5) -> Chromosome:
    """Uses the n-point crossover method to produce a single child from a parent pair.

    Params:
    - parent_pair (Parents): The pair of parent chromosomes
    - num_points (int): The number of crossover points to be used. Must be less than the length of the chromosome.
    - mixing_ratio (float): This refers to the probability that any gene slice is selected from the first parent as
                             opposed to the second parent in the parent pair. Defaults to 0.5 (equal probability that
                             the gene is chosen from either parent)

    Returns:
    - child (Chromosome): The child produced by crossover
    """
    parent_one, parent_two = parent_pair
    chromosome_length = len(parent_one)
    if not num_points < parent_one:
        raise ValueError("The number of crossover pairs ({}) must be < the length of chromosomes ({})".format(
            num_points, chromosome_length)
        )
    slice_indices = [0] + random.sample(list(range(1, chromosome_length)), num_points) + [chromosome_length]
    child = list()
    for index in range(len(slice_indices) - 1):
        start_index = slice_indices[index]
        end_index = slice_indices[index + 1]
        if random.random() < mixing_ratio:
            chromosome_slice = parent_one[start_index:end_index]
        else:
            chromosome_slice = parent_two[start_index:end_index]
        child.extend(chromosome_slice)
    return child
# End of _n_point_crossover_one_pair()


def uniform_crossover(parent_pairs: List[Parents], random_seed: float, mixing_ratio: float = 0.5) -> List[Chromosome]:
    """Uses the n-point crossover method to produce children from parent pairs. Each parent pair produces one child
    chromosome.

    Params:
    - parent_pairs (List[Parents]): The list of parent pairs to be crossed over. Each parent pair produces one child
    - random_seed (int or float): The seed for the random number generator
    - mixing_ratio (float): This refers to the probability that any gene or gene slice is selected from the first
                             parent as opposed to the second parent in the parent pair. Defaults to 0.5 (equal
                             probability that the gene is chosen from either parent)
    
    Returns:
    - children (List[Chromosome]): The children produced by crossover
    """
    random.seed(random_seed)
    children = list()
    for parent_pair in parent_pairs:
        child = _uniform_crossover_one_pair(parent_pair, mixing_ratio)
        children.append(child)
    return children
# End of uniform_crossover()


def _uniform_crossover_one_pair(parent_pair: Parents, mixing_ratio: float = 0.5) -> Chromosome:
    """Uses the uniform crossover method to produce a single child from a parent pair.
    
    Params:
    - parent_pair (Parents): The pair of parent chromosomes
    - mixing_ratio (float): This refers to the probability that any gene slice is selected from the first parent as
                             opposed to the second parent in the parent pair. Defaults to 0.5 (equal probability that
                             the gene is chosen from either parent)

    Returns:
    - child (Chromosome): The child produced by crossover
    """
    child = list()
    parent_one, parent_two = parent_pair
    for index in range(len(parent_one)):
        if random.random() < mixing_ratio:
            gene = parent_one[index]
        else:
            gene = parent_two[index]
        child.append(gene)
    return child
# End of _uniform_crossover_one_pair()
