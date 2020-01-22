# -*- coding: utf-8 -*-

__author__ = 'Hans Kristian Lunda, Mikko Rekstad'
__email__ = 'hans.kristian.lunda@nmbu.no, mikkreks@nmbu.no'

from biosim.cell import Ocean, Mountain, Desert, Savannah, Jungle
import numpy as np
import math
from numba import jit


class Map:
    """
    Creates a numpy array with the coordinates of the map based on
    multi_line_map_string, and add the corresponding landscape type.
    """
    def __init__(self, map_string):
        """
        Will create the map as an array, containing objects with cells.
        Will also create a matrix in order to be able to visualize the map
        easier later.
        """

        self.map_string_split = map_string.split()
        self.n_rows = len(self.map_string_split)
        self.n_cols = len(str(self.map_string_split[0]))
        self.cell_map = np.empty((self.n_rows, self.n_cols), dtype=object)
        self.map_matrix = np.zeros((self.n_rows, self.n_cols))
        self.map_herbivores = np.zeros((self.n_rows, self.n_cols))
        self.map_carnivores = np.zeros((self.n_rows, self.n_cols))
        self.create_map()

    def create_map(self):
        """
        Creates the map with cell objects and add lists with the adjacent
         cell cordinates to each cell object.
        :return:
        """
        for row_index in range(self.n_rows):
            for col_index in range(self.n_cols):
                landscape_type = self.map_string_split[row_index][col_index]
                if landscape_type == 'O':
                    self.cell_map[row_index][col_index] = Ocean()
                    self.map_matrix[row_index][col_index] = 0
                elif landscape_type == 'M':
                    self.cell_map[row_index][col_index] = Mountain()
                    self.map_matrix[row_index][col_index] = 1
                elif landscape_type == 'D':
                    self.cell_map[row_index][col_index] = Desert()
                    self.define_adjacent_cells(row_index, col_index)
                    self.map_matrix[row_index][col_index] = 2
                elif landscape_type == 'S':
                    self.cell_map[row_index][col_index] = Savannah()
                    self.define_adjacent_cells(row_index, col_index)
                    self.map_matrix[row_index][col_index] = 3
                else:
                    self.cell_map[row_index][col_index] = Jungle()
                    self.define_adjacent_cells(row_index, col_index)
                    self.map_matrix[row_index][col_index] = 4

    def define_adjacent_cells(self, x_coord, y_coord):
        """
        Calculates the coordinates of the adjacent cells.
        :param x_coord:
        :param y_coord:
        :return:
        """
        self.cell_map[x_coord][y_coord].adjacent_cells2 = [
            (x_coord + 1, y_coord), (x_coord, y_coord + 1),
            (x_coord - 1, y_coord), (x_coord, y_coord - 1)
        ]

    def migration(self):
        """
        This function will summon all functions related to migration.
        :return:
        """
        # Will update preferred location to each creature.
        self.update_preferred_locations()
        # for cell in self.cell_map:
        for y_coord in range(self.n_cols):
            for x_coord in range(self.n_rows):
                self.migrate_herbivores(self.cell_map[x_coord][y_coord],
                                        x_coord, y_coord)
                self.migrate_carnivores(self.cell_map[x_coord][y_coord],
                                        x_coord, y_coord)

    def migrate_herbivores(self, cell, x_coord, y_coord):
        """
        The function checks if the herbivores in the cell want to migrate
        to one of the adjacent cells, then move them to one of the these cells.
        :param cell: np.array
        :param x_coord: int
        :param y_coord: int
        :return:
        """
        index = 0
        while index < cell.number_herbivores():
            creature =\
                self.cell_map[x_coord][y_coord].population_herbivores[index]

            if creature.wants_to_migrate():
                move_index = self.select_index_to_move(
                    cell.probability_herbivores)
                if move_index in [0, 1, 2, 3]:
                    move_to = cell.adjacent_cells2[move_index]
                    move_from = x_coord, y_coord
                    if self.cell_map[move_to[0]][move_to[1]].habitable:
                        self.move_herbivore(move_to, move_from, index)
                index -= 1
            index += 1

    def migrate_carnivores(self, cell, x_coord, y_coord):
        """
        The function checks if the carnivores in the cell want to migrate
        to one of the adjacent cells, then move them to one of the these cells.
        :param cell: np.array
        :param x_coord: int
        :param y_coord: int
        :return:
        """
        index = 0
        while index < cell.number_carnivores():
            creature =\
                self.cell_map[x_coord][y_coord].population_carnivores[index]
            if creature.wants_to_migrate():
                move_index = self.select_index_to_move(
                    cell.probability_carnivores)
                if move_index in [0, 1, 2, 3]:
                    move_to = cell.adjacent_cells2[move_index]
                    move_from = x_coord, y_coord
                    if self.cell_map[move_to[0]][move_to[1]].habitable:
                        self.move_carnivore(move_to, move_from, index)
                index -= 1
            index += 1

    def update_preferred_locations(self):
        """
        Will first update the lucrativeness for each cell.
        This gives the simulated effect that all creatures moves at the same
        time.
        Will then create a list with chances of moving to each cell.
        - For each species.
        NB! lucrativeness is the chance for a creature to move there if it
        will move at all.
        :return:
        """

        for y_coordinate in range(self.n_cols-1):
            for x_coordinate in range(self.n_rows-1):
                # Setting default values to 0

                # Find propensities for each cell.
                propensities_herbivores, propensities_carnivores = \
                    self.get_propensities(y_coordinate, x_coordinate)

                # Turn propensities into probabilities
                self.convert_into_probabilities(propensities_herbivores,
                                                propensities_carnivores,
                                                x_coordinate, y_coordinate)

    def get_propensities(self, y_coordinate, x_coordinate):
        """
        Takes two lists of zeros, and turns them into lists containing the
        propensities of fodder for each species. Each value in the list
        represents an adjacent cell.
        :param y_coordinate: int
        :param x_coordinate: int
        :return:
        """
        propensities_herbivores = [0, 0, 0, 0]
        propensities_carnivores = [0, 0, 0, 0]
        index = 0
        for adjacent_cell in self.cell_map[x_coordinate][
                                            y_coordinate].adjacent_cells2:
            x_adjacent, y_adjacent = adjacent_cell
            lambda1 = 1

            # Inserting propensity into lists
            herbivore_abundance = self.cell_map[x_adjacent][
                y_adjacent].get_abundance_herbivore()
            propensities_herbivores[index] = math.exp(
                lambda1 * herbivore_abundance)

            carnivore_abundance = self.cell_map[x_adjacent][
                y_adjacent].get_abundance_carnivore()
            propensities_carnivores[index] = math.exp(
                lambda1 * carnivore_abundance)
            index += 1
        return propensities_herbivores, propensities_carnivores

    def convert_into_probabilities(self, propensities_herbivores,
                                   propensities_carnivores, x_coordinate,
                                   y_coordinate):
        """
        Takes the lists containing propensities and calculates probabilities
        for each species to migrate to the cell represented by the index of
        that list.
        :param propensities_herbivores: list
        :param propensities_carnivores: list
        :param x_coordinate: int
        :param y_coordinate: int
        :return:
        """
        probabilities_herbivores = [0, 0, 0, 0]
        probabilities_carnivores = [0, 0, 0, 0]

        if sum(propensities_herbivores) != 0:
            for i in range(len(propensities_herbivores)):
                probabilities_herbivores[i] = propensities_herbivores[i] / sum(
                    propensities_herbivores)
            self.cell_map[x_coordinate][
                y_coordinate].probability_herbivores = probabilities_herbivores

        if sum(propensities_carnivores) != 0:
            for i in range(len(propensities_carnivores)):
                probabilities_carnivores[i] = propensities_carnivores[i] / sum(
                    propensities_carnivores)
            self.cell_map[x_coordinate][
                y_coordinate].probability_carnivores = probabilities_carnivores
        # return propensities_herbivores, probabilities_carnivores

    def select_index_to_move(self, probabilities):
        """
        Uses the list of probabilities as a parameter to choose a number
        between 0 and 3. The number represents the index the creature will use
        in order to migrate.
        :param probabilities: list
        :return: int
        """
        if (sum(probabilities)) == 1:
            return np.random.choice([0, 1, 2, 3], p=probabilities)

    def move_herbivore(self, move_to, move_from, creature_index):
        """
        Moves the herbivore from move_from to move_to. They are both tuples,
        and contain coordinates which will be used as indexes from removal and
        adding of the creature. The creature is selected with creature_index.
        :param move_to: tuple
        :param move_from: tuple
        :param creature_index: int
        :return:
        """
        x_to, y_to = move_to
        x_from, y_from = move_from
        herbivore = self.cell_map[x_from][y_from].population_herbivores.pop(
            creature_index)
        self.cell_map[x_to][y_to].population_herbivores.append(herbivore)

    def move_carnivore(self, move_to, move_from, creature_index):
        """
        Moves the carnivore from move_from to move_to. They are both tuples,
        and contain coordinates which will be used as indexes from removal and
        adding of the creature. The creature is selected with creature_index.
        :param move_to: tuple
        :param move_from: tuple
        :param creature_index: int
        :return:
        """
        x_to, y_to = move_to
        x_from, y_from = move_from
        carnivore = self.cell_map[x_from][y_from].population_carnivores.pop(
            creature_index)
        self.cell_map[x_to][y_to].population_carnivores.append(carnivore)

    def get_populations(self):
        """
        Returns the number of herbivores, carnivores and the sum of these two.
        :return: int
        """
        herbivores = 0
        carnivores = 0
        for list_of_cells in self.cell_map:
            for cell in list_of_cells:
                herbivores += cell.number_herbivores()
                carnivores += cell.number_carnivores()
        total = herbivores + carnivores
        return herbivores, carnivores, total

    def reset_mated_migration(self, cell):
        """
        Set the creatures have_migrated and have_mated attribute to False
        and is called at the end of each year.
        :param cell:
        :return:
        """
        for creature in cell.population_herbivores:
            creature.have_mated = False
            creature.have_migrated = False
        for creature in cell.population_carnivores:
            creature.have_mated = False
            creature.have_migrated = False
    @jit()
    def feeding_and_procreation(self):
        """
        Yearly stage 1 handles the addition of fodder to each cell,
        feeding for both species, and procreation of both species.
        Here we wil feed and procreate. Names up for change.
        NB! The order is important. Fodder grows first.
        Used to have feed_map and procreate_map. But put them together.
        :return:
        """
        for row_index in range(self.n_rows):
            for col_index in range(self.n_cols):
                current_cell = self.cell_map[row_index][col_index]
                if current_cell.landscape in {2, 3, 4}:
                    current_cell.add_fodder()
                    # Feed the herbivores
                    for creature in current_cell.population_herbivores:
                        #creature.fitness = creature.calculate_fitness()
                        current_cell.ranked_fitness_herbivores()
                        current_cell.feed_herbivores(creature)

                    # Feed the carnivores
                    if len(current_cell.population_carnivores) > 0:
                        # for carnivore in current_cell.population_carnivores:
                            #carnivore.fitness = carnivore.calculate_fitness()
                        current_cell.ranked_fitness_carnivores()
                        current_cell.feed_carnivores()
                    current_cell.mating_season()

    def ageing_weight_loss_and_death(self):
        """
        This function makes the creatures one year older, causes them to
        lose weight according to some beta and their current weight,
        then calculate their fitness before altering the population.
        Altering population checks if the creature dies based and removes it
        from the population if that is the case.
        :return:
        """
        for row_index in range(self.n_rows):
            for col_index in range(self.n_cols):

                cell = self.cell_map[row_index][col_index]
                if cell.landscape in {2, 3, 4}:
                    cell.add_age()
                    cell.lose_weight()
                    self.reset_mated_migration(cell)
                    cell.alter_population()

    def yearly_cycle(self):
        """
        Will run through each stage of the yearly cycle.
        :return:
        """
        self.feeding_and_procreation()
        self.migration()
        self.ageing_weight_loss_and_death()

    def get_population_maps(self):
        """
        Calculate the number of herbivores and carnivores and place them
        in a map.
        :return:
        """
        for x_cords in range(self.n_rows):
            for y_cords in range(self.n_cols):
                self.map_herbivores[x_cords][y_cords] = self.cell_map[x_cords][
                    y_cords].number_herbivores()
                self.map_carnivores[x_cords][y_cords] = self.cell_map[x_cords][
                    y_cords].number_carnivores()
