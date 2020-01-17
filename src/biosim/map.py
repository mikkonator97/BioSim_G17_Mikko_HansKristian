#from biosim.fauna import Fauna

__author__ = 'Hans Kristian Lunda, Mikko Rekstad'
__email__ = 'hans.kristian.lunda@nmbu.no, mikkreks@nmbu.no'

from biosim.Cell import Cell, Ocean, Mountain, Desert, Savannah, Jungle
import biosim.Cell
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
                    # self.define_adjacent_cells2(row_index, col_index)
                elif landscape_type == 'S':
                    self.cell_map[row_index][col_index] = Savannah()
                    self.define_adjacent_cells(row_index, col_index)
                    # self.define_adjacent_cells2(row_index, col_index)
                else:
                    self.cell_map[row_index][col_index] = Jungle()
                    self.define_adjacent_cells(row_index, col_index)
                    # self.define_adjacent_cells2(row_index, col_index)

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


    def migration(self):
        """
        This function will summon all functions related to migration.
        :return:
        """
        # Will update preferred location to each creature.
        self.update_preferred_locations()
        # self.move_to_preferred_location()

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

        for cell in self.cell_map:
            cell.attractiveness_herbivore()
            # cell.attractiveness_carnivore()
        for cell in self.cell_map:
            index = 0
            for location in cell.adjacent_cells:
                # Updates preferrence lists for both species
                x, y = location
                print('Location: ', location)
                cell.herbivore_preferrence[index] = cell_map[x][
                    y].chance_herbivores
                #cell.herbivore_preferrence[index] = cell_map[x][
                #   y].lucrativeness_herbivores
                index += 1

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
        # for list_of_cells in self.cell_map:
        #     for cell in list_of_cells:
        #         if cell.population_herbivores != []:
        #             print('Antall herbivores her: ', len(cell.population_herbivores))
        #         for creature in cell.population_herbivores:
        #             # Lets the creature be able to mate as well.
        #             creature.have_mated = False
        #             creature.fitness = creature.calculate_fitness()
        #         cell.ranked_fitness_herbivores()
        #         cell.add_fodder()
        #         cell.feed_herbivores()
        #         # print('Amount of fodder left this year: ', cell.fodder)
        #         # OPS! Feed carnivores might need some more funcs
        #         # cell.feed_carnivores()
        #         cell.mating_season()
        #
        # code for carrying out feeding and procreation for each cell
        for row_index in range(self.n_rows):
            for col_index in range(self.n_cols):
                if self.cell_map[row_index][col_index].landscape == (0 or 1):
                    continue
                else:
                    for creature in self.cell_map[row_index][col_index].population_herbivores:
                        creature.fitness = creature.calculate_fitness()
                    self.cell_map[row_index][col_index].add_fodder()
                    self.cell_map[row_index][col_index].ranked_fitness_herbivores()
                    self.cell_map[row_index][col_index].feed_herbivores()
                    # Note to self: re-calculate fitness of hervbivores since weight has been increased?
                    for creature in self.cell_map[row_index][col_index].population_herbivores:
                        creature.fitness = creature.calculate_fitness()
                    self.cell_map[row_index][col_index].feed_carnivores()
                    self.cell_map[row_index][col_index].mating_season()


    def yearly_stage_2(self):
        """
        Here we will just summon the migration function when its redo.
        The function loops through the map and calls migrate for all the herbivores.
        :return:
        """

        print("Yearly stage 2 has started")
        for row_index in range(self.n_rows):
            for col_index in range(self.n_cols):
                for cell in self.cell_map[row_index][col_index].adjacent_cells:
                    cell.adjacent_cells_attractiveness = [
                        self.cell_map[row_index + 1][
                            col_index].attractiveness_herbivore(),
                        self.cell_map[row_index][
                            col_index - 1].attractiveness_herbivore(),
                        self.cell_map[row_index - 1][
                            col_index].attractiveness_herbivore(),
                        self.cell_map[row_index][
                            col_index + 1].attractiveness_herbivore()
                    ]

        for row_index in range(self.n_rows):
            for col_index in range(self.n_cols):
                self.cell_map[row_index][col_index].send_adjacent_cells_to_fauna()

        for row_index in range(self.n_rows):
            for col_index in range(self.n_cols):
                herbivore_list = self.cell_map[row_index][col_index].population_herbivores
                # herbivore_list = self.cell_map[row_index][col_index].get_herbivores()
                # print("herbivore list: ", herbivore_list)

                for herbivore in herbivore_list:
                    herbivore_desired_cell = herbivore.migrate()
                    if herbivore_desired_cell is None:
                        continue
                    else:
                        print("herbivore_desired_cell: ", herbivore_desired_cell)
                        herbivore_desired_cell.population_herbivores.append(herbivore)
                        herbivore_list.remove(herbivore)
                        herbivore.have_migrated = True


        print("Yearly stage 2 has finished")


    def yearly_stage3(self):
        """
        4. aging, 5. Loss of weight and 6. Death.
        :return:
        """
        for row_index in range(self.n_rows):
            print("row", row_index)
            for col_index in range(self.n_cols):
                print("col", col_index)
                print("cell: ", self.cell_map[row_index][col_index])

                cell = self.cell_map[row_index][col_index]
                print("landscape: ", cell.landscape)
                if cell.landscape in {2, 3, 4}:
                    cell.add_age()
                    cell.lose_weight()
                    print("lose weight has been called")
                    for creature in cell.population_herbivores:
                        print("creature", creature)
                        creature.fitness = creature.calculate_fitness
                        creature.have_mated = False
                        creature.have_migrated = False
                    cell.alter_population()
    print("yearly_stage3() has finished")

    def yearly_cycle(self):
        # OPS! some of these functions can be put together
        self.yearly_stage1()
        # self.yearly_stage_2()
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