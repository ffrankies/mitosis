"""Selects chromosomes from an evaluated population.

@since 0.1.0
"""

from enum import Enum


class SelectionMethod(Enum):
    """The selection method to be used for selection.
    """
    TOURNAMENT = 1  # Tournament selection
    STOCHASTIC = 2  # Stochastic universal sampling
    REWARD = 3      # Reward-based selection
    FITNESS = 4     # Fitness proportionate selection
# End of SelectionMethod()


def select(evaluated_population: list, random_seed: float = 0.12345, elites: int = 5,
           method: SelectionMethod = SelectionMethod.TOURNAMENT):
    """Uses the correct evaluation method to select from the population.

    Params:
    - evaluated_population (list<tuple<list<int>,float>>): The evaluated population
    - random_seed (float): The seed for the random number generator
    - elites (int): The number of elites to keep from the current population
    - method (SelectionMethod): The selection method to use

    Returns:
    - elites (list<list<int>>): The elites from the evaluated population
    - parent_pairs (list<tuple<list<int>,list<int>>): The list of pairs of parent chromosomes to be crossed over
    """
    if method == SelectionMethod.TOURNAMENT:
        elites, parent_pairs = tournament_selection(evaluated_population, random_seed, elites)
    elif method == SelectionMethod.FITNESS:
        elites, parent_pairs = fitness_proportionate_selection(evaluated_population, random_seed, elites)
    elif method == SelectionMethod.REWARD:
        elites, parent_pairs = reward_based_selection(evaluated_population, random_seed, elites)
    else:  # method == SelectionMethod.STOCHASTIC
        elites, parent_pairs = stochastic_universal_sampling_selection(evaluated_population, random_seed, elites)
    return elites, parent_pairs
# End of select()


def tournament_selection(evaluated_population: list, random_seed: float = 0.12345, elites: int = 5):
    """Uses tournament selection to select parents from the population.

    Params:
    - evaluated_population (list<tuple<list<int>,float>>): The evaluated population
    - random_seed (float): The seed for the random number generator
    - elites (int): The number of elites to keep from the current population

    Returns:
    - elites (list<list<int>>): The elites from the evaluated population
    - parent_pairs (list<tuple<list<int>,list<int>>): The list of pairs of parent chromosomes to be crossed over
    """
    raise NotImplementedError()
# End of tournament_selection()


def stochastic_universal_sampling_selection(evaluated_population: list, random_seed: float = 0.12345, elites: int = 5):
    """Uses stochastic universal sampling selection to select parents from the population.

    Params:
    - evaluated_population (list<tuple<list<int>,float>>): The evaluated population
    - random_seed (float): The seed for the random number generator
    - elites (int): The number of elites to keep from the current population

    Returns:
    - elites (list<list<int>>): The elites from the evaluated population
    - parent_pairs (list<tuple<list<int>,list<int>>): The list of pairs of parent chromosomes to be crossed over
    """
    raise NotImplementedError()
# End of stochastic_universal_sampling_selection()


def reward_based_selection(evaluated_population: list, random_seed: float = 0.12345, elites: int = 5):
    """Uses the reward based selection to select parents from the population.

    Params:
    - evaluated_population (list<tuple<list<int>,float>>): The evaluated population
    - random_seed (float): The seed for the random number generator
    - elites (int): The number of elites to keep from the current population

    Returns:
    - elites (list<list<int>>): The elites from the evaluated population
    - parent_pairs (list<tuple<list<int>,list<int>>): The list of pairs of parent chromosomes to be crossed over
    """
    raise NotImplementedError()
# End of reward_based_selection()


def fitness_proportionate_selection(evaluated_population: list, random_seed: float = 0.12345, elites: int = 5):
    """Uses the fitness proportionate selection to select parents from the population.

    Params:
    - evaluated_population (list<tuple<list<int>,float>>): The evaluated population
    - random_seed (float): The seed for the random number generator
    - elites (int): The number of elites to keep from the current population

    Returns:
    - elites (list<list<int>>): The elites from the evaluated population
    - parent_pairs (list<tuple<list<int>,list<int>>): The list of pairs of parent chromosomes to be crossed over
    """
    raise NotImplementedError()
# End of fitness_proportionate_selection()
