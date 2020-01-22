# -*- coding: utf-8 -*-

__author__ = 'Hans Kristian Lunda, Mikko Rekstad'
__email__ = 'hans.kristian.lunda@nmbu.no, mikkreks@nmbu.no'

from biosim.cell import Cell
from biosim.fauna import Herbivore, Carnivore
from biosim.map import Map
from biosim.visualize import Visualize
import pandas as pd
import csv


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
            save_csv=False,
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
        :param save_csv: Boolean, gives the user the option to save mid
               results to a csv-file

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
            self.save_csv = save_csv
            self.visualize = Visualize(self.map, frequency=2, years=200,
                                       img_dir=self.img_base or ".", cmax_animals=self.cmax_animals)
            if self.img_base is not None:
                self._image_counter = 0
                self.vis_years = 1

    @staticmethod
    def check_validity_of_string(island_map):
        """
        This function checks if the mapstring is valid according to
        the project specifications, that is Ocean cell at the map's edges and
        no other landscape than Ocean, Jungle, Savannah, Desert and Mountain,
        and returns a boolean.
        :param island_map: multiline-string
        :return: boolean
        """
        valid_landscape = ['O', 'J', 'S', 'D', 'M']
        temp_lines = island_map.split()

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

    @staticmethod
    def set_animal_parameters(species, params):
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

    @staticmethod
    def set_landscape_parameters(landscape, params):
        """
        Set parameters for landscape type.

        :param landscape: String, code letter for landscape
        :param params: Dict with valid parameter specification for landscape
        """
        for key, value in params.items():
            if (landscape in {'J', 'S'}) \
                    and (key in {'f_max', 'alpha'} and (value >= 0)):
                if landscape == 'J':
                    setattr(Cell, key[4], params[key])
                else:
                    setattr(Cell, key[3], params[key])
            else:
                raise ValueError("Illegal landscape parameter(s)")

    def simulate(self, num_years, vis_years=1, img_years=1):
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
            self.map.yearly_cycle()
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
                self.visualize.update_graphics(self.map,
                                               current_simulation_year)
                self.visualize.save_graphics()
            if self.save_csv is True:
                self.save_mid_simulation_result(herbivores, carnivores, total)

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
            if self.map.cell_map[i][j].landscape not in {2, 3, 4}:
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
        self.visualize.make_movie(movie_fmt='mp4')

    def save_mid_simulation_result(self, herbivores, carnivores, total):
        """ Saves the mid simulation results to a CSV-file each year. """
        with open('save mid simulation result', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([self._year, herbivores, carnivores, total])


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
                for _ in range(100)
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
                for _ in range(10)
            ],
        }
    ]

    sim = BioSim(str(island_map), ini_herbs, seed=18)

    # sim.set_animal_parameters("Herbivore", {"zeta": 3.2, "xi": 1.8})
    # sim.set_animal_parameters(
    #     "Carnivore",
    #     {
    #         "a_half": 70,
    #         "phi_age": 0.5,
    #         "omega": 0.3,
    #         "F": 65,
    #         "DeltaPhiMax": 9.0,
    #     },
    # )
    # sim.set_animal_parameters(
    #     "Carnivore",
    #     {
    #         "a_half": 70,
    #         "phi_age": 0.5,
    #         "omega": 0.3,
    #         "F": 65,
    #         "DeltaPhiMax": 9.0,
    #     },
    # )

    # sim.add_population(population=ini_herbs)
    # sim.set_landscape_parameters("J", {"f_max": 800})
    sim.add_population(population=ini_carns)
    sim.simulate(100, vis_years=1)
    sim.make_movie()

    #properties of the sim object
    print(sim.year)
    print(sim.num_animals)
    print(sim.num_animals_per_species)
    print(sim.animal_distribution)

    # sim.simulate(20, vis_years=5)
    # sim.make_movie()
    # sim.simulate(100)
    # sim.add_population(population=ini_carns)
