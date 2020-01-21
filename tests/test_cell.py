from biosim.fauna import Fauna, Herbivore, Carnivore
from biosim.cell import Cell, Jungle, Ocean, Mountain, Savannah, Desert
import numpy as np

__author__ = 'Hans Kristian Lunda, Mikko Rekstad'
__email__ = 'hans.kristian.lunda@nmbu.no, mikkreks@nmbu.no'

"""
This file is used for testing of the class Cell.
"""
import pytest

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
    carn_list = [{'loc': (4, 4),
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

    test_random_carn = [{'loc': (10, 10),
              'pop': [{'species': 'herbivore', 'age': 10, 'weight': 15},
                      ]} for _ in range(10)
             ]

    @pytest.fixture(autouse=True)
    def jungle_test_cell(self):
        self.test_cell = Jungle()
        for item in self.fauna_list:
            cell_pop = item['pop']
            self.test_cell.add_pop(cell_pop)

    def test_add_pop(self, test=test):
        """
        Will test that we can add a population to the single cell.
        :param test:
        :return:
        """
        assert self.test_cell.number_herbivores() == 6
        assert self.test_cell.number_carnivores() == 3

    def test_number_carnivores(self):
        """
        Test that the correct number of carnivores are returned.
        Currently checks that the empty cell contains 0 carnivores.
        :return:
        """
        test_cell = Jungle()
        num_carnivores = test_cell.number_carnivores()
        assert num_carnivores == 0

        num_carnivores = self.test_cell.number_carnivores()
        assert num_carnivores == 3

    def test_number_herbivores(self, test=test):
        """
        Test that the correct number of herbivores are returned
        :return:
        """
        assert self.test_cell.number_herbivores() == 6

    def test_add_fodder(self):
        """
        Test that the start amount of fodder is correct.
        Will also test that the test fodder function works properly, and
        that fodder can be added to a cell.
        :return:
        """
        # test_jungle = Jungle()
        assert self.test_cell.fodder == 800.0
        self.test_cell.fodder = 0.0
        self.test_cell.add_fodder()
        assert self.test_cell.fodder == 800.0
        test_savannah = Savannah()
        assert test_savannah.fodder == 300.0
        test_savannah.fodder = 0
        test_savannah.add_fodder()
        assert test_savannah.fodder == 90.0
        test_savannah.add_fodder()
        assert test_savannah.fodder == 153.0

    def test_get_fodder(self):
        """ Test that get_fodder returns the correct amount of fodder. """
        assert self.test_cell.get_fodder() == 800

    def test_habitability(self):
        """Test that the cells get correct habitability."""
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

    def test_ranked_fitness(self, test=test2):
        """
        Will test that each creature gets ranked properly. Uses test 2,
        because there all creatures have different fitness.
        :param test: List of creatures in a population.
        :return:
        """
        self.test_cell.ranked_fitness_herbivores()
        for i in range(self.test_cell.number_herbivores() - 1):
            fitness1 = self.test_cell.population_herbivores[i].fitness
            fitness2 = self.test_cell.population_herbivores[i + 1].fitness
            assert fitness1 > fitness2
        self.test_cell.ranked_fitness_herbivores_weakest()
        for i in range(self.test_cell.number_herbivores() - 1):
            fitness1 = self.test_cell.population_herbivores[i].fitness
            fitness2 = self.test_cell.population_herbivores[i + 1].fitness
            assert fitness1 < fitness2
        cell_pop = {}
        for item in self.carn_list:
            cell_pop = item['pop']
        test_cell = Jungle()
        test_cell.add_pop(cell_pop)
        test_cell.ranked_fitness_carnivores()
        for i in range(test_cell.number_carnivores() - 1):
            fitness1 = test_cell.population_carnivores[i].fitness
            fitness2 = test_cell.population_carnivores[i + 1].fitness
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
            test_cell.feed_herbivores(creature)
        assert 24 == test_cell.population_herbivores[0].weight
        for i in range(len(weight)):
            assert weight[i] + 9 == test_cell.population_herbivores[i].weight
            # Storing this information for next test.
            weight2.append(test_cell.population_herbivores[i].weight)

        # Testing that the correct amount of fodder is removed.
        assert test_cell.fodder == 800.0 - 10 * len(weight)

        # Will now test that a creature gets the correct amount of food if
        # Fodder is < 10 also that the rest does not get food.
        test_creature = test_cell.population_herbivores[0]
        test_cell.fodder = 7
        test_cell.feed_herbivores(test_creature)
        assert test_cell.population_herbivores[0].weight == 24 + (7 * 0.9)
        # Will test that the weight on the other creatures is unaltered.
        for i in range(1, len(weight)):
            assert test_cell.population_herbivores[i].weight == weight2[i]

    def test_feed_carnivore(self, test=test2):
        """
        This function will test that the carnivore will not eat if there is no
        herbivores in the cell, stops eating if it has eaten 50 units of fodder
        if there is no herbivores left to eat, or if the carnivore has tried
        to kill all the herbivores in the cell.
        :return:
        """
        test_cell = Jungle()
        cell_pop = {}
        for item in self.carn_list:
            cell_pop = item['pop']
        test_cell.add_pop(cell_pop)
        assert test_cell.feed_carnivores() is None

        test_cell = Jungle()
        cell_pop = {}
        test3 = [{'loc': (10, 10),
                  'pop': [{'species': 'herbivore', 'age': 100, 'weight': 70},
                          {'species': 'herbivore', 'age': 100, 'weight': 70},
                          {'species': 'herbivore', 'age': 100, 'weight': 70},
                          {'species': 'herbivore', 'age': 100, 'weight': 70},
                          {'species': 'herbivore', 'age': 100, 'weight': 70},
                          ]}]
        for item in test3:
            cell_pop = item['pop']
            test_cell.add_pop(cell_pop)
        test_carnivore = [{'species': 'carnivore', 'age': 1,
                                    'weight': 6}]

        test_cell.add_pop(test_carnivore)
        test_cell.feed_carnivores()
        assert len(test_cell.population_herbivores) == 4

    def test_successfull_hunt(self):
        """
        Will test that a successfull hunt returns correct probability
        """
        test_herbivore = Herbivore(weight=20, age=5)
        test_carnivore = Carnivore(weight=10, age=80)
        hunt = self.test_cell.successful_hunt(test_carnivore, test_herbivore)
        assert hunt == 0
        test_herbivore = Herbivore(weight=20, age=5)
        test_carnivore = Carnivore(weight=10, age=20)
        hunt = self.test_cell.successful_hunt(test_carnivore, test_herbivore)
        assert 1 > hunt > 0
        test_herbivore = Herbivore(weight=150, age=100)
        test_carnivore = Carnivore(weight=3, age=1)
        hunt = self.test_cell.successful_hunt(test_carnivore, test_herbivore)
        assert hunt < 0.05

    def test_alter_population(self, test=test):
        """
        Will test that the animals die in correct fashion. This test is heavily
        dependent on Fauna.death. The randomness comes from that funcion. To
        test alter_population, we insert weight 0 to make sure the creature
        will die. The rest is up to the Fauna.deat() funtion.
        :param test:
        :return:
        """
        cell_pop = {}
        for item in test:
            cell_pop = item['pop']
        test_cell = Jungle()
        test_cell.add_pop(cell_pop)

        for creature in test_cell.population_herbivores:
            creature.weight = 0
        test_cell.alter_population()
        assert test_cell.number_herbivores() == 0

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
        # Will test that the creature only mates if they weigh enough.
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

    def test_get_abundance_herbivore(self):
        """
        Will test that the correct amount of abundant fodder is returned.
        """
        self.test_cell.fodder = 800
        population = 6
        f = 10
        test_abundance = self.test_cell.fodder / ((population + 1) * f)
        assert self.test_cell.get_abundance_herbivore() == test_abundance


    def test_get_abundance_carnivore(self, cell=test):
        """
        Will test that the correct amount of abundant fodder is returned.
        Will also test that it is zero if there are no herbivores in the cell.
        :param :
        :return:
        """
        cell_pop = {}
        test_cell = Jungle()
        for item in cell:
            cell_pop = item['pop']
            test_cell.add_pop(cell_pop)

        assert test_cell.get_abundance_carnivore() == 4
        assert self.test_cell.get_abundance_carnivore() == 0.92
        test_cell = Jungle()
        cell = self.carn_list
        for item in cell:
            cell_pop = item['pop']
            test_cell.add_pop(cell_pop)
        assert test_cell.get_abundance_carnivore() == 0

    def test_add_age(self, test=test):
        """
        Will test that all creatures get one year older from add_age function
        :param test: dict
        :return:
        """
        cell_pop = {}
        for item in test:
            cell_pop = item['pop']
        test_cell = Jungle()
        test_cell.add_pop(cell_pop)

        # Defines list with old age
        creature_count = test_cell.number_herbivores()
        age_list = []
        for i in range(creature_count):
            age_list.append(test_cell.population_herbivores[i].age)

        # Compares new age to old age + 1
        test_cell.add_age()
        for i in range(creature_count):
            assert test_cell.population_herbivores[i].age == age_list[i] + 1

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
        weight2 = []

        # Stores current weight in a list
        for i in range(test_cell.number_herbivores()):
            weight.append(test_cell.population_herbivores[i].weight)
        test_cell.lose_weight()

        # Compares new weight to old weight - eta * old weight
        # Also stores new weight in weight2 list
        for i in range(test_cell.number_herbivores()):
            new_weight = test_cell.population_herbivores[i].weight
            assert new_weight == weight[i] - weight[i] * 0.05
            weight2.append(new_weight)

        # Will now test that they lose weight once more, using weight2 list.
        test_cell.lose_weight()
        for i in range(test_cell.number_herbivores()):
            new_weight = test_cell.population_herbivores[i].weight
            assert new_weight == weight2[i] - weight2[i] * 0.05
