# -*- coding: utf-8 -*-

__author__ = 'Hans Kristian Lunda, Mikko Rekstad'
__email__ = 'hans.kristian.lunda@nmbu.no, mikkreks@nmbu.no'

from biosim import cell
from biosim.fauna import Herbivore, Carnivore
from biosim.map import Map
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sb
import pandas as pd


class BioSim:
    """
    The BioSim class handels the creation of a biosim-object and methods for
    simulation, adding population, setting landscape- and animalparameters.
    There is also a method for making an MPEG4 movie from saved simulation
    images.
    """
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
        :param ymax_animals: Number specifying y-axis limit for graph
               showing animal numbers
        :param cmax_animals: Dict specifying color-code limits for
               animal densities
        :param img_base: String with beginning of file name for figures,
               including path
        :param img_fmt: String with file type for figures, e.g. 'png'

        If ymax_animals is None, the y-axis limit should be adjusted
        automatically.

        If cmax_animals is None, sensible, fixed default values should be used.
        cmax_animals is a dict mapping species names to numbers, e.g.,
           {'Herbivore': 50, 'Carnivore': 20}

        If img_base is None, no figures are written to file.
        Filenames are formed as

            '{}_{:05d}.{}'.format(img_base, img_no, img_fmt)

        where img_no are consecutive image numbers starting from 0.
        img_base should contain a path and beginning of a file name.
        """
        self._animal_distribution = pd.DataFrame()
        self._num_animals_per_species = {'Carnivore': 0, 'Herbivore': 0}
        self._num_animals = 0
        self._year = 0
        if self.check_validity_of_string(island_map) is False:
            raise ValueError("Invalid multiline mapstring!")
        else:
            self.island_map = island_map
            self.seed = seed
            self.ymax_animals = ymax_animals
            self.cmax_animals = cmax_animals
            self.img_base = img_base
            self.img_fmt = img_fmt
            self.map = Map(self.island_map)
            self.add_population(ini_pop)
            if self.img_base is not None:
                self._image_counter = 0
                self.vis_years = 1


    def check_validity_of_string(self, map_string):
        """
        This function checks if the mapstring is valid according to
        the project specifications, that is Ocean cell at the map's edges and
        no other landscape than Ocean, Jungle, Savannah, Desert and Mountain,
        and returns a boolean.
        :param map_string: multiline-string
        :return: boolean
        """
        valid_landscape = ['O', 'J', 'S', 'D', 'M']
        temp_lines = map_string.split()

        for i in temp_lines[1:]:
            if len(i) != len(temp_lines[0]):
                raise ValueError("ValueError: The strings in the multiline "
                                 "string must have equal length!")

        valid_string = ((temp_lines[0].count('O') == len(temp_lines[0]))
                        and (temp_lines[-1].count('O') == len(temp_lines[-1])))

        for line in temp_lines:
            if valid_string is False:
                break
            else:
                if (line[0] and line[-1]) != 'O':
                    valid_string = False
                    break
                else:
                    for letter in line:
                        if letter not in valid_landscape:
                            raise ValueError("Invalid landscape")
        return valid_string

    def set_animal_parameters(self, species, params):
        """
        Set parameters for animal species.

        :param species: String, name of animal species
        :param params: Dict with valid parameter specification for species
        """
        valid_species = {'herbivore', 'carnivore'}
        valid_parameters = ['w_birth', 'sigma_birth', 'beta', 'eta',
                            'a_half', 'phi_age', 'w_half', 'phi_weight',
                            'mu', 'lambda1', 'gamma', 'zeta', 'xi',
                            'omega', 'F', 'DeltaPhiMax']
        species = species.lower()
        for key in params:
            if (species in valid_species) and (key in valid_parameters):
                if species == 'herbivore':
                    setattr(Herbivore, key, params[key])
                else:
                    setattr(Carnivore, key, params[key])
            else:
                raise ValueError("Illegal animal parameter(s)")

    def set_landscape_parameters(self, landscape, params):
        """
        Set parameters for landscape type.

        :param landscape: String, code letter for landscape
        :param params: Dict with valid parameter specification for landscape
        """
        for key, value in params.items():
            if (landscape in {'J', 'S'}) \
                    and (key in {'f_max', 'alpha'} and (value >= 0)):
                if landscape == 'J':
                    setattr(cell.Cell, key[4], params[key])
                else:
                    setattr(cell.Cell, key[3], params[key])
            else:
                raise ValueError("Illegal landscape parameter(s)")

    def simulate(self, num_years, vis_years=1, img_years=None):
        """
        Run simulation while visualizing the result.

        :param num_years: number of years to simulate
        :param vis_years: years between visualization updates
        :param img_years: years between visualizations saved to files
               (default: vis_years)

        Image files will be numbered consecutively.
        """
        self.vis_years = vis_years
        current_simulation_year = 0
        while current_simulation_year < num_years:
            print('Ingoing population: ', self.map.get_populations())
            self.map.feeding_and_procreation()
            self.map.migration()
            self.map.agein_weight_loss_and_death()
            print("current_simulation_year", current_simulation_year + 1,
                  " out of ", num_years)
            current_simulation_year += 1
            self._year += 1
            herbivores, carnivores, total = self.map.get_populations()
            self._num_animals = total
            self._num_animals_per_species = {'Carnivore': carnivores,
                                             'Herbivore': herbivores}
            self._animal_distribution = \
                self.fill_animal_distribution_dataframe()

            if current_simulation_year % vis_years == 0:
                self.visualization(current_simulation_year)
            if (img_years is not None) and (vis_years % img_years == 0):
                pass

    def visualization(self, current_simulation_year):
        """
        Will take care of the visualisation according to specifications in
        simulation.
        :return:
        """
        x = []
        y_herbivores = []
        herbs, carns, total = self.map.get_populations()
        y_herbivores.append(herbs)
        x.append(current_simulation_year)
        pop_map = np.zeros((self.map.n_rows, self.map.n_cols))
        map_matrix = np.zeros((self.map.n_rows, self.map.n_cols))
        for x_cords in range(self.map.n_rows):
            for y_cords in range(self.map.n_cols):
                pop_map[x_cords][y_cords] = self.map.cell_map[x_cords][
                    y_cords].number_herbivores()
                map_matrix[x_cords][y_cords] = self.map.cell_map[x_cords][
                    y_cords].landscape
        # self.illustrate(x, y_herbivores)
        # island = sb.heatmap(map_matrix)
        heat_map = sb.heatmap(pop_map)
        plt.show()
        pass

    def illustrate(self, x, y):
        plt.plot(x, y)
        plt.xlabel('Year')
        plt.ylabel('Population of herbivores')
        plt.show()

    def add_population(self, population):
        """
        Add a population to the island based on dictionary containing
        location('loc') and population('pop'). 'pop' contains species, age,
        and weight of the creature.
        :param population: List of dictionaries specifying population
        """
        for item in population:
            coordinates = item['loc']
            i = coordinates[0]
            j = coordinates[1]
            cell_pop = item['pop']
            if self.map.cell_map[i][j].landscape not in {2,3,4}:
                raise ValueError("The cell is uninhabitable!")
            self.map.cell_map[i][j].add_pop(cell_pop)

    def fill_animal_distribution_dataframe(self):
        """
        The function fills a pandas dataframe with the number of herbivores
        and carnivores in each cell.
        :return: dataframe.
        """
        herbivores = []
        carnivores = []
        col = [j for _ in range(self.map.n_rows)
               for j in range(self.map.n_cols)]

        row = [j for j in range(self.map.n_rows)
               for _ in range(self.map.n_cols)]

        for row_index in range(self.map.n_rows):
            for col_index in range(self.map.n_cols):
                herbivores.append(self.map.cell_map[row_index][
                                      col_index].number_herbivores())
                carnivores.append(self.map.cell_map[row_index][
                                      col_index].number_carnivores())

        data2 = {
                'Row': row,
                'Col': col,
                'Herbivore': herbivores,
                'Carnivore': carnivores
        }
        df = pd.DataFrame(data2,
                          columns=['Row', 'Col', 'Herbivore', 'Carnivore'])
        return df

    @property
    def year(self):
        """Last year simulated."""
        return self._year

    @property
    def num_animals(self):
        """Total number of animals on island."""
        return self._num_animals

    @property
    def num_animals_per_species(self):
        """Number of animals per species in island, as dictionary."""
        return self._num_animals_per_species

    @property
    def animal_distribution(self):
        """
        Pandas DataFrame with animal count per species for each cell on island.
        """
        if self._animal_distribution.empty:
            self._animal_distribution = \
                self.fill_animal_distribution_dataframe()
        return self._animal_distribution

    def make_movie(self):
        """Create MPEG4 movie from visualization images saved."""
        if (self.img_base is not None) and (self._year % self.vis_years == 0):
            plt.savefig('{img_base}_{img_no:05d}.{type}'.format(img_base=self.img_base, img_no=self._image_counter, type=self.img_fmt))
            self._image_counter += 1


if __name__ == '__main__':
    map1 = """\
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

    map_string = map1.split()

    test = [{'loc': (3, 4),
             'pop': [{'species': 'herbivore', 'age': 10, 'weight': 15},
                     {'species': 'herbivore', 'age': 5, 'weight': 40},
                     {'species': 'herbivore', 'age': 15, 'weight': 25}]}]

    island_map = """OOOOOOOOOOOOOOOOOOOOO
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

    ini_herbs = [
        {
            "loc": (4, 6),
            "pop": [
                {"species": "Herbivore", "age": 5, "weight": 20}
                for _ in range(10)
            ],
        },
        # {
        #     "loc": (5, 6),
        #     "pop": [
        #         {"species": "Herbivore", "age": 5, "weight": 20}
        #         for _ in range(150)
        #     ],
        # }

    ]

    ini_carns = [
        {
            "loc": (4, 6),
            "pop": [
                {"species": "Carnivore", "age": 5, "weight": 20}
                for _ in range(40)
            ],
        }
    ]
    seed = 18
    sim = BioSim(str(island_map), ini_herbs, seed)

    sim.set_animal_parameters("Herbivore", {"zeta": 3.2, "xi": 1.8})
    sim.set_animal_parameters(
        "Carnivore",
        {
            "a_half": 70,
            "phi_age": 0.5,
            "omega": 0.3,
            "F": 65,
            "DeltaPhiMax": 9.0,
        },
    )
    sim.set_animal_parameters(
        "Carnivore",
        {
            "a_half": 70,
            "phi_age": 0.5,
            "omega": 0.3,
            "F": 65,
            "DeltaPhiMax": 9.0,
        },
    )

    # sim.add_population(population=ini_herbs)
    sim.set_landscape_parameters("J", {"f_max": 800})

    sim.simulate(20, vis_years=5)
    sim.add_population(population=ini_carns)
    sim.simulate(20, vis_years=5)

    # sim.simulate(100)
    # sim.add_population(population=ini_carns)
