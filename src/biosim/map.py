#from biosim.fauna import Fauna

__author__ = 'Hans Kristian Lunda, Mikko Rekstad'
__email__ = 'hans.kristian.lunda@nmbu.no, mikkreks@nmbu.no'

from biosim.Cell import Cell, Ocean, Mountain, Desert, Savannah, Jungle
import biosim.Cell
import numpy as np



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
        self.cell_map = np.empty((self.n_rows, self.n_cols),dtype=object)
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
                    self.cell_map[row_index][col_index] = Ocean((row_index, col_index))
                elif landscape_type == 'M':
                    self.cell_map[row_index][col_index] = Mountain((row_index, col_index))
                elif landscape_type == 'D':
                    self.cell_map[row_index][col_index] = Desert((row_index, col_index))
                    self.define_adjacent_cells(row_index, col_index)
                    self.define_adjacent_cells2(row_index, col_index)
                elif landscape_type == 'S':
                    self.cell_map[row_index][col_index] = Savannah((row_index, col_index))
                    self.define_adjacent_cells(row_index, col_index)
                    self.define_adjacent_cells2(row_index, col_index)
                else:
                    self.cell_map[row_index][col_index] = Jungle((row_index, col_index))
                    self.define_adjacent_cells(row_index, col_index)
                    self.define_adjacent_cells2(row_index, col_index)

    def define_adjacent_cells(self, x_coord, y_coord):
        """
        Calculates the coordinates of the adjacent cells.
        :param x_coord:
        :param y_coord:
        :return:
        """
        if (x_coord != (0 or self.n_rows-1)) and (y_coord != (0 or self.n_cols-1)):
            self.cell_map[x_coord][y_coord].adjacent_cells = [self.cell_map[x_coord + 1][y_coord], self.cell_map[x_coord][y_coord - 1],
                                                              self.cell_map[x_coord - 1][y_coord], self.cell_map[x_coord][y_coord + 1]]
            # print("adj_Cells: ", self.cell_map[x_coord][y_coord].adjacent_cells)

    def define_adjacent_cells2(self, x, y):
        """
        Calculates the coordinates of the adjacent cells.
        :param x_coord:
        :param y_coord:
        :return:
        """
        self.cell_map[x][y].adjacent_cells2 = [(x+1, y),(x, y+1),
                                               (x-1, y),(x, y-1)]


    def migration(self):
        """
        This function will summon all functions related to migration.
        :return:
        """
        # Will update preferred location to each creature.
        self.update_preferred_locations()
        # for cell in self.cell_map:
        for x in range(self.n_rows):
            for y in range(self.n_cols):
                index = 0
                while index < self.cell_map[x][y].number_herbivores():
                    creature = self.cell_map[x][y].population_herbivores[index]
                    if creature.wants_to_migrate():
                        # print('A creature wants to migrate')
                        # selects a index based on probabilities and possible moves.
                        move_index = self.select_index_to_move(self.cell_map[x][y].probability_herbivores)
                        if move_index in [0, 1, 2, 3]:
                            move_to = self.cell_map[x][y].adjacent_cells2[move_index]
                            # Perhaps include cell.location?
                            move_from = x, y
                            # need creature index
                            self.move_herbivore(move_to, move_from, index)
                        index -=1
                    index += 1




    def update_preferred_locations(self):
        """
        !!! This need some adjustments but works for now.
        Will first update the lucrativeness for each cell.
        This gives the simulated effect that all creatures moves at the same
        time.
        Will then create a list with chances of moving to each cell.
        - For each species.
        NB! lucrativeness is the chance for a creature to move there if it
        will move at all.
        :return:
        """

        for x in range(self.n_rows):
            for y in range(self.n_cols):
                probabilities = [0, 0, 0, 0]
                propensities = [0, 0, 0, 0]
                # Yes this is wrong, need to divide by correct amount, now only correct when propensity is equal on all 4 sides.
                for index in range(len(self.cell_map[x][y].adjacent_cells2)):
                    lambda1 = 1
                    propensities[index] = np.exp(lambda1 * self.cell_map[x][y].get_abundance_herbivore())
                    # print('Propensity[index]: ', index)
                    #probability = propensity/(4*propensity)
                    #sum_probabilities += propensity


                if sum(propensities) != 0:
                    for i in range(len(propensities)):
                        probabilities[i] = propensities[i] / sum(propensities)
                    # print('Pobabilities to move: ', probabilities)
                    self.cell_map[x][y].probability_herbivores = probabilities

    def select_index_to_move(self, probabilities):
        """
        Uses probabilities to choose from destinations.
        NB! Requires 4 adjacent cells, and 4 probabilities to work.
        !! This should work
        :param probabilities: list
        :param destinations: list
        :return: tuple
        """
        if (sum(probabilities)) == 1:
            return np.random.choice([0, 1, 2, 3], p=probabilities)

    def move_herbivore(self, move_to, move_from, creature_index):
        """
        !!! This should work
        Moves the herbivore
        :param move_to: tuple
        :param move_from: tuple
        :param creature_index: int
        :return:
        """
        x_to, y_to = move_to
        x_from, y_from = move_from
        herbivore = self.cell_map[x_from][y_from].population_herbivores.pop(creature_index)
        self.cell_map[x_to][x_from].population_herbivores.append(herbivore)

    def move_to_preferred_location(self):
        """
        Will extract the creatures that wants to move, and then put them
        in their new habitat.
        :return:
        """
        for cell in self.cell_map:
            for herbivore in cell.population_herbivores:
                if herbivore.wants_to_migrate():
                    # Selects coordinates based on
                    x, y = np.random.choice(cell.adjacent_cells,
                                     p=cell.herbivore_preferrence)
                    cell_map.population_herbivores.append(list_one.pop(i))
            for carnivore in cell.population_carnivores:
                if carnivore.wants_to_migrate():
                    x, y =np.random.choice(cell.adjacent_cells,
                                     p=cell.herbivore_preferrence)
                    cell_map.population_carnivores.append(list_one.pop(i))

    def get_populations(self):
        herbivores = 0
        carnivores = 0
        for list_of_cells in self.cell_map:
            for cell in list_of_cells:
                herbivores += cell.number_herbivores()
                carnivores += cell.number_carnivores()
        total = herbivores + carnivores
        return herbivores, carnivores, total

    def yearly_stage1(self):
        """
        Here we wil feed and procreate. Names up for change.
        NB! The order is important. Fodder grows first.
        Used to have feed_map and procreate_map. But put them together.
        :return:
        """
        for list_of_cells in self.cell_map:
            for cell in list_of_cells:
                if cell.population_herbivores != []:
                    #print('Antall herbivores her: ', len(cell.population_herbivores))
                    for creature in cell.population_herbivores:
                        # Lets the creature be able to mate as well.
                        creature.have_mated = False
                        creature.fitness = creature.calculate_fitness()
                    cell.ranked_fitness_herbivores()
                    cell.add_fodder()
                    cell.feed_herbivores()
                    # print('Amount of fodder left this year: ', cell.fodder)
                    # OPS! Feed carnivores might need some more funcs
                    # cell.feed_carnivores()
                    cell.mating_season()


    def yearly_stage_2(self):
        """
        Here we will just summon the migration function when its redo.
        The function loops through the map and calls migrate for all the herbivores.
        :return:
        """

        # print("Yearly stage 2 has started")
        for row_index in range(self.n_rows):
            for col_index in range(self.n_cols):
                herbivore_list = self.cell_map[row_index][col_index].population_herbivores
                # herbivore_list = self.cell_map[row_index][col_index].get_herbivores()
                # print("herbivore list: ", herbivore_list)

                for herbivore in herbivore_list:
                    herbivore.migrate()
        # print("Yearly stage 2 has finished")


    def yearly_stage3(self):
        """
        4. aging, 5. Loss of weight and 6. Death.
        :return:
        """
        for list_of_cells in self.cell_map:
            for cell in list_of_cells:
                cell.add_age()
                cell.lose_weight()
                for creature in cell.population_herbivores:
                    creature.fitness = creature.calculate_fitness
                    creature.have_mated = False
                cell.alter_population()


    def yearly_cycle(self):
        # OPS! some of these functions can be put together
        self.yearly_stage1()
        # self.yearly_stage_2()
        # NB! first year none can mate
        self.migration()
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
    #test_map.show_map()
    #print((test_map.landscape_matrix))