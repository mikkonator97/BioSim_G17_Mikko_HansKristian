from biosim.fauna import Fauna

__author__ = 'Hans Kristian Lunda, Mikko Rekstad'
__email__ = 'hans.kristian.lunda@nmbu.no, mikkreks@nmbu.no'

from biosim.Cell import Cell, Ocean, Mountain, Desert, Savannah, Jungle
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt


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
        # self.adjacent_cells = []

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
                elif landscape_type == 'M':
                    self.cell_map[row_index][col_index] = Mountain()
                elif landscape_type == 'D':
                    self.cell_map[row_index][col_index] = Desert()
                    self.define_adjacent_cells(row_index, col_index)
                elif landscape_type == 'S':
                    self.cell_map[row_index][col_index] = Savannah()
                    self.define_adjacent_cells(row_index, col_index)
                else:
                    self.cell_map[row_index][col_index] = Jungle()
                    self.define_adjacent_cells(row_index, col_index)

    def define_adjacent_cells(self, x_coord, y_coord):
        """
        Calculates the coordinates of the adjacent cells.
        :param x_coord:
        :param y_coord:
        :return:
        """
        self.cell_map[x_coord][y_coord].adjacent_cells = [(x_coord + 1, y_coord), (x_coord, y_coord - 1),
                                                          (x_coord - 1, y_coord), (x_coord, y_coord + 1)]

    def find(self, coordinate_to_find):
        for index in range(len(self.cell_map)):
            if self.cell_map[index].coordinate == coordinate_to_find:
                return index

    def show_map(self):
        landscape_matrix = np.zeros((self.n_rows, self.n_cols))
        for row_index in range(self.n_rows):
            for col_index in range(self.n_cols):
                landscape_matrix[row_index][col_index] = self.cell_map[row_index][col_index].landscape
        cmap = mpl.colors.ListedColormap(['royalblue', 'grey', 'khaki', 'honeydew', 'forestgreen'])
        plt.imshow(landscape_matrix, cmap=cmap)
        plt.show()

    # def migrate(self):
    #     """
    #     Calculates the migration for each animal on the map,
    #     then moves them to their new destination.
    #     :return:
    #     """
    #     # Note to self: Må bruke antall dyr før man kjører migrate...
    #     creatures_to_move = []
    #
    #     for x_coord in range(1, self.n_rows):
    #         for y_coord in range(1, self.n_cols):
    #             # for cell in self.cell_map:
    #             current_cell = self.cell_map[x_coord][y_coord]
    #
    #             # adj_cells = self.cell_map[i][j].adjacent_cells
    #             print('current cell', current_cell)
    #             migrating_probabilities = self.get_destination_probabilities(x_coord, y_coord)
    #             print('Migration', migrating_probabilities)
    #
    #             # migrating_probabilities = cell.find_migration()
    #             for creature in current_cell.population:
    #                 if creature.wants_to_migrate():
    #                     chosen_probabilty = np.random.choice(migrating_probabilities)
    #                     index = migrating_probabilities.index[chosen_probabilty]
    #                     current_x_coord, current_y_coord = current_cell.adjecent_cells[index]
    #                     print('A creature has moved')
    #                     creature.desired_location(current_x_coord, current_y_coord)
    #                     creatures_to_move.append(creature)
    #
    #     for creature in creatures_to_move:
    #         for x_coord in self.n_rows:
    #             for y_coord in self.n_cols:
    #                 if self.cell_map[x_coord][y_coord] != creature.desired_location:
    #                     self.cell_map[x_coord][y_coord].population += cell.population.pop(creature)
    #                     creature.desired_location = (x_coord, y_coord)

    # def get_destination_probabilities(self, x_coord, y_coord):
    #     """
    #     Calculates the probability of moving to each of the adjacent cells,
    #      then returns a list with these probabilities.
    #     :param x_coords: int
    #     :param y_coords: int
    #     :return: list
    #     """
    #     highest_relevance = []
    #     # print("adjacent cells", self.cell_map[i][j].adjacent_cells)
    #
    #     # print('adjacent cells', adjecent_cells)
    #     for tup in self.cell_map[x_coord][y_coord].adjacent_cells:
    #         print('tup', tup)
    #         new_x_coord, new_y_coord = tup
    #         # print("landscape ", self.cell_map[i][j].landscape)
    #         if self.cell_map[new_x_coord][new_y_coord].landscape in {3, 4}:
    #             fodder = self.cell_map[new_x_coord][new_y_coord].attractiveness_herbivore()
    #             print("Fodder ", fodder)
    #             propensity = np.exp(Fauna.lambda1[0]*fodder)
    #             highest_relevance.append(propensity)
    #
    #     probability_to_move = []
    #     for index in highest_relevance:
    #         probability_to_move.append(highest_relevance[index]/sum(highest_relevance))
    #     return probability_to_move

    def get_populations(self):
        herbivores = 0
        carnivores = 0
        total = 0
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
                for creature in cell.population_herbivores:
                    creature.fitness = creature.calculate_fitness()
                cell.ranked_fitness()
                cell.add_fodder()
                cell.feed_herbivores()
                # print('Amount of fodder left this year: ', cell.fodder)
                # OPS! Feed carnivores might need some more funcs
                # cell.feed_carnivores()
                cell.mating_season()


    def yearly_stage_2(self):
        """
        Here we will just summon the migration funcion when its redo.
        :return:
        """
        pass

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
                    if creature.weight < 0:
                        print('Warning, serious bug. Creatures can weigh < 0.')
                    cell.alter_population()

    def yearly_cycle(self):
        # OPS! some of these functions can be put together
        self.yearly_stage1()
        self.yearly_stage_2()
        # NB! first year none can mate
        self.yearly_stage3()








"""
dictionary = {}
antall_rader = len(map_string_split)
for i in range(antall_rader):
    old_value = str(map_string_split[i])
    new_value = old_value.replace(' ','')
    map_string_split[i] = new_value
    # print(map_string_split[i])
    antall_kolonnner = len(str(map_string_split[0]))
    for j in range(antall_kolonner):
        dictionary[i, j] = map_string_split[i][j]

print(dictionary)"""

# def population(list_of_dicts):
#     population_list = []
#     position = list_of_dicts[0].get('loc')
#     print(position)
#     print(list_of_dicts[1].get('pop'))
#     for i, item in enumerate(list_of_dicts[1].get('pop')):
#         species = list_of_dicts[i].get('species')
#         print(species)
#         age = list_of_dicts[i].get('age')
#         print(age)
#
#         weight = list_of_dicts[i].get('weight')
#         print(weight)
#         population_list.append(Fauna(position, species, age, weight))
#
# for d in pop:
#     location = d['loc']
#     cell_pop = d['pop']
#     #finn hvilken celle tilhører pop, kall den celle
#     celle.add_pop(cell_pop)

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
    print('f_max in a jungle cell: ', test_map.cell_map[10][10].f_max)
    print('the adjecent cells to the same cell ([10][10])', test_map.cell_map[10][10].adjecent_cells)
    y, x = test_map.cell_map[10][10].adjecent_cells[0]
    print(y,x)
    #test_map.show_map()
    #print((test_map.landscape_matrix))