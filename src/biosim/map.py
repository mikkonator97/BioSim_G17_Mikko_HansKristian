__author__ = 'Hans Kristian Lunda, Mikko Rekstad'
__email__ = 'hans.kristian.lunda@nmbu.no, mikkreks@nmbu.no'

from Cell import Cell
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
        Will create the map as a list, containing objects with cells.
        Will also create a matrix in order to be able to visualize the map
        easier later.
        """
        # self.population_herbivores_list
        self.map_string_split = map_string.split()
        self.n_rows = len(self.map_string_split)
        self.n_cols = len(str(self.map_string_split[0]))

        self.number_of_herbivores = 0
        self.number_of_carnivores = 0
        self.population = []

        self.landscape_matrix = np.zeros([self.n_rows, self.n_cols])
        self.cell_map = []

        for i in range(self.n_rows):
            for j in range(self.n_cols):
                current_cell = Cell((i, j), self.map_string_split[i][j],
                                       fodder=0)
                self.cell_map.append(current_cell)
                map_value = self.convert_landscape(self.map_string_split[i][j])
                self.landscape_matrix[i][j] = map_value

    def convert_landscape(self, landscape_type):
        if landscape_type == 'O':
            return 0
        elif landscape_type == 'M':
            return 1
        elif landscape_type == 'D':
            return 2
        elif landscape_type == 'S':
            return 3
        else:
            return 4

    def get_creatures(self):
        """
        Returns the total number of creatures in the cell
        :return: int
        """
        return self.number_of_carnivores + self.number_of_herbivores

    def get_number_of_carnivores(self):
        """
        Returns the number of carnivores in the cell
        :return: int
        """
        return self.number_of_carnivores



    def get_number_of_herbivores(self):
        """
        Returns the number of herbivores in the cell
        :return: int
        """
        return self.number_of_herbivores

    def find(self, coordinate_to_find):
        for i in range(len(self.cell_map)):
            if self.cell_map[i].coordinate == coordinate_to_find:
                return i

    def show_map(self):
        cmap = mpl.colors.ListedColormap(['royalblue', 'grey', 'khaki', 'honeydew', 'forestgreen'])
        plt.imshow(self.landscape_matrix, cmap=cmap)
        plt.show()

    def set_animal_parameters(self, species, params):
        pass


    def add_pop(self, cell_pop):
        """
        Calls the Fauna class to add animals to the cell.
        :param cell_pop: dictionary containing species, age, and weight
        :return:
        """
        for element in cell_pop:

            for creature in element['pop']:
                # print(item.get('species'))
                species = creature.get('species')
                weight = creature.get('weight')
                age = creature.get('age')
                # print(item['species'])
                #self.population.append(Fauna(species, weight, age))
                self.number_of_herbivores += 1

                if species == 'herbivore':
                    self.population.append(Herbivore(species, weight, age))
                    print('Added a herbivore to the population in this cell.')




    def alter_population(self):

        # for index in range(self.number_of_herbivores):
        index = 0
        while index < self.number_of_herbivores:
            # print(self.number_of_herbivores)
            # print(self.population[index].death)
            if self.population[index].state == True:
                print(self.population[index].age,' should be dead')
                self.population.pop(index)
                self.number_of_herbivores = len(self.population)
                index += 1
            index += 1

    def feed_herbivores(self):
        for creature in self.population:
            if self.fodder > 10:
                self.fodder -= 10
                fodder = 10
            else:
                fodder = self.fodder
                self.fodder = 0
            if creature.species == 'herbivore':
                beta = 0.9
                creature.weight += beta * fodder

    def mating_season(self):
        if self.number_of_herbivores > 1:
            for herbivore in self.population:
                if herbivore.species == 'herbivore':

                    herbivore.give_birth()

    def ranked_fitness(self):
        self.population.sort(key=lambda x: x.fitness)




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
    test_map.show_map()
    # print((test_map.landscape_matrix))