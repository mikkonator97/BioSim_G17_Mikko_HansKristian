
import pandas as pd
from map import Map
from biosim.fauna import Fauna
from biosim.map import Map
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sb

__author__ = ""
__email__ = ""


class BioSim:
    def __init__(
        self,
        island_map,
        ini_pop,
        seed,
        ymax_animals=None,
        cmax_animals=None,
        img_base=None,
        img_fmt="png",
    ):
        """
        :param island_map: Multi-line string specifying island geography
        :param ini_pop: List of dictionaries specifying initial population
        :param seed: Integer used as random number seed
        :param ymax_animals: Number specifying y-axis limit for graph showing animal numbers
        :param cmax_animals: Dict specifying color-code limits for animal densities
        :param img_base: String with beginning of file name for figures, including path
        :param img_fmt: String with file type for figures, e.g. 'png'

        If ymax_animals is None, the y-axis limit should be adjusted automatically.

        If cmax_animals is None, sensible, fixed default values should be used.
        cmax_animals is a dict mapping species names to numbers, e.g.,
           {'Herbivore': 50, 'Carnivore': 20}

        If img_base is None, no figures are written to file.
        Filenames are formed as

            '{}_{:05d}.{}'.format(img_base, img_no, img_fmt)

        where img_no are consecutive image numbers starting from 0.
        img_base should contain a path and beginning of a file name.
        """
        # Boring stuff
        self.island_map = island_map
        self.ini_pop = ini_pop
        self.seed = seed
        self.ymax_animals = ymax_animals
        self.cmax_animals = cmax_animals
        self.img_base = img_base
        self.img_fmt = img_fmt
        # Cool stuff
        self.map = Map(self.island_map)
        self.insert_population(ini_pop)

    def insert_population(self, population):
        for item in population:
            i, j = item['loc']
            cell_pop = item['pop']
            self.map.cell_map[i][j].add_pop(cell_pop)


    def set_animal_parameters(self, species, params):
        """
        Set parameters for animal species.

        :param species: String, name of animal species
        :param params: Dict with valid parameter specification for species
        """
        if species == 'herbivore':
            for key in params.keys():
                getattr(Fauna, key)[0] = params[key]

        else:
            for key in params.keys():
                getattr(Fauna, key)[1] = params[key]

    def set_landscape_parameters(self, landscape, params):
        """
        Set parameters for landscape type.

        :param landscape: String, code letter for landscape
        :param params: Dict with valid parameter specification for landscape
        """
        if landscape == 'J':
            for key in params.keys():
                getattr(Cell.Cell, key)[0] = params[key]

        else:
            for key in params.keys():
                getattr(Cell.Cell, key)[1] = params[key]

    def simulate(self, num_years, vis_years=1, img_years=None):
        """
        Run simulation while visualizing the result.

        :param num_years: number of years to simulate
        :param vis_years: years between visualization updates
        :param img_years: years between visualizations saved to files (default: vis_years)

        Image files will be numbered consecutively.
        """
        n = int(num_years / 10)
        #x = np.linspace(10, num_years, n)
        x = []
        y_herbivores = []
        #y_carnivores = [0] * n
        #y_total = [0] * n
        for year in range(num_years):
            print('Year: ', year)
            print('Ingoing population: ', self.map.get_populations())
            self.map.yearly_cycle()
            if year % 10 == 0:
                herbs, carns, total = self.map.get_populations()
                y_herbivores.append(herbs)
                x.append(year)
                #y_carnivores[year] = carns
                #y_total[year] = total
        pop_map = np.zeros((self.map.n_rows, self.map.n_cols))
        map_matrix = np.zeros((self.map.n_rows, self.map.n_cols))
        for x_cords in range(self.map.n_rows):
            for y_cords in range(self.map.n_cols):
                pop_map[x_cords][y_cords] = self.map.cell_map[x_cords][y_cords].number_herbivores()
                map_matrix[x_cords][y_cords] = self.map.cell_map[x_cords][y_cords].landscape
        self.illustrate(x, y_herbivores)
        island = sb.heatmap(map_matrix)
        heat_map = sb.heatmap(pop_map)
        plt.show()

    def illustrate(self, x, y):
        plt.plot(x, y)
        plt.xlabel('Year')
        plt.ylabel('Population of herbivores')
        plt.show()




    @property
    def year(self):
        """Last year simulated."""
        pass

    @property
    def num_animals(self):
        """Total number of animals on island."""
        pass

    @property
    def num_animals_per_species(self):
        """Number of animals per species in island, as dictionary."""
        pass

    @property
    def animal_distribution(self):
        """Pandas DataFrame with animal count per species for each cell on island."""
        pass

    def make_movie(self):
        """Create MPEG4 movie from visualization images saved."""
        pass

if __name__ == '__main__':
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
                     {'species': 'herbivore', 'age': 15, 'weight': 25}]}
            ]
    """
    {"loc": (10, 10),
        "pop": [{"species": "herbivore", "age": 1, "weight": 10},
                {'species': 'herbivore', 'age': 5, 'weight': 40},
                {'species': 'herbivore', 'age': 5, 'weight': 40},
                {'species': 'herbivore', 'age': 5, 'weight': 40},
                {'species': 'herbivore', 'age': 5, 'weight': 40},
                {'species': 'herbivore', 'age': 5, 'weight': 40}
    ]}
    """
    seed = 1

    BioSim_test = BioSim(map_string, test, seed)

    # print('(10,10): ', BioSim_test.map.cell_map[10][10].population[1].age)
    # print('(10,10): ', BioSim_test.map.cell_map[10][10].population[0].age)
    BioSim_test.simulate(10)

    print(BioSim_test.map.cell_map[10][10].adjacent_cells2[1])
