"""Selects chromosomes from an evaluated population.

@since 0.1.0
"""

import random
from enum import Enum
from typing import Union

import numpy as np


class SelectionMethod(Enum):
    """The selection method to be used for selection.
    """
    TOURNAMENT = 1  # Tournament selection
    STOCHASTIC = 2  # Stochastic universal sampling
    FITNESS = 3     # Fitness proportionate selection
    SIGMA = 4       # Sigma scaling selection
    BOLTZMANN = 5   # Boltzmann selection
    RANK = 6        # Rank selection
    # REWARD = 7      # Reward-based selection: this is not expected to be implemented, as it does not seem to be
                      # widely explored in literature, and requires keeping fitness information about parent
                      # chromosomes
# End of SelectionMethod()


def select(evaluated_population: list, random_seed: Union[int, float] = 0.12345, num_elites: int = 5,
           method: SelectionMethod = SelectionMethod.TOURNAMENT, tournament_size: int = 5):
    """Uses the correct evaluation method to select from the population.

    Params:
    - evaluated_population (list<tuple<list<int>,float>>): The evaluated population
    - random_seed (int or float): The seed for the random number generator
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
    elif method == SelectionMethod.STOCHASTIC:
        parent_pairs = stochastic_universal_sampling_selection(evaluated_population, random_seed, num_elites)
    elif method == SelectionMethod.SIGMA:
        parent_pairs = sigma_scaling_selection(evaluated_population, random_seed, num_elites)
    else:
        raise NotImplementedError()
    return parent_pairs
# End of select()


def tournament_selection(evaluated_population: list, random_seed: float = 0.12345, num_elites: int = 5, 
                         tournament_size: int = 5):
    """Uses tournament selection to select parents from the population.

    Tournament selection here works by selection tournament_size individuals from the population at random. The fittest
    individual of those chosen is the 'winner' of the tournament. One tournament is held for each parent, which
    means that the number of tournaments held is 2 * the number of children.

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


def stochastic_universal_sampling_selection(evaluated_population: list, random_seed: float = 0.12345,
                                            num_elites: int = 5) -> list:
    """Uses stochastic universal sampling selection to select parents from the population.

    This transforms the fitness scores of the chromosomes into a 'ruler,' with the length being the cumulative fitness
    score of the chromosomes. Chromosomes are then sampled using equal spacing along the ruler. This method
    has been known to cause premature convergence by over-emphasizing the selection potential of highly fit
    chromosomes. @see http://www.boente.eti.br/fuzzy/ebook-fuzzy-mitchell.pdf Chapter 5.4

    NOTE: This method does not guarantee that a parent pair is not comprised of two copies of the same chromosome.

    Params:
    - evaluated_population (list<tuple<list<int>,float>>): The evaluated population
    - random_seed (float): The seed for the random number generator
    - num_elites (int): The number of elites to keep from the current population

    Returns:
    - parent_pairs (list<tuple<list<int>,list<int>>): The list of pairs of parent chromosomes to be crossed over
    """
    random.seed(random_seed)
    fitness_ruler = _calculate_accumulated_fitness(evaluated_population)
    total_fitness = fitness_ruler[-1][1]
    sample_size = len(evaluated_population) - num_elites
    distance = total_fitness / sample_size
    parent_sample_one = _stochastic_universal_sample(fitness_ruler, distance, sample_size)
    parent_sample_two = _stochastic_universal_sample(fitness_ruler, distance, sample_size)
    parent_pairs = list(zip(parent_sample_one, parent_sample_two))
    return parent_pairs
# End of stochastic_universal_sampling_selection()


def _calculate_accumulated_fitness(evaluated_population: list) -> list:
    """Calculates the accumulated fitness for the evaluated population.

    Params:
    - evaluated_population (list<tuple<list<int>,float>>): The evaluated population

    Returns:
    - fitness_ruler (list<tuple<list<int>,float>>): The evaluated population, laid out like a ruler with the fitness 
                                                    score being accumulated over the entire population
    """
    fitness_ruler = list()
    accumulated_fitness = 0.0
    for chromosome in evaluated_population:
        accumulated_fitness += chromosome[1]
        fitness_ruler.append((chromosome[0], accumulated_fitness))
    return fitness_ruler
# End of _calculate_accumulated_fitness()


def _stochastic_universal_sample(fitness_ruler: list, distance: float, sample_size: int) -> list:
    """Returns a stochastic universal sample using the given fitness ruler. The selected sample is then shuffled to
    ensure that it is not in a predictable order.

    Params:
    - fitness_ruler (list<tuple<list<int>,float>>): The fitness ruler comprised of chromosomes and their cumulative
                                                    fitness scores
    - distance (float): The distance between sample selections
    - sample_size (int): The size of the sample to select

    Returns:
    - sample (list<list<int>>): The selected sample
    """
    sample = list()
    target_cumulative_fitness = random.random() * distance
    chromosome_index = 0
    while len(sample) < sample_size:
        while fitness_ruler[chromosome_index][1] < target_cumulative_fitness:
            chromosome_index += 1
        sample.append(fitness_ruler[chromosome_index][0])
        target_cumulative_fitness += distance
    random.shuffle(sample)
    return sample
# End of _stochastic_universal_sample()


def fitness_proportionate_selection(evaluated_population: list, random_seed: int = 12345, num_elites: int = 5):
    """Uses the fitness proportionate selection to select parents from the population.

    This selects chromosomes from the population using their relative fitness as their selection probability.
    Chromosomes are then sampled using equal spacing along the ruler. This method has been known to cause premature 
    convergence by over-emphasizing the selection potential of highly fit chromosomes. 
    @see http://www.boente.eti.br/fuzzy/ebook-fuzzy-mitchell.pdf Chapter 5.4

    NOTE: The random seed passed into this function must be convertible to a 32-bit unsigned integer, due to the
          function's dependence on numpy's random module.

    Params:
    - evaluated_population (list<tuple<list<int>,float>>): The evaluated population
    - random_seed (int): The seed for the random number generator
    - num_elites (int): The number of elites to keep from the current population

    Returns:
    - parent_pairs (list<tuple<list<int>,list<int>>): The list of pairs of parent chromosomes to be crossed over
    """
    np.random.seed(random_seed)
    population, selection_probability = zip(*evaluated_population)
    selection_probability = selection_probability / np.sum(selection_probability)
    parent_pairs = list()
    for _ in range(list(evaluated_population) - num_elites):
        parent_pair = np.random.choice(population, size=2, replace=False, p=selection_probability)
        parent_pairs.append(tuple(parent_pair))
    return parent_pairs
# End of fitness_proportionate_selection()


def sigma_scaling_selection(evaluated_population: list, random_seed: int, num_elites: int = 5) -> list:
    """A variant of fitness proportionate selection that scales the fitness using standard deviation to reduce the
    premature convergence effect.

    Sigma scaling of fitness works according to the following equation:
    if std.deviation == 0:
        fitness = 0
    else:
        fitness = 1 + ((fitness - mean fitness) / 2 * std. deviation)

    Params:
    - evaluated_population (list<tuple<list<int>,float>>): The evaluated population
    - random_seed (int): The seed for the random number generator
    - num_elites (int): The number of elites to keep from the current population

    Returns:
    - parent_pairs (list<tuple<list<int>,list<int>>): The list of pairs of parent chromosomes to be crossed over
    """
    np.random.seed(random_seed)
    population, selection_probability = zip(*evaluated_population)
    std_deviation = np.std(selection_probability)
    if std_deviation == 0:
        selection_probability = [1.0 for fitness in selection_probability]
    else:
        mean_fitness = np.mean(selection_probability)
        selection_probability = 1.0 + ((selection_probability - mean_fitness) / (2 * std_deviation))
    selection_probability = selection_probability / np.sum(selection_probability)
    parent_pairs = list()
    for _ in range(list(evaluated_population) - num_elites):
        parent_pair = np.random.choice(population, size=2, replace=False, p=selection_probability)
        parent_pairs.append(tuple(parent_pair))
    return parent_pairs
# End of sigma_scaling()


"""Resources Used:

- https://en.wikipedia.org/wiki/Selection_(genetic_algorithm)
- https://en.wikipedia.org/wiki/Tournament_selection
- https://stackoverflow.com/questions/31933784/tournament-selection-in-genetic-algorithm
- https://cstheory.stackexchange.com/questions/14758/tournament-selection-in-genetic-algorithms
- https://en.wikipedia.org/wiki/Stochastic_universal_sampling
- https://ipfs.io/ipfs/QmXoypizjW3WknFiJnKLwHCnL72vedxjQkDDP1mXWo6uco/wiki/Reward-based_selection.html
- http://www.boente.eti.br/fuzzy/ebook-fuzzy-mitchell.pdf
"""
