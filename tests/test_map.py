
__author__ = 'Hans Kristian Lunda, Mikko Rekstad'
__email__ = 'hans.kristian.lunda@nmbu.no, mikkreks@nmbu.no'

from biosim.fauna import Fauna
from biosim.cell import Cell, Jungle, Ocean, Mountain, Savannah, Desert
from biosim.map import Map
from biosim.simulation import BioSim
import mock
import unittest

# Testing the operations within a function

class TestMap:
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

    map = Map(map_string)

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

    def test_get_populations(self, map_string=map_string, pop=test):
        """
        Will test that once a population is added, we can get it using the
        get_populations function.
        :param map:
        :param pop:
        :return:
        """
        map2 = Map(map_string)
        for item in pop:
            i, j = item['loc']
            cell_pop = item['pop']
            map2.cell_map[i][j].add_pop(cell_pop)
        assert map2.get_populations() == (6, 0, 6)

    def test_list_of_adjacent_cells(self, map=map):
        """
        Will test that the list of adjacent cells is correct.
        It is supposed to be a list of tuples.
        !!! Remember, mountain and oceans does not get adjacent cells.
        :param map:
        :return:
        """
        assert (10, 11) in map.cell_map[10][10].adjacent_cells2
        assert map.cell_map[10][10].adjacent_cells2 == [(11,10),(10,11),
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


    @mock.patch("biosim.map.choice", return_value=1, autospec=True)
    def test_select_index_to_move(self, mock_choice, map=map):
        probabilities_index_test = [0, 0.25, 0.75, 0.25]
        index = map.select_index_to_move(probabilities_index_test)
        assert index == 1
        mock_choice.assert_called_once_with(1)


    def test_creature_moves_to_preferred(self, map=map, pop=test):
        """
        If the creature is supposed to move: test that the creature will be
        removed from the previous cell. Then ensure that it has been added to
        the new cell.
        :param map: object.
        :param test: dict.
        :return:
        """
        pass

    def test_move(self, map=map):
        # map.move()
        pass

    def test_migration(self, map=map_string, pop=test):
        """
        Will test that herbivores are removed from old cell, and that there
        are more in another cell.
        :param map:
        :param pop:
        :return:
        """

        map1 = Map(map)
        for item in pop:
            i, j = item['loc']
            cell_pop = item['pop']
            map1.cell_map[i][j].add_pop(cell_pop)
        assert map1.cell_map[10][10].number_herbivores() == 6
        map1.migration()
        assert map1.cell_map[10][10].number_herbivores() != 6



