
"""
This file should not be included in the finnished project.
Will simulate the population of herbivores in a single cell.
The purpose of this is to get a greater understanding of how to deal with the
next problem, which is implementing carnivores and then using the entire map.


"""
#from .fauna import Fauna, Herbivore
#from fauna import Herbivore
#from Cell import Cell
from Cell import Cell
from matplotlib import pyplot as plt
import numpy as np


cell = Cell((3 ,4), landscape='J', fodder=800)


def run_simulation(number_years, start_population):
    x = []
    y = []
    # Creating the start population in the cell.
    # set_animal_parameters('herbivore', params)
    cell.add_pop(start_population)

    for year in range(number_years):


        cell.feed_herbivores()
        print('Year: ', year +1)
        print('Population: ', cell.number_of_herbivores,'\n')
        for creature in cell.population:
            creature.reduce_weight()
            creature.ageing()
            # print('Weight: ' ,creature.weight)
            creature.fitness = creature.calculate_fitness()
            # print('Fitness: ', creature.get_fitness())
            creature.state = creature.death()
            # print('Will die: ', creature.state, '\n')

        cell.alter_population()
        cell.ranked_fitness()
        cell.add_fodder()
        cell.mating_season()

        # print('År: ',year)
        # print(cell.number_of_herbivores)
        x.append(year)
        y.append(cell.number_of_herbivores)


        if cell.number_of_herbivores == 0:
            print('The population is now extinct')

    return x, y




test = [{'loc': (3,4),
         'pop': [{'species': 'herbivore', 'age': 10, 'weight': 15},
                {'species': 'herbivore', 'age': 5, 'weight': 40},
                {'species': 'herbivore', 'age': 15, 'weight': 25}]}]

x, y = run_simulation(200, test)
z = np.mean(x)
plt.plot(x,y)
# plt.plot(x,z)
plt.show()



