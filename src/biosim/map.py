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
        self.cell_map.adjacent_cells = []

        for i in range(self.n_rows):
            for j in range(self.n_cols):
                landscape_type = self.map_string_split[i][j]
                if landscape_type == 'O':
                    self.cell_map[i][j] = Ocean()
                    # self.cell_map[i][j].adjecent_cells =
                elif landscape_type == 'M':
                    self.cell_map[i][j] = Mountain()
                elif landscape_type == 'D':
                    self.cell_map[i][j] = Desert()
                    self.cell_map[i][j].adjecent_cells =[(i+1, j), (i, j-1),
                                                         (i, j+1), (i+1, j)]
                    #     self.cell_map[i+1][j], self.cell_map[i][j-1],
                    #     self.cell_map[i+1][j], self.cell_map[i+1][j]
                    # ]
                elif landscape_type == 'S':
                    self.cell_map[i][j] = Savannah()
                    self.cell_map[i][j].adjecent_cells =[(i+1, j), (i, j-1),
                                                         (i, j+1), (i+1, j)]
                    #     self.cell_map[i + 1][j], self.cell_map[i][j - 1],
                    #     self.cell_map[i + 1][j], self.cell_map[i + 1][j]
                    # ]
                else:
                    self.cell_map[i][j] = Jungle()
                    self.cell_map[i][j].adjecent_cells =[(i+1, j), (i, j-1),
                                                         (i, j+1), (i+1, j)]
                    #     self.cell_map[i + 1][j], self.cell_map[i][j - 1],
                    #     self.cell_map[i + 1][j], self.cell_map[i + 1][j]
                    # ]

    def find(self, coordinate_to_find):
        for i in range(len(self.cell_map)):
            if self.cell_map[i].coordinate == coordinate_to_find:
                return i

    def show_map(self):
        landscape_matrix = np.zeros((self.n_rows, self.n_cols))
        for i in range(self.n_rows):
            for j in range(self.n_cols):
                landscape_matrix[i][j] = self.cell_map[i][j].landscape
        cmap = mpl.colors.ListedColormap(['royalblue', 'grey', 'khaki', 'honeydew', 'forestgreen'])
        plt.imshow(landscape_matrix, cmap=cmap)
        plt.show()

    def migrate(self):
        # Note to self: Må bruke antall dyr før man kjører migrate...
        creatures_to_move = []
        for cell in self.cell_map:
            migrating_probabilites = cell.find_migration()
            for creature in cell.population:
                if creature.wants_to_migrate():
                    chosen_probabilty = np.random.choice(migrating_probabilites)
                    ind = migrating_probabilites.index[chosen_probabilty]
                    i, j = cell.adjecent_cells[ind]
                    creature.desired_location(i, j)
                    creatures_to_move.append(creature)

        for creature in creatures_to_move:
            for i in self.n_rows:
                for j in self.n_cols:
                    if self.cell_map[i][j] != creature.desired_location:
                        self.cell_map[i][j].population += cell.population.pop(creature)
                        creature.desired_location = (i, j)







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
    print(test_map.cell_map[10][10].f_max)
    test_map.show_map()
    #print((test_map.landscape_matrix))