"""Tests the functions in the generate module.

@since 0.1.0
"""

from mitosis.generate import generate


class TestGenerate():
    def test_should_return_empty_list_when_pop_size_is_0(self):
        pop = generate(100, 0)
        assert pop == []
        pop2 = generate(0, 0)
        assert pop2 == []

    def test_should_return_list_of_empty_lists_when_pop_size_is_0(self):
        pop = generate(0, 100)
        for p in pop:
            assert p == []

    def test_should_return_the_correct_number_of_genotypes(self):
        pop = generate(50, 100)
        assert len(pop) == 100

    def test_should_return_genotypes_of_the_correct_size(self):
        pop = generate(50, 100)
        for p in pop:
            assert len(p) == 50

    def test_should_return_genotypes_containing_only_0s_and_1s(self):
        pop = generate(50, 100)
        for p in pop:
            assert set(p) == set([0, 1])
