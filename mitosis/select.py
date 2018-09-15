"""Selects chromosomes from an evaluated population.

@since 0.1.0
"""

import random
from enum import Enum
from typing import List


class SelectionMethod(Enum):
    """The selection method to be used for selection.
    """
    TOURNAMENT = 1  # Tournament selection
    STOCHASTIC = 2  # Stochastic universal sampling
    REWARD = 3      # Reward-based selection
    FITNESS = 4     # Fitness proportionate selection
# End of SelectionMethod()


def select(evaluated_population: list, random_seed: float = 0.12345, num_elites: int = 5,
           method: SelectionMethod = SelectionMethod.TOURNAMENT, tournament_size: int = 5):
    """Uses the correct evaluation method to select from the population.

    Params:
    - evaluated_population (list<tuple<list<int>,float>>): The evaluated population
    - random_seed (float): The seed for the random number generator
    - num_elites (int): The number of elites to keep from the current population
    - method (SelectionMethod): The selection method to use

    Method-specific params:
    - tournament_size (int): In the tournament method, specifies the size of the tournament. When equal to 1, the
                             method is equivalent to random selection. The higher the tournament size, the higher the
                             bias towards the fitter individuals.

    Returns:
    - parent_pairs (list<tuple<list<int>,list<int>>): The list of pairs of parent chromosomes to be crossed over
    """
    if method == SelectionMethod.TOURNAMENT:
        parent_pairs = tournament_selection(evaluated_population, random_seed, num_elites, tournament_size)
    elif method == SelectionMethod.FITNESS:
        parent_pairs = fitness_proportionate_selection(evaluated_population, random_seed, num_elites)
    elif method == SelectionMethod.REWARD:
        parent_pairs = reward_based_selection(evaluated_population, random_seed, num_elites)
    else:  # method == SelectionMethod.STOCHASTIC
        parent_pairs = stochastic_universal_sampling_selection(evaluated_population, random_seed, num_elites)
    return parent_pairs
# End of select()


def tournament_selection(evaluated_population: list, random_seed: float = 0.12345, num_elites: int = 5, 
                         tournament_size: int = 5):
    """Uses tournament selection to select parents from the population.

    Params:
    - evaluated_population (list<tuple<list<int>,float>>): The evaluated population
    - random_seed (float): The seed for the random number generator
    - num_elites (int): The number of elites to keep from the current population
    - tournament_size (int): Specifies the size of the tournament. When equal to 1, the
                             method is equivalent to random selection. The higher the tournament size, the higher the
                             bias towards the fitter individuals.

    Returns:
    - parent_pairs (list<tuple<list<int>,list<int>>): The list of pairs of parent chromosomes to be crossed over
    """
    random.seed(random_seed)
    parent_pairs = list()
    for _ in range(len(evaluated_population) - num_elites):
        parent_one = _tournament(evaluated_population, tournament_size)
        parent_two = _tournament(evaluated_population, tournament_size)
        parent_pairs.append((parent_one, parent_two))
    return parent_pairs
# End of tournament_selection()


def _tournament(evaluated_population: list, tournament_size: int = 5, previous_winner: list = None):
    """Selects tournament_size number of chromosomes to 'compete' against each other. The chromosome with the highest
    fitness score 'wins' the tournament.

    Params:
    - evaluated_population (list<tuple<list<int>,float>>): The evaluated population
    - tournament_size (int): Specifies the size of the tournament. When equal to 1, the
                             method is equivalent to random selection. The higher the tournament size, the higher the
                             bias towards the fitter individuals.
    - previous_winner (list<int>): The winner of the previous tournament. If the same chromosome wins both tournaments,
                                   then the runner-up to the current tournament is chosen.

    Returns:
    - winner (list<int>): The chromosome with the highest score in the tournament
    """
    tournament = random.sample(evaluated_population, tournament_size)
    tournament.sort(key=lambda evaluated_chromosome: evaluated_chromosome[1])
    winner = tournament[0][0]  # pylint: disable=E1136
    if winner == previous_winner:
        winner = tournament[1][0]  # pylint: disable=E1136
    return winner
# End of _tournament()


def stochastic_universal_sampling_selection(evaluated_population: list, random_seed: float = 0.12345, num_elites: int = 5):
    """Uses stochastic universal sampling selection to select parents from the population.

    Params:
    - evaluated_population (list<tuple<list<int>,float>>): The evaluated population
    - random_seed (float): The seed for the random number generator
    - num_elites (int): The number of elites to keep from the current population

    Returns:
    - parent_pairs (list<tuple<list<int>,list<int>>): The list of pairs of parent chromosomes to be crossed over
    """
    raise NotImplementedError()
# End of stochastic_universal_sampling_selection()


def reward_based_selection(evaluated_population: list, random_seed: float = 0.12345, num_elites: int = 5):
    """Uses the reward based selection to select parents from the population.

    Params:
    - evaluated_population (list<tuple<list<int>,float>>): The evaluated population
    - random_seed (float): The seed for the random number generator
    - num_elites (int): The number of elites to keep from the current population

    Returns:
    - parent_pairs (list<tuple<list<int>,list<int>>): The list of pairs of parent chromosomes to be crossed over
    """
    raise NotImplementedError()
# End of reward_based_selection()


def fitness_proportionate_selection(evaluated_population: list, random_seed: float = 0.12345, num_elites: int = 5):
    """Uses the fitness proportionate selection to select parents from the population.

    Params:
    - evaluated_population (list<tuple<list<int>,float>>): The evaluated population
    - random_seed (float): The seed for the random number generator
    - num_elites (int): The number of elites to keep from the current population

    Returns:
    - parent_pairs (list<tuple<list<int>,list<int>>): The list of pairs of parent chromosomes to be crossed over
    """
    raise NotImplementedError()
# End of fitness_proportionate_selection()
