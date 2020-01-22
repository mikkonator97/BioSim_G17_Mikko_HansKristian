
__author__ = 'Hans Kristian Lunda, Mikko Rekstad'
__email__ = 'hans.kristian.lunda@nmbu.no, mikkreks@nmbu.no'

from biosim.fauna import Fauna
from biosim.cell import Cell, Jungle, Ocean, Mountain, Savannah, Desert
from biosim.map import Map
from biosim.simulation import BioSim
import mock
import unittest

# Testing the operations within a function

class TestMap(unittest.TestCase):
    map_string = """\
                  OOOOOOOOOOOOOOOOOOOOO
                  OOOOOOOOSMMMMJJJJJJJO
                  OSSSSSJJJJMMJJJJJJJOO
                  OSSSSSSSSSMMJJJJJJOOO
                  OSSSSSJJJJJJJJJJJJOOO
                  OSSSSSJJJDDJJJSJJJOOO
                  OSSJJJJJDDDJJJSSSSOOO
                  OOSSSSJJJDDJJJSOOOOOO
                  OSSSJJJJJDDJJJJJJJOOO
                  OSSSSJJJJDDJJJJOOOOOO
                  OOSSSSJJJJJJJJOOOOOOO
                  OOOSSSSJJJJJJJOOOOOOO
                  OOOOOOOOOOOOOOOOOOOOO"""
    test = [{'loc': (10, 10),
             'pop': [{'species': 'herbivore', 'age': 10, 'weight': 15},
                     {'species': 'herbivore', 'age': 5, 'weight': 40},
                     {'species': 'herbivore', 'age': 5, 'weight': 40},
                     {'species': 'herbivore', 'age': 5, 'weight': 40},
                     {'species': 'herbivore', 'age': 5, 'weight': 40},
                     {'species': 'herbivore', 'age': 15, 'weight': 25}]}]

    test_both = [{'loc': (10, 10),
             'pop': [{'species': 'carnivore', 'age': 10, 'weight': 15},
                     {'species': 'carnivore', 'age': 5, 'weight': 40},
                     {'species': 'carnivore', 'age': 5, 'weight': 40},
                     {'species': 'herbivore', 'age': 5, 'weight': 40},
                     {'species': 'herbivore', 'age': 5, 'weight': 40},
                     {'species': 'herbivore', 'age': 15, 'weight': 25}]}]

    map = Map(map_string)

    def setUp(self, test=test, map_string=map_string):
        print('SetUP')
        self.map2 = Map(map_string)
        for item in test:
           i, j = item['loc']
           cell_pop = item['pop']
           self.map2.cell_map[i][j].add_pop(cell_pop)




    cell_pop = {}
    for item in test:
        cell_pop = item['pop']

    def test_creates_map(self, map=map):
        """
        Tests that the map is created.
        :return:
        """
        assert map is not None
        assert map.cell_map[0][0].landscape == 0
        assert map.cell_map[10][10].landscape == 4

    def test_get_populations(self):
        """
        Will test that once a population is added, we can get it using the
        get_populations function. The population is added in the setUp func.
        :return:
        """
        assert self.map2.get_populations() == (6, 0, 6)

    def test_list_of_adjacent_cells(self):
        """
        Will test that the list of adjacent cells is correct.
        It is supposed to be a list of tuples.
        Remember, mountain and oceans does not get adjacent cells.
        :return:
        """
        assert (10, 11) in self.map2.cell_map[10][10].adjacent_cells2
        assert self.map2.cell_map[10][10].adjacent_cells2 == [(11,10),(10,11),
                                                       (9,10),(10,9)]

    def test_preferred_list_middle_of_jungle(self, map=map):
        """
        We will now test that the list of preferrence displays the correct
        probabilities for herbivores when surrounded by jungle.
        !!! Remember to enable parameter change to attractiveness func...
        :param map: object
        :return:
        """
        map.update_preferred_locations()
        assert map.cell_map[8][6].probability_herbivores == [0.25, 0.25, 0.25,
                                                            0.25]
        # assert map.cell_map[8][6].herbivore_preferrence == [0.25, 0.25, 0.25, 0.25]

    def test_doesnt_prefere_unhabitable_cells(self, map=map):
        """
        Will test that a creature will not move to an unhabitable cell.
        :param map: object
        :return:
        """
        test_herb = [{'loc': (1, 1),
                 'pop': [{'species': 'herbivore', 'age': 10, 'weight': 15}]}]

        sim = BioSim(island_map="OOO\nOJO\nOOO", ini_pop=test_herb, seed=1)
        sim.map.migration()
        assert sim.map.cell_map[1][1].number_herbivores() == 1


    #mock.patch("biosim.map.choice", return_value=1, autospec=True)
    @mock.patch("biosim.map.choice", return_value=1, autospec=True)
    def test_select_index_to_move(self, mock_choice, map=map):
        probabilities_index_test = [0, 0.25, 0.75, 0.25]
        index = map.select_index_to_move(probabilities_index_test)
        assert index == 1
        mock_choice.assert_called_once_with(1)

    def test_migration(self, map=map_string, pop2=test_both):
        """
        Will test that herbivores are removed from old cell, and that there
        are more in another cell.

        Also tests that carnivores does not move when there are no herbivores
        nextdoor.
        :param map:
        :param pop:
        :return:
        """
        assert self.map2.cell_map[10][10].number_herbivores() == 6
        self.map2.migration()
        assert self.map2.cell_map[10][10].number_herbivores() != 6

        # Now adds population with both species.
        for item in pop2:
            i, j = item['loc']
            cell_pop2 = item['pop']
            self.map2.cell_map[i][j].add_pop(cell_pop2)

        # Now there are only creatures in 10, 10, so they should now move
        assert self.map2.cell_map[10][10].number_carnivores() == 3
        self.map2.migration()
        assert self.map2.cell_map[10][10].number_carnivores() == 3

    def test_carnivores_follow_herbivores(self, map1=map):
        """
        NB! This test might be redundant, carnivores can still move even though
        there are no adjacent herbivores....
        First we create a big population of both species. Now we test that the
        carnivores does not move after first call of migration.
        The next call we can expect that the population of carnivores in the
        starting cell has changed. We will do this with a mock. OR HIGH POPS.
        :return:
        """
        n_herbs = 1000
        n_carns = 1000
        ini_herbs = [
            {
                "loc": (10, 10),
                "pop": [
                    {"species": "Herbivore", "age": 5, "weight": 20}
                    for _ in range(n_herbs)
                ],
            },
        ]

        ini_carns = [
            {
                "loc": (10, 10),
                "pop": [
                    {"species": "Carnivore", "age": 5, "weight": 20}
                    for _ in range(n_carns)
                ],
            }
        ]

        for item in ini_herbs:
            i, j = item['loc']
            cell_herbivores = item['pop']
            map1.cell_map[i][j].add_pop(cell_herbivores)

        for item in ini_carns:
            i, j = item['loc']
            cell_carnivores = item['pop']
            map1.cell_map[i][j].add_pop(cell_carnivores)

        # Make sure that the correct amount is at first.
        assert map1.get_populations() == (n_herbs, n_carns, n_herbs + n_carns)
        assert map1.cell_map[10][10].number_carnivores() == n_carns
        assert map1.cell_map[10][10].number_herbivores() == n_herbs
        # Make sure that only herbivores move first round.
        map1.migration()
        assert map1.cell_map[10][10].number_carnivores() == n_carns
        assert map1.cell_map[10][10].number_herbivores() != n_herbs
        # Looks like carnivores follow herbivores straight away, easy fix if we
        # want to, just switch order, think we will keep it.
        # Make sure that both populations are different that initially
        map1.migration()
        assert map1.cell_map[10][10].number_carnivores() != n_carns
        assert map1.cell_map[10][10].number_herbivores() != n_herbs

    def test_reset_migration_mated(self):
        """
        :return:
        """
        self.map2.migration()
        self.map2.cell_map[10][10].mating_season()
        self.map2.reset_mated_migration(self.map2.cell_map[10][10])

        for herbivore in self.map2.cell_map[10][10].population_herbivores:
            assert not herbivore.have_mated
            assert not herbivore.have_migrated

        for carnivore in self.map2.cell_map[10][10].population_carnivores:
            assert not carnivore.have_mated
            assert not carnivore.have_migrated

    def test_yearly_cycle_age(self):
        """
        Will test that yearly cycle alters the population.
        :return:
        """

        age_herbivores = []
        for herbivore in self.map2.cell_map[10][10].population_herbivores:
            age_herbivores.append(herbivore.age)

        age_carnivores = []
        for carnivore in self.map2.cell_map[10][10].population_carnivores:
            age_carnivores.append(carnivore.age)

        pop_before = self.map2.get_populations()
        self.map2.yearly_cycle()
        # Tests that there are a different number of creatures.
        assert pop_before != self.map2.get_populations()
