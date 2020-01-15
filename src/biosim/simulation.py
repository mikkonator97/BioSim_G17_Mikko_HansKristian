# -*- coding: utf-8 -*-

"""
"""
# from Cell import Cell
from biosim import Cell
from biosim.map import Map
from biosim.fauna import Fauna
from biosim.map import Map

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
                            raise ValueError

        if valid_string is False:
            raise ValueError("Invalid multiline mapstring!")
        else:
            self.island_map = island_map
            self.ini_pop = ini_pop
            self.seed = seed
            self.ymax_animals = ymax_animals
            self.cmax_animals = cmax_animals
            self.img_base = img_base
            self.img_fmt = img_fmt
            self.map = Map(self.island_map)

    def initialize(self):

        self.map = Map(self.island_map)
        self.map.show_map()


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

    def add_population(self, population):
        """
        Add a population to the island

        :param population: List of dictionaries specifying population
        """
        for item in population:
            coordinates = item['loc']
            i = coordinates[0]
            j = coordinates[1]
            cell_pop = item['pop']

            self.map.cell_map[i][j].add_pop(cell_pop)


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

    seed = 1


    #
    # BioSim_test = BioSim(map_string, test, seed)
    # BioSim.initialize()
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
            "loc": (10, 10),
            "pop": [
                {"species": "Herbivore", "age": 5, "weight": 20}
                for _ in range(150)
            ],
        }
    ]

    ini_carns = [
        {
            "loc": (10, 10),
            "pop": [
                {"species": "Carnivore", "age": 5, "weight": 20}
                for _ in range(40)
            ],
        }
    ]
    sim = BioSim(str(island_map), ini_herbs, seed)
    for i in range(sim.map.n_rows):
        for j in range(sim.map.n_cols):
            sim.map.cell_map[i][j].add_fodder()
    print("Cell 10,10 amount of food: ", sim.map.cell_map[10][10].fodder)
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

    sim.add_population(population=ini_carns)
    # for i in range(sim.map.n_rows):
    #     for j in range(sim.map.n_cols):
    #         sim.map.define_adjacent_cells(i, j)

    # sim.map.migrate()

