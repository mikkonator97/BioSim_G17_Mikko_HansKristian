from biosim.fauna import Fauna
from biosim.Cell import Cell, Jungle, Ocean, Mountain, Savannah, Desert
__author__ = 'Hans Kristian Lunda, Mikko Rekstad'
__email__ = 'hans.kristian.lunda@nmbu.no, mikkreks@nmbu.no'

"""
This file is used for testing of the class Cell.
"""


class TestCell:
    fauna_list = [{'loc': (3,4),
      'pop': [{'species': 'herbivore', 'age': 10, 'weight': 15},
              {'species': 'herbivore', 'age': 5, 'weight': 40},
              {'species': 'herbivore', 'age': 15, 'weight': 25}]},
     {'loc': (4,4),
      'pop': [{'species': 'Herbivore', 'age': 2, 'weight': 60},
              {'species': 'Herbivore', 'age': 9, 'weight': 30},
              {'species': 'Herbivore', 'age': 16, 'weight': 14}]},
     {'loc': (4,4),
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


    def test_add_population(self, test=test):
        """
        Will test that we can add a population to the single cell.
        :param test:
        :return:
        """
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
        for item in test:
            cell_pop = item['pop']

        test_cell = Jungle()
        test_cell.add_pop(cell_pop)
        assert test_cell.number_herbivores() == 6

    def test_get_fodder(self):
        """
        Test that the correct amount of fodder is returned
        :return:
        """
        fodder_test = Cell((2,2), 'J', fodder=300)
        amount_of_fodder = fodder_test.get_fodder()
        assert amount_of_fodder == 300
        pass

    def test_add_fodder(self):
        """
        Test that fodder can be added to the cell
        :return:
        """
        fodder_test = Cell((2,2), 'J', fodder=300)
        amount_of_fodder = fodder_test.get_fodder()
        assert amount_of_fodder is not None
        pass

    def test_mating_season(self, test=test):
        """
        Test that population can be added to the cell
        :return:
        """
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


        



