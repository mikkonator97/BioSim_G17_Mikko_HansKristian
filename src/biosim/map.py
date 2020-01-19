# from biosim.fauna import Fauna

__author__ = 'Hans Kristian Lunda, Mikko Rekstad'
__email__ = 'hans.kristian.lunda@nmbu.no, mikkreks@nmbu.no'

from biosim.Cell import Cell, Ocean, Mountain, Desert, Savannah, Jungle
import biosim.Cell
import numpy as np
import math



class Map:
    """
    Creates a dictionary with the coordinates of the map based on
    multi_line_map_string, and add the corresponding landscape type
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
        for y in range(self.n_cols):
            for x in range(self.n_rows):
                self.migrate_herbivores(self.cell_map[x][y], x, y)
                self.migrate_carnivores(self.cell_map[x][y], x, y)

    def migrate_herbivores(self, cell, x, y):
        index = 0
        while index < cell.number_herbivores():
            creature = self.cell_map[x][y].population_herbivores[index]
            if creature.wants_to_migrate():
                move_index = self.select_index_to_move(
                    cell.probability_herbivores)
                if move_index in [0, 1, 2, 3]:
                    move_to = cell.adjacent_cells2[move_index]
                    move_from = x, y
                    if self.cell_map[move_to[0]][move_to[1]].habitable:
                        self.move_herbivore(move_to, move_from, index)
                index -= 1
            index += 1

    def migrate_carnivores(self, cell, x, y):
        index = 0
        while index < cell.number_carnivores():
            creature = self.cell_map[x][y].population_carnivores[index]
            if creature.wants_to_migrate():
                move_index = self.select_index_to_move(
                    cell.probability_carnivores)
                if move_index in [0, 1, 2, 3]:
                    move_to = cell.adjacent_cells2[move_index]
                    move_from = x, y
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
                probabilities_herbivores = [0, 0, 0, 0]
                propensities_herbivores = [0, 0, 0, 0]
                probabilities_carnivores = [0, 0, 0, 0]
                propensities_carnivores = [0, 0, 0, 0]
                index = 0
                for adjacent_cell in self.cell_map[x_coordinate][y_coordinate].adjacent_cells2:
                    x_adjacent, y_adjacent = adjacent_cell
                    lambda1 = 1

                    # Inserting propensity into lists
                    herbivore_abundance = self.cell_map[x_adjacent][y_adjacent].get_abundance_herbivore()
                    propensities_herbivores[index] = math.exp(lambda1 * herbivore_abundance)

                    carnivore_abundance = self.cell_map[x_adjacent][y_adjacent].get_abundance_carnivore()
                    propensities_carnivores[index] = math.exp(lambda1 * carnivore_abundance)

                    index += 1

                # Turning the propensities into probability
                if sum(propensities_herbivores) != 0:
                    for i in range(len(propensities_herbivores)):
                        probabilities_herbivores[i] = propensities_herbivores[i] / sum(propensities_herbivores)
                    self.cell_map[x_coordinate][y_coordinate].probability_herbivores = probabilities_herbivores

                if sum(propensities_carnivores) != 0:
                    for i in range(len(propensities_carnivores)):
                        probabilities_carnivores[i] = propensities_carnivores[i] / sum(propensities_carnivores)
                    self.cell_map[x_coordinate][y_coordinate].probability_carnuvires = probabilities_carnivores


    def select_index_to_move(self, probabilities):
        """
        Uses probabilities to choose from destinations.
        NB! Requires 4 adjacent cells, and 4 probabilities to work.
        :param probabilities: list
        :param destinations: list
        :return: tuple
        """
        if (sum(probabilities)) == 1:
            return np.random.choice([0, 1, 2, 3], p=probabilities)

    def move_herbivore(self, move_to, move_from, creature_index):
        """
        Moves the herbivore
        :param move_to: tuple
        :param move_from: tuple
        :param creature_index: int
        :return:
        """
        x_to, y_to = move_to
        x_from, y_from = move_from
        herbivore = self.cell_map[x_from][y_from].population_herbivores.pop(creature_index)
        self.cell_map[x_to][y_to].population_herbivores.append(herbivore)

    def move_carnivore(self, move_to, move_from, creature_index):
        """
        Moves the carnivore
        :param move_to: tuple
        :param move_from: tuple
        :param creature_index: int
        :return:
        """
        x_to, y_to = move_to
        x_from, y_from = move_from
        carnivore = self.cell_map[x_from][y_from].population_carnivores.pop(creature_index)
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
        for creature in cell.population_herbivores:
            creature.have_mated = False
            creature.have_migrated = False
        for creature in cell.population_carnivores:
            creature.have_mated = False
            creature.have_migrated = False

    def yearly_stage1(self):
        """
        Yearly stage 1 handles the addition of fodder to each cell, feeding for both species,
        and procreation of both species.
        Here we wil feed and procreate. Names up for change.
        NB! The order is important. Fodder grows first.
        Used to have feed_map and procreate_map. But put them together.
        :return:
        """

        # code for carrying out feeding and procreation for each cell
        for row_index in range(self.n_rows):
            for col_index in range(self.n_cols):
                if self.cell_map[row_index][col_index].landscape in {2, 3, 4}:
                    self.cell_map[row_index][col_index].add_fodder()
                    for creature in self.cell_map[row_index][col_index].population_herbivores:
                        creature.fitness = creature.calculate_fitness()
                        self.cell_map[row_index][col_index].ranked_fitness_herbivores()
                        self.cell_map[row_index][col_index].feed_herbivores(creature)
                    # Note to self: re-calculate fitness of hervbivores since weight has been increased?
                    for creature in self.cell_map[row_index][col_index].population_herbivores:
                        creature.fitness = creature.calculate_fitness()

                    if len(self.cell_map[row_index][col_index].population_carnivores) > 0:
                        for carnivore_creature in self.cell_map[row_index][col_index].population_carnivores:
                            carnivore_creature.fitness = carnivore_creature.calculate_fitness()
                            self.cell_map[row_index][col_index].ranked_fitness_carnivores()
                            self.cell_map[row_index][col_index].feed_carnivores()
                        # print("All carnivores in this cell have eaten!")
                    self.cell_map[row_index][col_index].mating_season()
                    # print("Mating season over")

    def yearly_stage2(self):
        """
        This function calls the migration function which handles the migration for both species.
        :return:
        """
        self.migration()


    def yearly_stage3(self):
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
                    sum_age = 0
                    for herbivore in cell.population_herbivores:
                        sum_age += herbivore.age
                    if len(cell.population_herbivores) != 0:
                        g = sum_age / len(cell.population_herbivores)
                        # print('Average age: ', g)

    def yearly_cycle(self):
    #     # OPS! some of these functions can be put together
        self.yearly_stage1()
    #     # NB! first year none can mate
        self.migration()
    #     # self.yearly_stage2()
        self.yearly_stage3()


if __name__ == "__main__":
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

    test_map = Map(map_string)
    # print('f_max in a jungle cell: ', test_map.cell_map[10][10].f_max)
    # print('the adjecent cells to the same cell ([10][10])', test_map.cell_map[10][10].adjecent_cells)
    y, x = test_map.cell_map[10][10].adjecent_cells[0]
    # print(y,x)
    # test_map.show_map()
    # print((test_map.landscape_matrix))
