from biosim.fauna import Fauna

__author__ = 'Hans Kristian Lunda, Mikko Rekstad'
__email__ = 'hans.kristian.lunda@nmbu.no, mikkreks@nmbu.no'

"""
This file is used for testing of the class Cell.
"""


class TestCell:
    fauna_list = [{'loc': (3,4),
      'pop': [{'species': 'Herbivore', 'age': 10, 'weight': 15},
              {'species': 'Herbivore', 'age': 5, 'weight': 40},
              {'species': 'Herbivore', 'age': 15, 'weight': 25}]},
     {'loc': (4,4),
      'pop': [{'species': 'Herbivore', 'age': 2, 'weight': 60},
              {'species': 'Herbivore', 'age': 9, 'weight': 30},
              {'species': 'Herbivore', 'age': 16, 'weight': 14}]},
     {'loc': (4,4),
      'pop': [{'species': 'Carnivore', 'age': 3, 'weight': 35},
              {'species': 'Carnivore', 'age': 5, 'weight': 20},
              {'species': 'Carnivore', 'age': 8, 'weight': 5}]}]

    def test_get_creatures(self):
        """
        Test that the correct number of animals are returned
        :return:
        """
        creatures_added = Fauna(species='herbivore', age=10, weight=15)
        assert len(creatures_added) == 1
        pass

    def test_get_number_of_carnivores(self):
        """
        Test that the correct number of carnivores are returned
        :return:
        """

        pass

    def test_get_number_of_herbivores(self):
        """
        Test that the correct number of herbivores are returned
        :return:
        """
        pass

    def test_get_fodder(self):
        """
        Test that the correct amount of fodder is returned
        :return:
        """

        pass

    def test_add_fodder(self):
        """
        Test that fodder can be added to the cell
        :return:
        """
        pass

    def test_add_pop(self):
        """
        Test that population can be added to the cell
        :return:
        """
        pass
