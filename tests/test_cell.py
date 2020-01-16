from biosim.fauna import Fauna
from biosim.Cell import Cell, Jungle, Ocean, Mountain, Savannah, Desert

__author__ = 'Hans Kristian Lunda, Mikko Rekstad'
__email__ = 'hans.kristian.lunda@nmbu.no, mikkreks@nmbu.no'

"""
This file is used for testing of the class Cell.
"""


class TestCell:
    fauna_list = [{'loc': (3, 4),
                   'pop': [{'species': 'herbivore', 'age': 10, 'weight': 15},
                           {'species': 'herbivore', 'age': 5, 'weight': 40},
                           {'species': 'herbivore', 'age': 15, 'weight': 25}]},
                  {'loc': (4, 4),
                   'pop': [{'species': 'Herbivore', 'age': 2, 'weight': 60},
                           {'species': 'Herbivore', 'age': 9, 'weight': 30},
                           {'species': 'Herbivore', 'age': 16, 'weight': 14}]},
                  {'loc': (4, 4),
                   'pop': [{'species': 'Carnivore', 'age': 3, 'weight': 35},
                           {'species': 'Carnivore', 'age': 5, 'weight': 20},
                           {'species': 'Carnivore', 'age': 8, 'weight': 5}]}]

    test = [{'loc': (10, 10),
             'pop': [{'species': 'herbivore', 'age': 10, 'weight': 15},
                     {'species': 'herbivore', 'age': 5, 'weight': 40},
                     {'species': 'herbivore', 'age': 5, 'weight': 40},
                     {'species': 'herbivore', 'age': 5, 'weight': 40},
                     {'species': 'herbivore', 'age': 5, 'weight': 40},
                     {'species': 'herbivore', 'age': 15, 'weight': 25}]}
            ]

    test2 = [{'loc': (10, 10),
              'pop': [{'species': 'herbivore', 'age': 10, 'weight': 15},
                      {'species': 'herbivore', 'age': 5, 'weight': 100},
                      {'species': 'herbivore', 'age': 0, 'weight': 6},
                      {'species': 'herbivore', 'age': 5, 'weight': 45},
                      {'species': 'herbivore', 'age': 40, 'weight': 43},
                      {'species': 'herbivore', 'age': 15, 'weight': 25}]}
             ]

    def test_add_population(self, test=test):
        """
        Will test that we can add a population to the single cell.
        :param test:
        :return:
        """
        cell_pop = {}
        for item in test:
            cell_pop = item['pop']

        test_cell = Jungle()
        test_cell.add_pop(cell_pop)
        assert test_cell.number_herbivores() == 6

    def test_get_creatures(self, test=test):
        """
        Test that the correct number of animals are returned
        :return:
        """
        cell_pop = {}
        for item in test:
            cell_pop = item['pop']

        test_cell = Jungle()
        test_cell.add_pop(cell_pop)
        assert test_cell.number_creatures() == 6

    def test_get_number_of_carnivores(self):
        """
        Test that the correct number of carnivores are returned.
        Currently checks that the empty cell contains 0 carnivores.
        :return:
        """
        test_cell = Jungle()
        num_carnivores = test_cell.number_creatures()

        assert num_carnivores == 0

    def test_get_number_of_herbivores(self, test=test):
        """
        Test that the correct number of herbivores are returned
        :return:
        """
        cell_pop = {}
        for item in test:
            cell_pop = item['pop']

        test_cell = Jungle()
        test_cell.add_pop(cell_pop)
        assert test_cell.number_herbivores() == 6

    def test_add_fodder(self):
        """
        Test that the start amount of fodder is correct.
        Will also test that the test fodder function works properly, and
        that fodder can be added to a cell.
        :return:
        """
        test_jungle = Jungle()
        assert test_jungle.fodder == 800.0
        test_jungle.fodder = 0.0
        test_jungle.add_fodder()
        assert test_jungle.fodder == 800.0

        test_savannah = Savannah()
        assert test_savannah.fodder == 300.0
        test_savannah.fodder = 0
        test_savannah.add_fodder()
        assert test_savannah.fodder == 30.0
        test_savannah.add_fodder()
        assert test_savannah.fodder == 111.0
        fodder_test = Cell((2, 2), 'J', fodder=300)
        amount_of_fodder = fodder_test.get_fodder()
        assert amount_of_fodder is not None

    def test_habitability(self):
        test_jungle = Jungle()
        test_savannah = Savannah()
        test_desert = Desert()
        test_ocean = Ocean()
        test_mountain = Mountain()
        assert test_jungle.habitable
        assert test_savannah.habitable
        assert test_desert.habitable
        assert not test_ocean.habitable
        assert not test_mountain.habitable

    # def test_add_fodder(self):
    #     """
    #     Test that fodder can be added to the cell
    #     :return:
    #     """
    #     fodder_test = Cell((2, 2), 'J', fodder=300)
    #     amount_of_fodder = fodder_test.get_fodder()
    #     assert amount_of_fodder is not None
    #     # pass

    def test_mating_season(self, test=test):
        """
        Test that population can be added to the cell
        :return:
        """
        cell_pop = {}
        for item in test:
            cell_pop = item['pop']
        test_cell = Jungle()
        test_cell.add_pop(cell_pop)
        test_cell.mating_season()
        assert test_cell.number_herbivores() != 6
        # Will test that the creature only mates if they whey enough.
        for creature in test_cell.population_herbivores:
            creature.have_mated = False
        test_cell.mating_season()
        assert test_cell.number_herbivores() == 10
        # Now I want to test that they can procreate next year.
        for creature in test_cell.population_herbivores:
            creature.weight += 20
        test_cell.mating_season()
        assert test_cell.number_herbivores() != 10
        # Now I want to test that the creature only mates once a year.
        # The population should now remain 16.
        test_cell.mating_season()
        assert test_cell.number_herbivores() == 16

    def test_ranked_fitness(self, test=test2):
        """
        Will test that each creature gets ranked properly. Uses test 2,
        because there all creatures have different fitness.
        :param test: List of creatures in a population.
        :return:
        """
        cell_pop = {}
        for item in test:
            cell_pop = item['pop']
        test_cell = Jungle()
        test_cell.add_pop(cell_pop)
        test_cell.ranked_fitness()
        for i in range(test_cell.number_herbivores() - 1):
            fitness1 = test_cell.population_herbivores[i].fitness
            fitness2 = test_cell.population_herbivores[i + 1].fitness
            assert fitness1 > fitness2

    def test_feed_herbivores(self, test=test):
        """
        We can do a couple different tests to check that the correct amount
        of weight is added to the creature after it eats.
        Also we have to check that the amount of available fodder is reduced.
        :param test: dict
        :return:
        """
        cell_pop = {}
        for item in test:
            cell_pop = item['pop']
        test_cell = Jungle()
        test_cell.add_pop(cell_pop)
        test_cell.add_fodder()

        weight = []
        weight2 = []
        for creature in test_cell.population_herbivores:
            weight.append(creature.weight)
        test_cell.feed_herbivores()
        assert 24 == test_cell.population_herbivores[0].weight
        for i in range(len(weight)):
            assert weight[i] + 9 == test_cell.population_herbivores[i].weight
            # Storing this information for next test.
            weight2.append(test_cell.population_herbivores[i].weight)

        # Testing that the correct amount of fodder is removed.
        assert test_cell.fodder == 800.0 - 10 * len(weight)

        # Will now test that a creature gets the correct amount of food if
        # Fodder is < 10 also that the rest does not get food.
        test_cell.fodder = 7
        test_cell.feed_herbivores()
        assert test_cell.population_herbivores[0].weight == 24 + (7 * 0.9)
        # Will test that the weight on the other creatures is unaltered.
        for i in range(1, len(weight)):
            assert test_cell.population_herbivores[i].weight == weight2[i]

    def test_lose_weight(self, test=test):
        """
        Will test that all creatures lose correct amount of weight.
        !!!! may also implement that they only lose weight once!
        :param test: dict
        :return:
        """
        cell_pop = {}
        for item in test:
            cell_pop = item['pop']
        test_cell = Jungle()
        test_cell.add_pop(cell_pop)
        weight = []
        for i in range(test_cell.number_herbivores()):
            weight.append(test_cell.population_herbivores[i].weight)
        test_cell.lose_weight()
        for i in range(test_cell.number_herbivores()):
            new_weight = test_cell.population_herbivores[i].weight
            assert new_weight == weight[i]

    def test_remove_pop(self, test=test):
        """
        Will test that the animals die in correct fashion.
        :param test:
        :return:
        """
        pass
