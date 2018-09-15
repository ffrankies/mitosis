"""Tests the functions in the evaluate module.

@since 0.1.0
"""

from mitosis.evaluate import evaluate
from mitosis.generate import generate


def eval_add(sequence):
    return sum(sequence)


class TestEvaluate():
    def test_should_give_empty_list_when_pop_is_empty(self):
        evaluated = evaluate([], eval_add)
        assert evaluated == []

    def test_should_give_empty_tuples_when_chromosomes_are_empty(self):
        pop = generate(0, 100)
        evaluated = evaluate(pop, eval_add)
        for e in evaluated:
            assert e == ([], 0)

    def test_should_not_have_impossible_scores(self):
        pop = generate(50, 100)
        evaluated = evaluate(pop, eval_add)
        for e in evaluated:
            assert e[1] <= 50
            assert e[1] >= 0
            assert sum(e[0]) == e[1]
            f = [elem for elem in e[0] if elem == 1]
            assert e[1] == len(f)
